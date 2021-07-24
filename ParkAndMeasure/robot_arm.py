import socket

# ROBOT_ARM Variables
import time

ROBOT_HOST = '192.168.3.20'  # The server's hostname or IP address
CONFIG_PORT = 10005  # The port used by the server
POS_PORT = 10003


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
        s.sendall(b'1;1;RUN1;1')
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


config_robot_arm()

pos_x = 578.520
pos_y = 39.59
pos_z = 520.0
pos_a = 180.0
pos_b = 0.0
pos_c = -30.0
switch = False


def move():
    pos = str.encode(
        "(" + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(pos_a) + "," + str(pos_b) + "," + str(
            pos_c) + ")(7,0)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, POS_PORT))
        s.sendall(pos)
        data = s.recv(1024)
    print('Received', repr(data))


for i in range(10):
    for j in range(10):
        move()
        time.sleep(.5)
        if switch:
            pos_y += 15
        else:
            pos_y -= 15
    switch = ~switch
    pos_x += 20

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
