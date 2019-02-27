
################################################################################
# File documentation:
"""
This module provides a plot class which can be used to generate plots.

Plots have the following characteristics:
    -
    -
    -
"""
################################################################################
# EDIT LOG
# ------------------------------------------------------------------------------
# CMJ, XCP-3 (02/2019)
#
#
################################################################################
# IMPORTS:
import matplotlib as plotlib
import matplotlib.pyplot as plt
from pylab import rcParams
import sys
import time

# MODULES:
from printClass import Print
import fileModule


# VERSION Number:
__version__ = "1.0.0"


# Plot defaults:
plt.rc('font', **{'family': 'serif'})   # Which font to use
defaultFont = 14
figureFont = 11
plotlib.rcParams.update({'font.size': figureFont})
# Figure size:
rcParams['figure.figsize'] = 6.811, 3.5 # Width, Height


# Actual Plot class:
class Plot:
    """
    This is the plot class
    """
    # Class for printing messages:
    __write = Print()
    # General plot information:
    __plotName = "?"
    __labelFont = defaultFont
    __titleFont = defaultFont + 2
    # X information
    __xScale = "linear"
    __xLabel = "?"
    __xMin  = 0
    __xMax  = 250
    # Y information
    __yScale = "symlog"
    __yLabel = "?"
    __yMin  = 1.0E-10
    __yMax  = 1.0E+10
    # Regarding annotation:
    __annotation = "?"
    __annotateX  = 1.10 * __xMin
    __annotateY  = 1.10 * __yMin


    def __init__(self, newPrint=Print()):
        """Plot class constructor"""

        # Set defaults:
        self.__write = Print()
        # General plot information:
        self.__plotName = "?"
        self.__labelFont = defaultFont
        self.__titleFont = self.__labelFont + 2
        self.__annotation = "?"
        self.__annotateX  = 1.10 * self.__xMin
        self.__annotateY  = 1.10 * self.__yMin
        # X Information
        self.__xLabel = "?"
        self.__xScale = "linear"
        self.__xMin = 0
        self.__xMax = 250
        # Y Information
        self.__yLabel = "?"
        self.__yScale = "symlog"
        self.__yMin = 1.0E-10
        self.__yMax = 1.0E+10


        # Set values passed in:
        self.__write = newPrint


        # Set plot details:
        self.setPlotDetails()



    def setPlotDetails(self):
        """Sets plot details"""
        # Set default plot values:
        self.setGrid()
        self.setScale()
        self.setX()
        self.setXLabel()
        self.setY()
        self.setYLabel()
        self.setTitle()


    def annotateXY(self, newX=None, newY=None, annotation=None):
        """Sets the X/Y of the annotation"""
        if ( not newX == None ):
            self.__annotateX = newX
        else:
            self.__annotateX = 1.10 * self.__xMin
        if ( not newY == None ):
            self.__annotateY = newY
        else:
            self.__annotateY = 1.10 * self.__yMin
        if ( not annotation == None ):
            self.__annotation = annotation
        else:
            self.__annotation = self.__plotName

        self.printAnnotation()

    def printAnnotation(self):
        """Prints the annotation"""
        plt.annotate(self.__annotation,
        xy=(self.__annotateX, self.__annotateY),
        xycoords="data",
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=self.__annotationFont )



    def setGrid(self, showGrid=True, whichAxis='both', gridColor='0.9', gridStyle=':'):
        """Sets grid on the plot"""
        plt.grid(b=showGrid, which=whichAxis, color=gridColor, linestyle=gridStyle)


    def setTitle(self, newTitle=None):
        """Sets plot title"""

        # Print to user:
        if ( not newTitle == None ):
            self.__plotName = newTitle
            self.__write.message = "The plot will be titled \"%s\"." % (self.__plotName)
            self.__write.print(2, 3)

        # Set title:
        plt.title(self.__plotName, fontsize=self.__titleFont)


    def setXLabel(self, newLabel=None ):
        """Sets the X label for the plot object"""
        if ( not newLabel == None ):
            self.__xLabel = newLabel
        plt.xlabel( self.__xLabel, fontsize=self.__labelFont )


    def setYLabel(self, newLabel=None ):
        """Sets the Y label for the plot object"""
        if ( not newLabel == None ):
            self.__yLabel = newLabel
        plt.ylabel( self.__yLabel, fontsize=self.__labelFont )


    def setX(self):
        """Set X values (min, max) on the plot"""
        # Ensure limits are valid:
        if ( self.__xMin <= 0 ):
            self.__xMin = 0

        if ( self.__xMin >= self.__xMax ):
            if ( self.__xMin == 0 ):
                self.__xMax = 250
            else:
                self.__xMax = 1.25 * self.__xMin

        # Set new limits:
        plt.xlim(self.__xMin, self.__xMax)


    def xMin(self, newXVal = 0 ):
        """Sets minimum X value"""
        # Ensure positive and real:
        if ( newXVal < 0 ):
            newXVal = 0

        # Set value:
        self.__xMin = newXVal


        # Print to user:
        self.__write.message = "A new X min (%0.2f) will be used for this plot." % (self.__xMin)
        self.__write.print(2, 3)


        # Set limits:
        self.setX()


    def xMax(self, newXVal = 1000 ):
        """Sets maximum X value"""
        self.__xMax = newXVal


        # Print to user:
        self.__write.message = "A new X max (%0.2f) will be used for this plot." % (self.__xMax)
        self.__write.print(2, 3)

        # Set limits:
        self.setX()


    def setScale(self, xScale=None, yScale=None):
        """Sets scale on the axis (linear or log for X/Y)"""
        if ( not xScale == None ):
            self.__xScale = xScale
        if ( not yScale == None ):
            self.__yScale = yScale


        # Set X/Y scales:
        plt.xscale(self.__xScale)
        plt.yscale(self.__yScale)


    def setY(self):
        """Set Y values (min, max) on the plot"""
        # Ensure limits are valid:
        if ( self.__yMin <= 0 ):
            self.__yMin = 1.0E-10

        if ( self.__yMin >= self.__yMax ):
            if ( self.__yMin <= 0 ):
                self.__yMax = 1.0E+10
            else:
                self.__yMax = 1.0E3 * self.__yMin

        # Set new limits:
        plt.ylim(self.__yMin, self.__yMax)


    def yMin(self, newyVal = 1.0E-10 ):
        """Sets minimum Y value"""
        # Ensure positive and real:
        if ( newyVal < 0 ):
            newyVal = 1.0E-3

        # Set value:
        self.__yMin = newyVal


        # Print to user:
        self.__write.message = "A new Y min (%0.2e) will be used for this plot." % (self.__yMin)
        self.__write.print(2, 3)


        # Set limits:
        self.setY()


    def yMax(self, newYVal = 1.0E10 ):
        """Sets maximum Y value"""
        self.__yMax = newYVal


        # Print to user:
        self.__write.message = "A new Y max (%0.2e) will be used for this plot." % (self.__yMax)
        self.__write.print(2, 3)

        # Set limits:
        self.setY()


    def show(self, pauseTime=100):
        """Shows the plot"""
        plt.ion()
        plt.show()
        time.sleep( pauseTime )
        plt.close('all')


    def savePlot(self, figName="temp", figDPI = 1200, figBBox = 'tight', figPad=0.15):
        """Save the plot to a file"""
        # Write that plot is being saved
        ext = ".png"
        figName = fileModule.verifyFileName( figName, ext )
        self.__write.message = "The following figure is being saved as \"%s\"." % (figName)
        self.__write.print(2, 2)


        # Set plot details:
        self.setPlotDetails()


        # Save file:
        plt.savefig(figName, bbox_inches=figBBox, pad_inches=figPad, dpi = figDPI)


        # Show the saved file:
        self.show(3)
