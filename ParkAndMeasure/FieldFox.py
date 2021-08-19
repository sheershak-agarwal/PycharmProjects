import pyvisa as visa
import pandas as pd
import numpy as np
import time
import datetime
import math

class FieldFox:
    def __init__(self, points=11, start=11e9, stop=12e9, ip = "TCPIP0::192.168.3.1::inst0::INSTR"):
        print("Init the FieldFox")
        self.numPoints = points
        self.startFreq = start
        self.stopFreq = stop
        self.ip = ip
        self.ll = []
        rm = visa.ResourceManager()
        self.myFieldFox = rm.open_resource(self.ip)
        self.myFieldFox.timeout = 10000
        self.myFieldFox.write("*RST")
        self.myFieldFox.write("*CLS")
        self.myFieldFox.write("*IDN?")
        print(self.myFieldFox.read())
        self.myFieldFox.write("SYST:PRES;*OPC?")
        print("Preset complete, *OPC? returned : " + self.myFieldFox.read())
        self.myFieldFox.write("INST:SEL 'NA';*OPC?")
        self.myFieldFox.read()
        #self.myFieldFox.write("DISP:WIND:SPL D12_34")
        self.myFieldFox.write("CALC:PAR1:DEF S12")
        self.myFieldFox.write("CALC:PAR1:SEL")
        # self.myFieldFox.write("CALC:FORMat PHASe")
        self.myFieldFox.write("BWID 10e2")
        self.myFieldFox.write("SOUR:POW -25")
        self.myFieldFox.write("SENS:SWE:POIN " + str(self.numPoints))
        self.myFieldFox.write("SENS:FREQ:START " + str(self.startFreq))
        self.myFieldFox.write("SENS:FREQ:STOP " + str(self.stopFreq))
        print("FieldFox start frequency = " + str(self.startFreq) + " stop frequency = " + str(self.stopFreq) + " number of point is " + str(self.numPoints))
        self.myFieldFox.write("INIT:CONT ON;*OPC?")
        self.myFieldFox.read()
        # time.sleep(1)

    def change_mode(self, mode='phase'):
        if mode == 'phase':
            self.myFieldFox.write("CALC:FORMat PHASe")
        elif mode == 'amp':
            self.myFieldFox.write("CALC:FORMat MLOG")
        time.sleep(.5)

    def create_frequency_array(self):
        stimulusArray = np.linspace(float(self.startFreq), float(self.stopFreq), int(self.numPoints))
        return stimulusArray

    def create_array(self):
        time.sleep(.1)
        self.myFieldFox.write("CALC:DATA:FDATa?")
        # time.sleep(.5)
        ff_SA_Amplitude_Data = self.myFieldFox.read()
        ff_SA_Amplitude_Data_Array = ff_SA_Amplitude_Data.split(",")
        print("Data_Array", ff_SA_Amplitude_Data_Array)
        return ff_SA_Amplitude_Data_Array


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
        self.myFieldFox.write("CALC:FORMat PHASe")
        time.sleep(.5)
        self.myFieldFox.write("CALC:DATA:FDATa?")
        ff_SA_Phase_Data = self.myFieldFox.read()
        # print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.

        # Use split to turn long string to an array of values

        ff_SA_Phase_Data_Array = ff_SA_Phase_Data.split(",")
        print("ff_SA_Phase_Data_Array", ff_SA_Phase_Data_Array)

        self.myFieldFox.write("CALC:FORMat MLOG")
        # time.sleep(.5)
        self.myFieldFox.write("CALC:DATA:FDATa?")
        ff_SA_Amplitude_Data = self.myFieldFox.read()
        # print("ff_SA_Trace_Data", ff_SA_Trace_Data)  # This is one long comma separated string list of values.

        # Use split to turn long string to an array of values
        ff_SA_Amplitude_Data_Array = ff_SA_Amplitude_Data.split(",")
        print("Data_Array", ff_SA_Amplitude_Data_Array)


        # # self.myFieldFox.write("CALC:FORMat PHAS")
        # self.myFieldFox.write("CALC:DATA:FDATa?")
        # ff_SA_Phase_Data = self.myFieldFox.read()
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
        # self.myFieldFox.write("INIT:CONT ON")

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
    #     self.myFieldFox.clear()
    #     self.myFieldFox.close()


# ff = FieldFox()
# ff.create()
