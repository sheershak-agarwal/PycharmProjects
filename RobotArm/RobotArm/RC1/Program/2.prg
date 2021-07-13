1 Close #2
2 *Top
3 Dly 1
4 Open "COM2:" As #2 ' Open as communication line COM3
5 *StateLoop
6 Input #2,DATA,DATA1 ' Wait for reception of value in DATA variable
7 If DATA=20 Then GoSub *ResetComs2
8 If DATA=40 Then GoSub *LoadNextPositions  'This needs to be moved to Slot 2 so can load next positions while runmotion is going.
9 '
10 GoTo *StateLoop
11 '
12 '-----------------------------------------SERVO ON
13 '
14 *ResetComs2
15 Close #2
16 GoTo *Top
17 Return
18 '
19 '-----------------------------------------SERVO OFF
20 '
21 '
22 '------------------------------------------LOAD POSITION ARRAY
23 '
24 *LoadNextPositions
25 '
26 Select DATA1
27 '
28 'Load position array P_100(1-9)
29 '
30 Case 100
31 Print #2,"42"
32 Input #2,P_100(1),P_100(2),P_100(3),P_100(4),P_100(5),P_100(6),P_100(7),P_100(8),P_100(9)' Wait for reception of value in DATA variable
33 Print #2,"P_100(1-9)"
34 Break
35 '
36 'Load position array P_101(1-9)
37 '
38 Case 101
39 Print #2,"42"
40 Input #2,P_100(1),P_101(2),P_101(3),P_101(4),P_101(5),P_101(6),P_101(7),P_101(8),P_101(9)' Wait for reception of value in DATA variable
41 Print #2,"P_101(1-9)"
42 Break
43 '
44 End Select
45 Print #2,"44"
46 Return
47 '
48 '-----------------------------------------MOVE THROUGH POSITION ARRAY
49 '
PHome=(+469.97,+0.00,+855.10,-180.00,+0.01,+180.00)(7,0)
