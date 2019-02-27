
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
from plotClass import Plot
from fileModule import readFile

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

# Creating plot object:
myPlot = Plot()


outputfiles = ("pBe.c.out", "pBe.g.out", "pBe.l.out")
fileData = readFile( outputfiles[1] )


myPlot.xMin(25)
myPlot.xMax(50)
myPlot.setXLabel("Something cool!")
myPlot.yMin(1.0E-5)
myPlot.yMax(1.0E+5)
myPlot.setYLabel("I'm not sure what this could be...")
myPlot.setTitle("Also something cool!")
myPlot.savePlot("trial1")




################################################################################
exit()
