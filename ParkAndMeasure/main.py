import pyvisa as visa
import serial
import time
import pandas as pd

chip = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30, 31]
values = [0x27, 0x2f, 0x37, 0x3f, 0x47, 0x4f, 0x57, 0x5f]
vna_addr = 'TCPIP0::127.0.0.1::5025::SOCKET'
rs_addr  = 'TCPIP0::169.254.5.55::5025::SOCKET'
ser_addr = 'COM9'
device = 'RS'


def config_vna():
    rm = visa.ResourceManager('@py')
    # Connect to a Socket on the local machine at 5025
    # Use the IP address of a remote machine to connect to it instead
    try:
        if device == 'RS':
            cmt = rm.open_resource(rs_addr)
        elif device == 'VNA':
            cmt = rm.open_resource(vna_addr)
        print("Successfully connected to VNA!")
    except:
        print("Failure to connect to VNA!")
        print("Check network settings")
    # The VNA ends each line with this. Reads will time out without this
    cmt.read_termination = '\n'
    # Set a really long timeout period for slow sweeps
    cmt.timeout = 10000
    return cmt


def config_serial():
    s = serial.Serial(ser_addr)
    s.baudrate = 9600
    return s


# CONFIGURE VNA and serial connection
vna = config_vna()
ser = config_serial()


def write_uart():
    while True:
        ser.write('Hello'.encode())


def get_vna_data(index):
    print(vna.query("*IDN?"))

    # TODO: Change the SCPI command here
    # Perform single sweep
    # vna.write('TRIG:SOUR BUS\n')
    # vna.write('TRIG:SEQ:SING\n')
    # vna.query('*OPC?\n')

    # query data
    if (device == 'C1420'):
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
