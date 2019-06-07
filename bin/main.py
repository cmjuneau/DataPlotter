
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
import os
import datetime
from math import floor
from multiprocessing import Pool


# Modules:
sys.path.insert(0, './src')   # Add personal python scripts to path:
from gsmPlotClass import PlotGSMInputFile
from printClass import Print

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

def determineNumProcessors():
    """Determines the number of processors to use"""
    _maxAllowedProcessors = 20
    numProcessors = min( floor( 0.8*(os.cpu_count()) ), _maxAllowedProcessors )
    if ( numProcessors <= 0 ):
        numProcessors = 1
    return numProcessors


################################################################################
# Script start:
################################################################################
if __name__ == "__main__":
    printTime("Start")

    # Test any new featurers here:
    if ( testingModule.letsTest ):
        exit()

    # Obtain all input files given (assume all are inputs):
    cmdArgs = sys.argv
    cmdArgs.pop(0)
    numArgs = len(cmdArgs)
    if(numArgs <= 1):
        eprint("")
        eprint("--------------------------------------------")
        eprint("This script may accept any number of input")
        eprint("   files, requiring at least one input file.")
        eprint("")
        eprint("Each input file is given its own processor")
        eprint("   to aid in image generation.")
        eprint("")
        eprint("--------------------------------------------")

    eprint("The provided command line arguments include:")
    for i in range(0, numArgs):
        eprint("\t{}: {}".format(i+1, cmdArgs[i].strip()) )


    # Now perform for each input (use multiple processors):
    _numProcessors = min(determineNumProcessors(), numArgs)
    print("The script is being ran using {} processor(s).".format(_numProcessors) )

    # Create input file class for each provided file:
    if(_numProcessors > 1):
        with Pool(processes=_numProcessors) as pool:
            pool.map(PlotGSMInputFile, cmdArgs)
            pool.close()
            pool.join()
    else:
        messageControlloer = Print(5)
        PlotGSMInputFile( cmdArgs[0], messageControlloer )

    exit()
