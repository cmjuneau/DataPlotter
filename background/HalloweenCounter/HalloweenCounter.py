
################################################################################
# This script is used to count groups of people and possibly provide some
#    statistics, if user desired.
#
# Written by CMJ, 10/2018
#
################################################################################

# Python imports
import datetime as dtime
import time
import math
import numpy as np
import sys


import ManyGroupClass
from ManyGroupClass import ManyGroup


def printInstructions():
    # Print script instructions
    print("\n\n\n")
    print("=============================================================")
    print("Hello, and welcome all! Tonight is gonna get BUSY, so be")
    print("be prepared!")
    print("")
    print("This python script allows you to easily track and count the")
    print("number of trick-or-treaters that visit you on this evening.")
    print("Once you are done giving out candy, this script will plot the")
    print("data for you on a histogram and give you some statistics.")
    print("")
    print("NOTE: More data than is necessary is 'tracked' with this script,")
    print("but why not? I couldn't get all interfacing done properly,")
    print("but time is finite and I had to get this rolled out. Oh well...")
    print("")
    print("Anyways, good luck!")
    print("=============================================================")
    print("\n\n\n")


def getSaveFile(defaultName = "TrickOrTreaters-", extension = ".txt"):
    """Obtains a filename to save data to"""
    # Obtain file name to save data to

    # Make default filename
    time = dtime.datetime.now()
    fileName = defaultName + str( time.year ) + extension
    print("Data will be saved to file '" + fileName + "', by default.")
    validData = False
    while ( not validData ):
        data = input("   Do you want to use a different filename (y/n)? ")
        data = data.lower().strip()
        if ( data[ : 1 ] == "n" ):
            validData = True

        elif ( data[ : 1 ] == "y" ):
            # Obtain new file name
            validData = True

            # Use non-default filename
            data = input("   What file would you like data saved to? ")
            data = data.strip()
            fileName = data

        else:
            print("Error: Please enter a valid input (either 'y' for yes or 'n' for no).")
            validData = False

    return fileName


def endScript(stopMessage = "Have a nice day homie!"):
    print("\n\n\n")
    print("I hope you enjoyed your night and all the smiles that occurred!")
    print(stopMessage)
    print("\n\n\n")
    sys.exit()

################################################################################
# Start of script
################################################################################

# Print instructions to user
printInstructions()

# Obtain fileName to save data to
fileName = getSaveFile()
print("Data will be saved to '" + fileName + "' in the current directory.\n")


# Make a class and collect data
newDay = ManyGroup()
newDay.collectData(fileName)


# End script
endScript()
