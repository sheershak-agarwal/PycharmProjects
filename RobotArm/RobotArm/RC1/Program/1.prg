1 Close #1
2 Dly 1
3 Open "COM1:" As #1 ' Open as communication line COM3 port 10003
4 *StateLoop
5 Input #1,P1' Wait for reception of value in DATA variable
6 Print #1,"P1 Loaded"
7 Input #1,DATA' Wait for reception of value in DATA variable
8 If DATA=10 Then GoSub *RunMotionSingle
9 GoTo *StateLoop
10 '----------------------
11 *RunMotionSingle
12 '
13 Mov P1
14 Print #1,"Motion Completed"
15 Return
16 '
17 '
P1=(+390.00,+400.00,+400.00,-180.00,+0.00,+180.00)(7,0)
P2=(+525.00,+200.00,+400.00,-180.00,+0.00,+180.00,+0.00,+0.00)(7,0)
PHome=(+469.97,+0.00,+855.10,-180.00,+0.01,+180.00)(7,0)
