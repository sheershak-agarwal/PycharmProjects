import pyvisa as visa
import serial
import time
import pandas as pd
import numpy as np


chip = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30, 31]
values = [0x27, 0x2f, 0x37, 0x3f, 0x47, 0x4f, 0x57, 0x5f]

numPoints = 101
startFreq = 11E9
stopFreq = 12E9
vna_addr = 'TCPIP0::127.0.0.1::5025::SOCKET'
rs_addr  = 'TCPIP0::169.254.5.55::5025::SOCKET'
ff_addr = "TCPIP0::192.168.3.1::inst0::INSTR"
ser_addr = 'COM9'
device = 'FF'



def config_vna():
    rm = visa.ResourceManager('@py')
    # Connect to a Socket on the local machine at 5025
    # Use the IP address of a remote machine to connect to it instead
    try:
        if device == 'RS':
            cmt = rm.open_resource(rs_addr)
        elif device == 'VNA':
            cmt = rm.open_resource(vna_addr)
        elif device == 'FF':
            cmt = rm.open_resource(ff_addr)
            print("Successfully connected to VNA!")
            cmt.timeout = 10000
            cmt.write("*CLS")
            # Query identification string *IDN?
            cmt.write("*IDN?")
            print(cmt.read())
    except:
        print("Failure to connect to VNA!")
        print("Check network settings")
    # The VNA ends each line with this. Reads will time out without this
    #cmt.read_termination = '\n'

    return cmt


def config_serial():
    s = serial.Serial(ser_addr)
    s.baudrate = 9600
    return s


# CONFIGURE VNA and serial connection
vna = config_vna()
#ser = config_serial()


def write_uart():
    while True:
        ser.write('Hello'.encode())


def get_vna_data(index):

    # TODO: Change the SCPI command here
    # Perform single sweep
    # vna.write('TRIG:SOUR BUS\n')
    # vna.write('TRIG:SEQ:SING\n')
    # vna.query('*OPC?\n')

    # query data
    if (device == 'C1420'):
        print(vna.query("*IDN?"))
        Freq = vna.query("SENS1:FREQ:DATA?\n")  # Get data as string
        S11 = vna.query("CALC1:TRAC1:DATA:FDAT?\n")  # Get data as string

        Freq = Freq.split(",")
        S11 = S11.split(",")

        # S11 = S11[::2]
        # S11 = [float(s) for s in S11]
        # Freq = [float(f) for f in Freq]

        ll = []
        for i in range(len(Freq)):
            ll.append([Freq[i], S11[2*i], S11[2*i+1]])
        df = pd.DataFrame(ll, columns=['Frequency', 'I', 'Q'])
        print(df)
        df.to_csv(str(index)+'_VNAData.csv', sep=',')
    elif (device == 'RS'):
        print(vna.query("*IDN?"))
        vna.write('FORM ASC')
        vna.write('FORM ASC')
        vna.write('SENS:FREQ:CENT 13000000000')
        vna.write('SENS:FREQ:SPAN 5000000')
        vna.write('SENS:BAND:RES 3000')
        vna.write('SENS:AVER:COUN 5')
        vna.write('SENS:AVER ON')
        vna.write('SENS:SWE:POIN 101')
        # vna.write('CALC1:MARK1:X:13000000000')
        # raw_y_data = vna.query('CALC:MARK1:Y?')
        # data  vna.
        vna.write('INIT;*WAI')
        # Freq = vna.query("TRAC:DATA:X?")  # Get data as string

        spectrum = vna.query('TRAC:DATA? TRACE1')  # Get data as string
        spectrum = spectrum.split(",")
        # print(Freq)

        ll = []
        for i in range(len(spectrum)):
            ll.append([spectrum[i]])
        df = pd.DataFrame(ll, columns=['Amplitude'])
        print(df)
        df.to_csv(str(index) + '_FSW_Data.csv', sep=',')

        print(len(spectrum))
    elif (device == 'FF'):
        vna.write("SYST:PRES;*OPC?")
        print("Preset complete, *OPC? returned : " + vna.read())
        vna.write("INST:SEL 'SA';*OPC?")
        vna.read()
        vna.write("SENS:SWE:POIN " + str(numPoints))

        vna.write("SENS:FREQ:START " + str(startFreq))

        vna.write("SENS:FREQ:STOP " + str(stopFreq))

        vna.write("SENS:SWE:POIN?")
        numPoints = vna.read()
        print("Number of trace points " + numPoints)
        vna.write("SENS:FREQ:START?")
        startFreq = vna.read()
        vna.write("SENS:FREQ:STOP?")
        stopFreq = vna.read()
        print("FieldFox start frequency = " + startFreq + " stop frequency = " + stopFreq)
        # Set trigger mode to hold for trigger synchronization
        vna.write("INIT:CONT OFF;*OPC?")
        vna.read()

        stimulusArray = np.linspace(float(startFreq), float(stopFreq), int(numPoints))

        print(stimulusArray)
        vna.write("INIT:IMM;*OPC?")

        print("Single Trigger complete, *OPC? returned : " + vna.read())

        # Query the FieldFox response data

        vna.write("TRACE:DATA?")

        ff_SA_Trace_Data = vna.read()

        print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.

        # Use split to turn long string to an array of values

        ff_SA_Trace_Data_Array = ff_SA_Trace_Data.split(",")

        ll = []
        for i in range(len(ff_SA_Trace_Data_Array)):
            ll.append([stimulusArray[i], ff_SA_Trace_Data_Array[i]])
        df = pd.DataFrame(ll, columns=['Freq', 'Amplitude'])
        print(df)
        df.to_csv(str(index) + '_FSW_Data.csv', sep=',')


for i in range(len(chip)):
    # write_uart()
    # time.sleep(5)
    get_vna_data(i)
    #time.sleep(5)

    # while ser.inWaiting():
    #     recv = ser.readline()
    #     if (recv == "OK"):
    #         print(vna.query("*IDN?"))
    #
