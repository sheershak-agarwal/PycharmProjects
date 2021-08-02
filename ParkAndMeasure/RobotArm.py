import socket
import time


ROBOT_HOST = '192.168.3.20'  # The server's hostname or IP address
CONFIG_PORT = 10005  # The port used by the server
POS_PORT = 10003
ERROR_PORT = 10004


class RobotArm:
    def __init__(self):
        self.config_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config_s.connect((ROBOT_HOST, CONFIG_PORT))
        self.config_s.sendall(b'1;1;OPEN=PORT10005')
        data = self.config_s.recv(1024)
        print('Received Open Port:', repr(data))
        self.config_s.sendall(b'1;1;CNTLON')
        data1 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;1;SLOTINIT')
        data2 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;2;SLOTINIT')
        data3 = self.config_s.recv(1024)
        print('Received Program INIT:', repr(data1), repr(data2), repr(data3))

        self.config_s.sendall(b'1;1;CNTLON')
        data1 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;1;RUN1;1')
        data = self.config_s.recv(1024)
        print('Received Program Run:', repr(data))

        self.config_s.sendall(b'1;1;CNTLON')
        data1 = self.config_s.recv(1024)
        # robot number, slot number, RUN Program Number, Mode number (1: cyclic start, 0: repeat start)
        self.config_s.sendall(b'1;2;RUN2;1')
        data = self.config_s.recv(1024)
        print('Received Program Run:', repr(data))

        self.config_s.sendall(b'1;1;CNTLON')
        data1 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;1;SRVON')
        data = self.config_s.recv(1024)
        print('Received ServoOn:', repr(data))

        self.pos_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pos_s.connect((ROBOT_HOST, POS_PORT))
        time.sleep(1)

    def __del__(self):
        self.config_s.sendall(b'1;1;CNTLON')
        data1 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;1;SRVOFF')
        data = self.config_s.recv(1024)
        self.config_s.sendall(b'1;1;STOP')
        data2 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;2;STOP')
        data3 = self.config_s.recv(1024)
        print('Received ServoOff:', repr(data), repr(data1), repr(data2), repr(data3))
        self.config_s.close()
        self.pos_s.close()

    def error_encounter(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ROBOT_HOST, ERROR_PORT))
            data = s.recv(1024)
        print('Received', repr(data))

        time.sleep(2)
        self.config_s.connect((ROBOT_HOST, CONFIG_PORT))
        self.config_s.sendall(b'1;1;RSTALRM')
        data1 = self.config_s.recv(1024)
        self.config_s.sendall(b'1;2;RSTALRM')
        data2 = self.config_s.recv(1024)
        print('Received', repr(data1), repr(data2))
        return repr(data)

    def move(self, pos_x, pos_y, pos_z, pos_a, pos_b, pos_c):
        pos = str.encode(
            "(" + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(pos_a) + "," + str(pos_b) + "," + str(
                    pos_c) + ")(7,0)")
        self.pos_s.sendall(pos)
        data = self.pos_s.recv(1024)
        print('Received', repr(data))


# ra = RobotArm()
#
# x = 657.0
# y = -39.0
# z = 550.0
# a = 180.0
# b = 0.0
# c = 60.0
# switch = False
#
# for i in range(16):
#     for j in range(33):
#         ra.move(x, y, z, a, b, c)
#         time.sleep(.2)
#         if (j != 32):
#             if switch:
#                 y -= 12
#             else:
#                 y += 12
#     switch = ~switch
#     x -= 12