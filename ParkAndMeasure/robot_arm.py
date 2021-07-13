import socket

# ROBOT_ARM Variables
import time

ROBOT_HOST = '10.1.10.118'  # The server's hostname or IP address
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

pos_x = 300.0
pos_y = 400.0
pos_z = 400.0
pos_a = -180.0
pos_b = 0.0
pos_c = 180.0
for _ in range(10):
    pos = str.encode(
        "(" + str(pos_x) + "," + str(pos_y) + "," + str(pos_z) + "," + str(pos_a) + "," + str(pos_b) + "," + str(
            pos_c) + ")(7,0)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, POS_PORT))
        s.sendall(pos)
        data = s.recv(1024)
    print('Received', repr(data))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ROBOT_HOST, POS_PORT))
        s.sendall(b'10')
        data = s.recv(1024)
    print('Received', repr(data))
    pos_x += 10.0
    time.sleep(1)
