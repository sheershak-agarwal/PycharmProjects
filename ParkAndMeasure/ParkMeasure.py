from FieldFox import FieldFox
from RobotArm import RobotArm
from P5024A import P5024A
import time
import os
import serial
from datetime import datetime

# global variables
# can be changed
numPoints = 11
startFreq = 115e8
stopFreq = 117e8
board = 'SN210015'
num_times = 5

# don't change below
offset = 12.0
HOME = [663.0, -176.0, 550.0, 180.0, 0.0, 150.0]  # x, y, z, a, b, c

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
         15: 'F'}

LARGE_SCAN = [325.0, -485.0, 600.0, 180.0, 0.0, 150.0]
POS_C = 150.0


class ParkMeasure:

    def __init__(self, board_number='SN210003', se=None, pos=[664.05, -38.18, 550.0, 180.0, 0.0, 150.0], f=None,
                 r=None):
        self.path = os.path.join('C:\\Users\Sheershak Agarwal\Desktop\PycharmProjects\ParkAndMeasure\\' + board_number)
        self.create_directory()
        self.initial_pos = [663.0, -176.0, 550.0, 180.0, 0.0, 150.0]
        self.board_number = board_number
        self.offset = offset
        self.switch = False
        self.POS_C = 150.0
        self.ff = f
        self.ser = se
        # print('send R')
        if self.ser is not None:
            self.ser.write(b"R\r\n")
            time.sleep(10)
        self.ra = r

        # self.chip = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        #         28, 29, 30, 31]
        # self.values = [0x27, 0x2f, 0x37, 0x3f, 0x47, 0x4f, 0x57, 0x5f]

    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            print("directory created at ", self.path)

    def park(self):
        self.ra.move(self.initial_pos[0],
                     self.initial_pos[1],
                     self.initial_pos[2],
                     self.initial_pos[3],
                     self.initial_pos[4],
                     self.initial_pos[5])

    # https://www.sutron.com/micropython/html/library/serial.html#:~:text=1%20port%20%28%20str%29%20%E2%80%93%20is%20the%20serial,%E2%80%93%20Enable%20H%2FW%20flow%20control.%20More%20items...%20
    def program_controller(self, m, n):
        self.ser.write("pcx\r\n".encode())
        command = 'pcr 1000' + m + '0' + n + ' 3F8\r\n'
        print('sending command ' + command)
        self.ser.write(command.encode())
        time.sleep(.1)

    def measure(self):
        self.ff.create()

    def complete_op(self):
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
                self.measure()
                self.program_controller(map_m[i], str(x))
                # time.sleep(.5)
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
        self.ff.create_file(self.board_number)

    def complete_op_optimized(self):
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        self.initial_pos = [663.0, -176.0, 550.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
        self.ff.change_mode('phase')
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
                self.program_controller(map_m[i], str(x))
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
        self.initial_pos = [663.0, -176.0, 550.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
        self.ff.change_mode('amp')
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
                self.program_controller(map_m[i], str(x))
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
        self.ff.create_file_optimized(self.board_number, freq_arr, amp_mat, phase_mat, self.path)

    def complete_op_optimized_newvna(self):
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        self.initial_pos = [663.0, -176.0, 550.0, 180.0, 0.0, 150.0]
        self.ra.change_speed("slow")
        self.park()
        self.ra.change_speed("fast")
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
                self.program_controller(map_m[i], str(x))
                amp_arr, phase_arr = self.ff.create_array()
                phase_mat.append(phase_arr)
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
        self.ff.create_file_optimized(self.board_number, freq_arr, amp_mat, phase_mat, self.path)

    def complete_op_large_scan(self):
        freq_arr = self.ff.create_frequency_array()
        phase_mat = []
        amp_mat = []
        for k in range(1):
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
                    print('positions', self.initial_pos, LARGE_SCAN)
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
            self.ff.create_file_optimized_scan(self.board_number, freq_arr, amp_mat, phase_mat, k)


s = serial.Serial(port='COM4', baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, dsrdtr=False,
                  rtscts=False, xonxoff=False)
fieldfox = FieldFox(numPoints, startFreq, stopFreq)
robotarm = RobotArm()
p = P5024A(numPoints, startFreq, stopFreq)
for _ in range(num_times):
    pm = ParkMeasure(board_number=board, se=s, pos=[663.0, -176.0, 550.0, 180.0, 0.0, 150.0], f=p, r=robotarm)
    # pm.complete_op_optimized()
    # pm.complete_op_large_scan()
    pm.complete_op_optimized_newvna()