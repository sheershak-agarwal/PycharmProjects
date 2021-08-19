import pyvisa as visa
import pandas as pd
import numpy as np
import time
import datetime
import math

class P5024A:
    def __init__(self, points=11, start=11e9, stop=12e9, ip = 'TCPIP0::localhost::hislip0::INSTR'):
        print("Init the P5024A")
        self.numPoints = points
        self.startFreq = start
        self.stopFreq = stop
        self.ip = ip
        self.ll = []
        rm = visa.ResourceManager()
        self.vna = rm.open_resource(self.ip)
        self.vna.timeout = 10000
        self.vna.write("*RST")
        self.vna.write("*CLS")
        self.vna.write(":SYST:PRES")
        self.vna.write("*IDN?")
        print(self.vna.read())
        self.vna.write("*OPC?")
        self.vna.write(":CALCulate: PARameter:DELete: ALL:")
        self.vna.write(':CALCulate1:PARameter:DEFine:EXTended "S12_Sweep_Amp","S12"')
        self.vna.write(':CALCulate1:PARameter:DEFine:EXTended "S12_Sweep_Pha","S12"')
        self.vna.write(':DISPlay:ARRange STACk')
        self.vna.write(':DISPlay:WINDow1:TRACe:FEED "S12_Sweep_Amp"')
        self.vna.write(':DISPlay:WINDow2:TRACe:FEED "S12_Sweep_Pha"')
        self.vna.write(':CALCulate1:PARameter:SELect "S12_Sweep_Amp"')
        self.vna.write(':CALCulate1:FORMat MLOGarithmic')
        self.vna.write(':CALCulate1:PARameter:SELect "S12_Sweep_Pha"')
        self.vna.write(':CALCulate1:FORMat PHASe')
        self.vna.write(':SENSe1:BANDwidth:RESolution 1000')
        self.vna.write(':SOURce1:POWer1:LEVel:IMMediate:AMPLitude -25')
        self.vna.write(':SENSe1:SWEep:POINts ' + str(self.numPoints))
        self.vna.write(':SENSe1:FREQuency:STARt ' + str(self.startFreq))
        self.vna.write(':SENSe1:FREQuency:STOP ' + str(self.stopFreq))
        print("VNA start frequency = " + str(self.startFreq) + " stop frequency = " + str(self.stopFreq) + " number of point is " + str(self.numPoints))
        self.vna.write(':INITiate1:CONTinuous 0')
        self.vna.write(':FORMat:DATA ASCii')
        self.vna.write(':CALCulate:X:VALues?')

    def create_frequency_array(self):
        stimulusArray = np.linspace(float(self.startFreq), float(self.stopFreq), int(self.numPoints))
        return stimulusArray

    def create_array(self):
        self.vna.write(':INITiate1:IMMediate')
        self.vna.write(':CALCulate1:PARameter:SELect "S12_Sweep_Amp"')
        self.vna.write(':CALCulate1:DATA? FDATa')
        # time.sleep(.5)

        ff_SA_Amplitude_Data = self.vna.read()
        ff_SA_Amplitude_Data_Array = ff_SA_Amplitude_Data.split(",")
        print("Amp_Data_Array", ff_SA_Amplitude_Data_Array)

        self.vna.write(':CALCulate1:PARameter:SELect "S12_Sweep_Pha"')
        self.vna.write(':CALCulate1:DATA? FDATa')
        ff_SA_Phase_Data = self.vna.read()
        ff_SA_Phase_Data_Array = ff_SA_Phase_Data.split(",")
        print("Phase_Data_Array", ff_SA_Phase_Data_Array)
        return ff_SA_Amplitude_Data_Array, ff_SA_Phase_Data_Array


    def create_row(self, freq, amp, phase):
        row = []
        for i in range(self.numPoints):
            row.append(freq[i])
            row.append(amp[i])
            row.append(phase[i])
        self.ll.append(row)

    def create(self):
        stimulusArray = np.linspace(float(self.startFreq), float(self.stopFreq), int(self.numPoints))
        # print(stimulusArray)
        self.vna.write("CALC:FORMat PHASe")
        time.sleep(.5)
        self.vna.write("CALC:DATA:FDATa?")
        ff_SA_Phase_Data = self.vna.read()
        # print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.

        # Use split to turn long string to an array of values

        ff_SA_Phase_Data_Array = ff_SA_Phase_Data.split(",")
        print("ff_SA_Phase_Data_Array", ff_SA_Phase_Data_Array)

        self.vna.write("CALC:FORMat MLOG")
        # time.sleep(.5)
        self.vna.write("CALC:DATA:FDATa?")
        ff_SA_Amplitude_Data = self.vna.read()
        # print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.

        # Use split to turn long string to an array of values
        ff_SA_Amplitude_Data_Array = ff_SA_Amplitude_Data.split(",")
        print("Data_Array", ff_SA_Amplitude_Data_Array)


        # # self.vna.write("CALC:FORMat PHAS")
        # self.vna.write("CALC:DATA:FDATa?")
        # ff_SA_Phase_Data = self.vna.read()
        # # print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.
        #
        # # Use split to turn long string to an array of values
        #
        # ff_SA_Phase_Data_Array = ff_SA_Phase_Data.split(",")
        # print("ff_SA_Phase_Data_Array", ff_SA_Phase_Data_Array)

        row = []
        for i in range(self.numPoints):
            row.append(stimulusArray[i])
            row.append(ff_SA_Amplitude_Data_Array[i])
            row.append(ff_SA_Phase_Data_Array[i])

        self.ll.append(row)
        # self.vna.write("INIT:CONT ON")

    def create_file(self, board, path=None):
        columns = []
        for i in range(self.numPoints):
            columns.append('Frequency_' + str(i + 1))
            columns.append('Amplitude_' + str(i + 1))
            columns.append('Phase_' + str(i + 1))

        df = pd.DataFrame(self.ll, columns=columns)
        # print(df)
        if path:
            df.to_csv(path + '\\' + board + '_' + datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%S_%p_") + '_FSW_Data.csv', sep=',')
        else:
            df.to_csv(board + '_' + datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%S_%p_") + '_FSW_Data.csv', sep = ',')
        print(board + '_' + datetime.datetime.now().strftime("%d_%m_%y_%I_%M_%S_%p_") + 'FSW_Data.csv file created')
        self.ll = []

    def create_file_optimized(self, board, freq_arr, amp_mat, phase_mat, path):
        columns = []
        for i in range(self.numPoints):
            columns.append('Frequency_' + str(i + 1))
            columns.append('Amplitude_' + str(i + 1))
            columns.append('Phase_' + str(i + 1))

        for i in range(len(amp_mat)):
            self.create_row(freq_arr, amp_mat[i], phase_mat[i])
        self.create_file(board, path)

    def create_file_optimized_scan(self, board, freq_arr, amp_mat, phase_mat, path, k):
        columns = []
        for i in range(self.numPoints):
            columns.append('Frequency_' + str(i + 1))
            columns.append('Amplitude_' + str(i + 1))
            columns.append('Phase_' + str(i + 1))

        for i in range(len(amp_mat)):
            self.create_row(freq_arr, amp_mat[i], phase_mat[i])
        if k == 0:
            self.create_file(board + '_ex', path)
        elif k == 1:
            self.create_file(board + '_ey', path)
        else:
            self.create_file(board, path)
    # def __del__(self):
    #     self.vna.clear()
    #     self.vna.close()