
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
    yum = testingModule.Dinner()
    yum.printFood()


    exit()

# Plot labeling:
xLabel     = "$^{4}$He Energy [MeV]"
yLabel     = "Cross Section [mb/MeV/sr]"
title      = "Double Differential Spectra ($^{4}$He)"
annotation = "$^{238}$U (5.5 GeV p, X) $^{4}$He"
figName    = "trial1"

# Create input file class:
inputObj = PlotGSMInputFile("pU.plot.inp")

exit()


# X limits:
myPlot.xMin(0)
myPlot.xMax(150)
# Y limits:
# myPlot.yMin(1.0E-12)
# myPlot.yMax(100)
# Labeling:
myPlot.setXLabel( xLabel)
myPlot.setYLabel( yLabel )
myPlot.setTitle( title )
myPlot.annotateXY( annotation )


outputfiles = ("pU.c.out", "pU.g.out") #, "pU.l.out")

# Obtain histogram object:
simData   = []
dataLabel = []
for i in range(0, len(outputfiles), 1):

    if ( ".g." in outputfiles[i] ):
        dataLabel.append( "GSM" )
        simData.append( GSMOutput( outputfiles[i] ) )
    elif ( ".c." in outputfiles[i] ):
        dataLabel.append( "CEM" )
        simData.append( CEMOutput( outputfiles[i] ) )
    elif ( ".l." in outputfiles[i] ):
        dataLabel.append( "LAQGSM" )
        continue
    else:
        label = input("Input line label for data from file \"%s\": " % (outputfiles[i]) )
        dataLabel.append( label.strip() )

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
