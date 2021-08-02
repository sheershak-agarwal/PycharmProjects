import socket

# ROBOT_ARM Variables
import time

ROBOT_HOST = '192.168.3.20'  # The server's hostname or IP address
CONFIG_PORT = 10005  # The port used by the server
POS_PORT = 10003
ERROR_PORT = 10004


def config_robot_arm():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;OPEN=PORT10005')
        data = s.recv(1024)
    print('Received Open Port:', repr(data))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;CNTLON')
        data1 = s.recv(1024)
        s.sendall(b'1;1;SLOTINIT')
        data2 = s.recv(1024)
        s.sendall(b'1;2;SLOTINIT')
        data3 = s.recv(1024)
    print('Received Program INIT:', repr(data1), repr(data2), repr(data3))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;CNTLON')
        data1 = s.recv(1024)
        s.sendall(b'1;1;RUN1;1')
        data = s.recv(1024)
    print('Received Program Run:', repr(data))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;CNTLON')
        data1 = s.recv(1024)
        # robot number, slot number, RUN Program Number, Mode number (1: cyclic start, 0: repeat start)
        s.sendall(b'1;2;RUN2;1')
        data = s.recv(1024)
    print('Received Program Run:', repr(data))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;CNTLON')
        data1 = s.recv(1024)
        s.sendall(b'1;1;SRVON')
        data = s.recv(1024)
    print('Received ServoOn:', repr(data))
    time.sleep(1)


def turn_off_robot():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;CNTLON')
        data1 = s.recv(1024)
        s.sendall(b'1;1;SRVOFF')
        data = s.recv(1024)
        s.sendall(b'1;1;STOP')
        data2 = s.recv(1024)
        s.sendall(b'1;2;STOP')
        data3 = s.recv(1024)
    print('Received ServoOff:', repr(data), repr(data1), repr(data2), repr(data3))


pos_x = 657.0
pos_y = -39.0
pos_z = 550.0
pos_a = 180.0
pos_b = 0.0
pos_c = 150.0
switch = False


def error_encounter():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, ERROR_PORT))
        data = s.recv(1024)
    print('Received', repr(data))

    time.sleep(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, CONFIG_PORT))
        s.sendall(b'1;1;RSTALRM')
        data1 = s.recv(1024)
        s.sendall(b'1;2;RSTALRM')
        data2 = s.recv(1024)
    print('Received', repr(data1), repr(data2))
    return repr(data)


def move():
    pos = str.encode(
        "(" + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(pos_a) + "," + str(pos_b) + "," + str(
            pos_c) + ")(7,0)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, POS_PORT))
        s.sendall(pos)
        data = s.recv(1024)
        print('Received', repr(data))


config_robot_arm()
move()
# while True:
#     for i in range(32):
#         move()
#         time.sleep(.3)
#         if switch:
#             pos_y -= 12
#         else:
#             pos_y += 12
#     switch = ~switch
#     pos_x += 12

# for i in range(16):
#     for j in range(33):
#         move()
#         time.sleep(.2)
#         if (j != 32):
#             if switch:
#                 pos_y -= 12
#             else:
#                 pos_y += 12
#     switch = ~switch
#     pos_x -= 12

# turn_off_robot()
# for i in range(10):
#     pos = str.encode(
#         "(" + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(pos_a) + "," + str(pos_b) + "," + str(
#             pos_c) + ")(7,0)")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((ROBOT_HOST, POS_PORT))
#         s.sendall(pos)
#         data = s.recv(1024)
#     print('Received', repr(data))
#     if (i % 2 == 0):
#         pos_z += 100.0
#     else:
#         pos_z -= 100.0
#
#     time.sleep(.5)
