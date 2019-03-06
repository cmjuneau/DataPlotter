
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
from gsmPlotClass import PlotGSMInputFile
from outputClass import GSMOutput, CEMOutput

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
inputObj = PlotGSMInputFile("pU.plot.inp")

exit()



desiredParticles = ["He4"]
desiredAngles = [10, 30, 90, 120, 30]
for i in range(0, len(desiredParticles), 1):
    for j in range(0, len(desiredAngles), 1):
        for k in range(0, len(simData), 1):
            thisPISAData = simData[k].getPISAData()
            thisParticle = thisPISAData.getParticle(desiredParticles[i])
            if ( not thisParticle == None ):
                thisHistogram = thisParticle.getHistogram(desiredAngles[j])
                if ( not thisHistogram == None ):
                    # Add histogram:
                    myPlot.addHistogram(thisHistogram.getBinValues(), thisHistogram.getDataPoints(), dataLabel[k])
        # End of output loop:
        typeLabel = str(desiredAngles[j]) + " degrees"
        myPlot.annotateLine( typeLabel )
        myPlot.addType()
    # End of angle loop:
# End of particle loop:



myPlot.savePlot( figName )

################################################################################
exit()
