
################################################################################
# File documentation:
"""
This file contains the methods used to plot stuff
"""
################################################################################
# EDIT LOG
# ------------------------------------------------------------------------------
# CMJ, XCP-3 (02/2019)
#
#
################################################################################
# IMPORTS:
import sys
import datetime


# Modules:
sys.path.insert(0, '../src')   # Add personal python scripts to path:
import gsmPlotClass

# For testing ideas:
import testingModule


# VERSION Number:
__version__ = "1.0.0"


def eprint(*args, **kwargs):
    """Prints messages to std:err"""
    print(*args, file=sys.stderr, **kwargs)


def printTime(str = "Start"):
    """Prints at what time this function was called"""
    scriptStart = "%s: %s.\n" % (str.strip(), datetime.datetime.now())
    eprint("")
    eprint("")
    eprint("----------------------------------------------")
    eprint(scriptStart.strip())
    eprint("----------------------------------------------")
    eprint("")
    eprint("")


def exit():
    """Exits script"""
    printTime("Script done")
    sys.exit()


################################################################################
# Script start:
################################################################################
printTime("Start")

if ( testingModule.letsTest ):
    # Put whatever interface is needed to test out the new feature(s) here:


    exit()



# Create input file class:
inputObj = gsmPlotClass.PlotGSMInputFile("pU.plot.inp")


################################################################################
exit()
