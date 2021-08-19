import numpy as np

from FieldFox import FieldFox
from RobotArm import RobotArm
import time
import os
import serial
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# global variables
# can be changed
numPoints = 11
startFreq = 115e8
stopFreq = 117e8
board = 'SN210025'
num_times = 2

# don't change below
offset = 12.0
HOME = [664.05, -38.18, 550.0, 180.0, 0.0, 150.0]  # x, y, z, a, b, c

map_index = {0: '0',
             1: '1',
             2: '1',
             3: '0',
             4: '0',
             5: '1',
             6: '1',
             7: '0',
             8: '0',
             9: '1',
             10: '1',
             11: '0',
             12: '0',
             13: '1',
             14: '1',
             15: '0',
             16: '0',
             17: '1',
             18: '1',
             19: '0',
             20: '0',
             21: '1',
             22: '1',
             23: '0',
             24: '0',
             25: '1',
             26: '1',
             27: '0',
             28: '0',
             29: '1',
             30: '1',
             31: '0'
             }
map_m = {0: '0',
         1: '1',
         2: '2',
         3: '3',
         4: '4',
         5: '5',
         6: '6',
         7: '7',
         8: '8',
         9: '9',
         10: 'A',
         11: 'B',
         12: 'C',
         13: 'D',
         14: 'E',
         15: 'F' }

map_hex = {'0000': '0',
         '0001': '1',
         '0010': '2',
         '0011': '3',
         '0100': '4',
         '0101': '5',
         '0110': '6',
         '0111': '7',
         '1000': '8',
         '1001': '9',
         '1010': 'A',
         '1011': 'B',
         '1100': 'C',
         '1101': 'D',
         '1110': 'E',
         '1111': 'F' }


class NearField:

    def __init__(self, board_number='SN210002', se=None, pos=[664.05, -38.18, 550.0, 180.0, 0.0, 150.0], f=None, r=None):
        self.initial_pos = [664.05, -38.18, 550.0, 180.0, 0.0, 150.0]
        self.path = os.path.join('C:\\Users\Sheershak Agarwal\Desktop\PycharmProjects\ParkAndMeasure\\' + board_number + "_e")
        self.create_directory()
        self.board_number = board_number
        self.offset = offset
        self.switch = False
        self.ff = f
        self.ser = se
        # print('send R')
        self.ser.write(b"R\r\n")
        time.sleep(10)
        self.ra = r
        phase_target = 90.0
        cal_data = pd.read_csv(board + "\\" + board + "_final_calibration.csv", header=None)
        phase_array = []
        amp_array = []
        phase_mean_array = []
        amp_mean_array = []
        phase_step_array = []
        amp_step_array = []
        phase_target_array = []
        amp_target_array = []
        for index, row in cal_data.iterrows():
            amp_array.append(row[1])
            phase_array.append(row[2])

        index = 1
        while index <= len(amp_array):
            avg = np.average(amp_array[index-1:index+15])
            amp_mean_array.append(avg)
            phase_mean_array.append(np.average(phase_array[index - 1:index + 15]))
            # print(count, amp_array[index-1:index+15])
            index+=16
        print("phase_mean_array", phase_mean_array)

        print("amp_mean_array", amp_mean_array)

        for ii in phase_mean_array:
            val = round((phase_target - ii)/5.625)
            phase_step_array.append(val)
            phase_target_array.append(ii + (val*5.625))

        amp_target = np.average(amp_mean_array)
        for jj in range(len(amp_mean_array)):
            # print("..."", amp_mean_array[jj])
            diff = amp_mean_array[jj]-amp_target
            if diff <= -3:
                print("Delete this element ", amp_mean_array[jj], " because it is 3db smaller than ", amp_target)
                amp_mean_array.pop(jj)
            else:
                if amp_mean_array[jj] <= amp_target:
                    amp_target_array.append(amp_mean_array[jj])
                    amp_step_array.append(0)
                else:
                    val = round((amp_mean_array[jj]-amp_target) / 0.45)
                    amp_target_array.append(amp_mean_array[jj] - (val * 0.45))
                    amp_step_array.append(val)

        # print("phase_target", phase_target)
        # print("amp_target", amp_target)
        # print("phase_target_array", phase_target_array)
        # print("amp_target_array",amp_target_array)
        # print("phase_step_array", phase_step_array)
        # print("amp_step_array", amp_step_array)

        self.commands = []
        val = '0'
        count = 1
        for i in range(len(phase_step_array)):
            p = '{0:06b}'.format(abs(phase_step_array[i]))
            a = '{0:06b}'.format(amp_step_array[i])
            b = ''
            for j in a:
                if j == '0':
                    b+='1'
                else:
                    b+='0'
            pa = p + b
            temp = map_hex[pa[0:4]] + map_hex[pa[4:8]] + map_hex[pa[8:12]]
            command = 'pcr 1000' + map_m[int(i/2)] + '0' + map_index[i] + ' ' + temp + '8\r\n'
            self.commands.append(command)
        print(self.commands)
        # self.array_plot(phase_target,phase_target_array, phase_mean_array, amp_target,amp_target_array, amp_mean_array)

    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print("directory created at ", self.path)

    def array_plot(self,phase_target,phase_target_array, phase_mean_array, amp_target,amp_target_array, amp_mean_array):
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.set_title('Phase Data')
        ax1.plot([phase_target] * 32, 'r--')
        ax1.plot(phase_target_array, 'g^')
        ax1.plot(phase_mean_array, 'bs', alpha=0.3)

        ax2.set_title('Amplitude Data')
        ax2.plot([amp_target] * 32, 'r--')
        ax2.plot(amp_target_array, 'g^')
        ax2.plot(amp_mean_array, 'bs', alpha=0.3)
        plt.show()

    def program_controller(self, index):
        self.ser.write("pcx\r\n".encode())
        time.sleep(.1)
        print('sending command ' + self.commands[index])
        self.ser.write(self.commands[index].encode())
        time.sleep(.1)

    def send_all_program_controller(self):
        print('command sent', len(self.commands))
        self.ser.write("pcx\r\n".encode())
        time.sleep(.1)
        for comm in self.commands:
            self.ser.write(comm.encode())
            print('command sent', comm)
        time.sleep(.1)

    def park(self):
        self.ra.move(self.initial_pos[0],
                     self.initial_pos[1],
                     self.initial_pos[2],
                     self.initial_pos[3],
                     self.initial_pos[4],
                     self.initial_pos[5])

    def near_field_scan(self):
        self.send_all_program_controller()
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        self.initial_pos = [568.05, -300.18, 600.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
        self.ff.change_mode('amp')
        time.sleep(1)

        for _ in range(56):
            self.park()
            amp_arr = self.ff.create_array()
            amp_mat.append(amp_arr)
            self.initial_pos[1] += self.offset
        self.ff.create_file_optimized(self.board_number, freq_arr, amp_mat, amp_mat)

    def complete_op_optimized(self):
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        self.initial_pos = [664.05, -38.18, 550.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
        self.ff.change_mode('phase')
        index_of_array = 0
        for i in range(16):
            for j in range(32):
                # park
                self.park()
                # measure
                x = 0
                if self.switch:
                    if j <= 15:
                        x = 1
                else:
                    if j > 15:
                        x = 1
                # self.measure()
                self.program_controller(index_of_array)
                if j == 15 or j == 31:
                    index_of_array+=1
                phase_arr = self.ff.create_array()
                phase_mat.append(phase_arr)
                # time.sleep(.2)
                if j == 15:
                    if self.switch:
                        self.initial_pos[1] -= self.offset
                    else:
                        self.initial_pos[1] += self.offset
                if j != 31:
                    if self.switch:
                        self.initial_pos[1] -= self.offset
                    else:
                        self.initial_pos[1] += self.offset
            self.switch = ~self.switch
            self.initial_pos[0] -= self.offset
        # change mode
        self.initial_pos = [664.05, -38.18, 550.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
        self.ff.change_mode('amp')
        index_of_array = 0
        for i in range(16):
            for j in range(32):
                # park
                self.park()
                # measure
                x = 0
                if self.switch:
                    if j <= 15:
                        x = 1
                else:
                    if j > 15:
                        x = 1
                # self.measure()
                self.program_controller(index_of_array)
                if j == 15 or j == 31:
                    index_of_array+=1
                # time.sleep(.5)
                amp_arr = self.ff.create_array()
                amp_mat.append(amp_arr)
                # time.sleep(.2)
                if j == 15:
                    if self.switch:
                        self.initial_pos[1] -= self.offset
                    else:
                        self.initial_pos[1] += self.offset
                if j != 31:
                    if self.switch:
                        self.initial_pos[1] -= self.offset
                    else:
                        self.initial_pos[1] += self.offset
            self.switch = ~self.switch
            self.initial_pos[0] -= self.offset
        self.ff.create_file_optimized(self.board_number, freq_arr, amp_mat, phase_mat)

    def complete_op_large_scan(self):
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        for k in range(2):
            if k == 0:
                self.POS_C = 150.0
            else:
                self.POS_C = 60.0
            self.initial_pos = [350.0, -400.0, 600.0, 180.0, 0.0, self.POS_C]
            self.ra.change_speed("slow")
            self.park()
            self.ra.change_speed("fast")
            self.ff.change_mode('phase')
            time.sleep(1.5)
            for i in range(30):
                for j in range(62):
                    # park
                    self.park()
                    phase_arr = self.ff.create_array()
                    phase_mat.append(phase_arr)
                    # time.sleep(.2)
                    if j != 61:
                        if self.switch:
                            self.initial_pos[1] -= self.offset
                        else:
                            self.initial_pos[1] += self.offset
                self.switch = ~self.switch
                self.initial_pos[0] += self.offset
            # change mode
            self.initial_pos = [350.0, -400.0, 600.0, 180.0, 0.0, self.POS_C]
            self.ra.change_speed("slow")
            self.park()
            self.ra.change_speed("fast")
            self.ff.change_mode('amp')
            time.sleep(1.5)
            for i in range(30):
                for j in range(62):
                    # park
                    self.park()
                    amp_arr = self.ff.create_array()
                    amp_mat.append(amp_arr)
                    # time.sleep(.2)
                    if j != 61:
                        if self.switch:
                            self.initial_pos[1] -= self.offset
                        else:
                            self.initial_pos[1] += self.offset
                self.switch = ~self.switch
                self.initial_pos[0] += self.offset
            self.ff.create_file_optimized_scan(self.board_number, freq_arr, amp_mat, phase_mat, self.path, k)



s = serial.Serial(port='COM4', baudrate = 115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, dsrdtr = False, rtscts  = False, xonxoff  = False)
fieldfox = FieldFox(numPoints, startFreq, stopFreq)
robotarm = RobotArm()
nf = NearField(board_number=board, se=s, pos=[664.05, -38.18, 550.0, 180.0, 0.0, 150.0], f=fieldfox, r=robotarm)
nf.send_all_program_controller()
for i in range(num_times):
    nf.complete_op_large_scan()
