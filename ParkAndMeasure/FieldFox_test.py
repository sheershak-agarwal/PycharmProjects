import pyvisa as visa
import os

# The numpy is imported as it is helpful for a linear ramp creation for the stimulus array

import numpy as npStimulusArray

# import module for plotting

import matplotlib.pyplot as stimulusResponsePlot

# A variable to control various events and testing during development.

# by uncommenting the #debug True line, debug will occur, for efficiency, during development.

debug = False

# debug = True

print("Debug flag set to " + str(debug))

# Set variables for ease of change - assumes 'debug is true.

# If debug is set to false then Spectrum Analyzer preset defaults for

# start frequency, stop frequency and number of points are utilized.

numPoints = 21

startFreq = 1.28579E9

stopFreq = 2.28579E9

# Open a VISA resource manager pointing to the installation folder for the Keysight Visa libraries.

rm = visa.ResourceManager('@py')

# Based on the resource manager, open a session to a specific VISA resource string as provided via

# Keysight Connection Expert

# ALTER LINE BELOW - Updated VISA resource string to match your specific configuration

myFieldFox = rm.open_resource("TCPIP0::192.168.3.1::inst0::INSTR")

# Set Timeout - 10 seconds

myFieldFox.timeout = 10000

# Clear the event status registers and empty the error queue

myFieldFox.write("*CLS")

# Query identification string *IDN?

myFieldFox.write("*IDN?")

print(myFieldFox.read())


# Define Error Check Function

def Errcheck():
    myError = []

    ErrorList = myFieldFox.query("SYST:ERR?").split(',')

    Error = ErrorList[0]

    if int(Error) == 0:

        print("+0, No Error!")

    else:

        while int(Error) != 0:
            print("Error #: " + ErrorList[0])

            print("Error Description: " + ErrorList[1])

            myError.append(ErrorList[0])

            myError.append(ErrorList[1])

            ErrorList = myFieldFox.query("SYST:ERR?").split(',')

            Error = ErrorList[0]

            myError = list(myError)

    return myError


# Call and print error check results

print(Errcheck())

# myFieldFox.write("SYST:PRES;*OPC?")
#
# print("Preset complete, *OPC? returned : " + myFieldFox.read())

# Set mode to Spectrum Analyzer and wait for operation complete via the *OPC?, i.e.

# the operation complete query.

myFieldFox.write("INST:SEL 'NA';*OPC?")

myFieldFox.read()

# If debug is true then user setting of start frequency, stop frequency and number of points

# if debug:
#     myFieldFox.write("SENS:SWE:POIN " + str(numPoints))
#
#     myFieldFox.write("SENS:FREQ:START " + str(startFreq))
#
#     myFieldFox.write("SENS:FREQ:STOP " + str(stopFreq))

# Determine, i.e. query, number of points in trace for ASCII transfer - query

myFieldFox.write("SENS:SWE:POIN?")

numPoints = myFieldFox.read()

print("Number of trace points " + numPoints)

# Determine, i.e. query, start and stop frequencies, i.e. stimulus begin and end points

myFieldFox.write("SENS:FREQ:START?")

startFreq = myFieldFox.read()

myFieldFox.write("SENS:FREQ:STOP?")

stopFreq = myFieldFox.read()

print("FieldFox start frequency = " + startFreq + " stop frequency = " + stopFreq)

myFieldFox.write("CALC:SEL:DATA:FDATa")
