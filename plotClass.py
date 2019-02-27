
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
# Use LaTeX as text editor:
plotlib.rcParams['text.usetex'] = True
plotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
# (font defaults)
defaultFont = 14
figureFont = 11
detaultAnnotationFont = 11
plotlib.rcParams.update({'font.size': figureFont})
plt.rc('font', **{'family': 'serif'})   # Which font to use
plt.rcParams['axes.labelweight'] = 'bold'
# Figure size:
figureHeight = 3.5
figureWidth  = 6.811
# For see-through images:
opacity = 0.6
# For when multiple types exist:
typeExpScaling = 2
surroundMainAnnotation = True


# Default scalings:
dynamicXScaling = 0.05   # Scale up/down for dynamic limits
dynamicYScaling = 0.05
useOwnHistPlot = True   # Uses a line for histogram plots




# For linestyle, color:
lineColors = [ 'blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', \
'gray', 'olive', 'cyan']
numColors = len( lineColors )
# Line styles:
lineStyles = ['--','-',':','-.']
numLineStyles = len(lineStyles)


class BaseFigure:
    """Contains the axis and figure for a plot"""
    __figure, __axis = plt.subplots()

    def __init__(self, newFigWidth = figureWidth, newFigHeigth = figureHeight):
        """Constructor for a figure object"""
        self.__figure, self.__axis = plt.subplots( figsize=(newFigWidth, newFigHeigth) )

        return



# Controls the Plot classes axis info:
class PlotLabeling(BaseFigure):
    """Controls axis labeling for a plot"""
    # General class control:
    __write = Print()
    # Fonts:
    __axisFont       = defaultFont
    __annotationFont = defaultFont
    __titleFont      = defaultFont + 2
    # Axis labeling (title, X/Y labels, fonts):
    __plotTitle = "Plot Title"
    __xLabel   = "X [Units]"
    __yLabel   = "Y [Units]"
    # In-plot annotations:
    __useBoldFont = True
    __boxAnnotation = True   # Includes a box around the annotation
    # (main annotation)
    __mainAnnotation = None
    __mainAnnotateX  = 0.0
    __mainAnnotateY  = 0.0
    # (secondary annotations)
    __otherAnnotations = []
    __otherAnnotateX   = []
    __otherAnnotateY   = []

    def __init__(self, newPlotTitle = None, newXLabel = None, newYLabel = None, useBoldFont = True, newPrint = Print() ):
        """Constructor for plot labeling object"""
        # General information:
        self.__write = newPrint

        # Reset all object members:
        self.__resetMembers()

        # Set constructor-specifiable variables:
        if ( not newPlotTitle == None ):
            self.__plotTitle = newPlotTitle
        if ( not newXLabel == None ):
            self.__xLabel = newXLabel
        if ( not newYLabel == None ):
            self.__yLabel = newYLabel
        self.__useBoldFont = useBoldFont

    def __resetMembers(self):
        """Resets all class member variables"""

        # Axis labeling (title, X/Y labels, fonts):
        self.__axisFont  = defaultFont
        self.__titleFont = defaultFont + 2
        self.__plotTitle = "Plot Title"
        self.__xLabel    = "X [Units]"
        self.__yLabel    = "Y [Units]"
        # In-plot annotations:
        self.__useBoldFont = True
        self.__boxAnnotation = True   # Includes a box around the annotation
        # (main annotation)
        self.__mainAnnotation = None
        self.__mainAnnotateX  = 0.0
        self.__mainAnnotateY  = 0.0
        # (secondary annotations)
        self.__otherAnnotations = []
        self.__otherAnnotateX   = []
        self.__otherAnnotateY   = []

    def __applyXLabel(self):
        """Sets the X-axis label"""
        super().__axis.set_xlabel( self.__xLabel, fontsize=self.__axisFont )
        return

    def __applyYLabel(self):
        """Sets the Y-axis label"""
        super().__axis.set_ylabel( self.__yLabel, fontsize=self.__axisFont )
        return

    def __applyPlotTitle(self):
        """Titles the plot title"""
        super().__axis.set_title( self.__plotName, fontsize=self.__titleFont )
        return

    def __applyMainAnnotation(self):
        """Prints the annotation"""
        # If annotation exists, create one (apply box if desired):
        if ( not self.__mainANnotation == None ):
            if ( self.__boxAnnotation ):
                plt.annotate(self.__mainAnnotation,
                xy=(self.__mainAnnotateX, self.__mainAnnotateY),
                xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                fontsize=self.__annotationFont, clip_on=True,
                bbox=dict(boxstyle="round", fc="1.0", ec="0.75", alpha=0.75) )
            else:
                plt.annotate(self.__mainAnnotation,
                xy=(self.__mainAnnotateX, self.__mainAnnotateY),
                xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                fontsize=self.__annotationFont, clip_on=True)

    def setXLabel(self, newXLabel = None):
        """Sets a new X Label"""
        if ( newXLabel == None ):
            self.__write.message = "Must pass a x-axis string to toggle the label."
            self.__write.print(1, 2)
        else:
            try:
                newXLabel = str(newXLabel)
            except:
                self.__write.message = "The passed in X label could not be converted to a string to be applied. Unable to use."
                self.__write.print(1, 2)
                newXLabel = self.__xLabel

            self.__xLabel = newXLabel

            # Apply bold font, if desired:
            if ( self.__useBoldFont ):
                self.__xLabel = "{\\bf" + self.__xLabel + "}"

        return

    def setYLabel(self, newYLabel = None):
        """Sets a new Y Label"""
        if ( newYLabel == None ):
            self.__write.message = "Must pass a y-axis string to toggle the label."
            self.__write.print(1, 2)
        else:
            try:
                newYLabel = str(newYLabel)
            except:
                self.__write.message = "The passed in Y label could not be converted to a string to be applied. Unable to use."
                self.__write.print(1, 2)
                newYLabel = self.__yLabel

            self.__yLabel = newYLabel

            # Apply bold font, if desired:
            if ( self.__useBoldFont ):
                self.__yLabel = "{\\bf" + self.__yLabel + "}"

        return

    def setPlotTitle(self, newPlotTitle = None):
        """Sets a new plot title to use"""
        if ( newPlotTitle == None ):
            self.__write.message = "Must pass a plot title string to toggle the plot's title."
            self.__write.print(1, 2)
        else:
            try:
                newPlotTitle = str(newPlotTitle)
            except:
                self.__write.message = "The passed in plot title could not be converted to a string for use. Unable to use."
                self.__write.print(1, 2)
                newPlotTitle = self.__plotTitle

            self.__plotTitle = newPlotTitle

            # Apply bold font, if desired:
            if ( self.__useBoldFont ):
                self.__plotTitle = "{\\bf" + self.__plotTitle + "}"

        return


    def setMainAnnotation(self, newAnnotation=None, xVal = None, yVal = None):
        """Sets the main annotation for the plot"""
        if ( newAnnotation == None ):
            self.__write.message = "No primary annotation text given. Cannot apply annotation."
            self.__write.print(1, 2)
            return

        return

    def annotateXY(self, annotation=None, newX=None, newY=None, fontSize = None):
        """Sets the X/Y of the annotation"""
        if ( not isinstance(annotation, str) ):
            self.__write.message = "First parameter to annotateXY function must of type 'str'. Converting to str type..."
            self.__write.print(1, 2)
            try:
                annotation = str( annotation )
            except:
                self.__write.message = "   Failed to convert annotation to text. No annotation will be printed."
                self.__write.print(1, 2)
                return
        self.__annotation = annotation
        if ( not newX == None ):
            try:
                newX = float(newX)
            except:
                newX = (1 + dynamicXScaling) * self.__xMin
            self.__annotateX = newX
        else:
            self.__annotateX = (1 + dynamicXScaling) * self.__xMin
        if ( not newY == None ):
            try:
                newY = float(newY)
            except:
                newY = (1 + dynamicYScaling) * self.__yMin
            self.__annotateY = newY
        else:
            self.__annotateY = (1 + dynamicYScaling) * self.__yMin
        if ( fontSize == None ):
            self.__annotationFont = detaultAnnotationFont
        else:
            try:
                fonSize = int(fontSize)
            except:
                fontSize = detaultAnnotationFont
            self.__annotationFont = fontSize

        if ( self.__boldText ):
            self.__annotation = "{\\bf " + self.__annotation + "}"


        self.printAnnotation()



    def labelPlot(self):
        """Applies the X/Y axis labels, plot title, and all annotations"""
        # X/Y/Title:
        self.__applyXLabel()
        self.__applyYLabel()
        self.__applyPlotTitle()
        # Annotations:
        self.__applyMainAnnotation()

        return


# Actual Plot class:
class Plot:
    """
    This is the plot class
    """
    # Class for printing messages:
    __write = Print()
    # General plot information:
    # X information
    __xScale = "linear"
    __xMin  = 0
    __xMax  = 250
    __dynamicXLimits = True
    __maxXPlotted = float("-inf")
    __minXPlotted = float("inf")
    # Y information
    __yScale = "symlog"
    __yMin  = 1.0E-10
    __yMax  = 1.0E+10
    __dynamicYLimits = True
    __maxYPlotted = float("-inf")
    __minYPlotted = float("inf")
    # Regarding annotation:
    __annotation = "?"
    __annotateX  = 1.10 * __xMin
    __annotateY  = 1.10 * __yMin
    __annotationFont = detaultAnnotationFont
    # Regarding legend information:
    __legendEntries = []
    __legendPos = "best"
    # Regarding plot information:
    __numPlots = 0
    __numTypes = 0
    __allowManyPlots = True
    __boldText = True
    __numPlottedLines = 0


    # Plot object stuff:
    __fig, __ax = plt.subplots( figsize=(figureWidth,figureHeight) )


    def __init__(self, newWidth = None, newHeight = None, allowManyPlots = True, newPrint=Print()):
        """Plot class constructor"""
        if ( newWidth == None ):
            newWidth = figureWidth
        if ( newHeight == None ):
            newHeight = figureHeight


        # Create figure and axis object:
        self.__fig, self.__ax = plt.subplots( figsize=(figureWidth,figureHeight) )

        # Set defaults:
        self.__write = Print()
        # General plot information:
        self.__labelFont = defaultFont
        self.__titleFont = self.__labelFont + 2
        self.__annotation = "?"
        self.__annotateX  = 1.10 * self.__xMin
        self.__annotateY  = 1.10 * self.__yMin
        self.__annotationFont = detaultAnnotationFont
        # X Information
        self.__xLabel = "?"
        self.__xScale = "linear"
        self.__xMin = 0
        self.__xMax = 250
        self.__dynamicXLimits = True
        self.__minXPlotted = float("inf")
        self.__maxXPlotted = float("-inf")
        # Y Information
        self.__yLabel = "?"
        self.__yScale = "symlog"
        if ( self.__yScale == "linear" ):
            self.__yMin = 0
            self.__yMax = 10
        else:
            self.__yMin = 1.0E-10
            self.__yMax = 1.0E+10
        self.__dynamicYLimits = True
        self.__minYPlotted = float("inf")
        self.__maxYPlotted = float("-inf")

        # Regarding plot information:
        self.__numPlots = 0
        self.__legendEntries = []
        self.__legendPos = "best"
        # Regarding the number of line "types" (various angles, etc.)
        self.__numTypes = 0
        self.allowsManyPlots( allowManyPlots )
        self.__boldText = True
        self.__numPlottedLines = 0


        # Set values passed in:
        self.__write = newPrint


        # Set plot details:
        self.setPlotDetails()

    def setPlotDetails(self):
        """Sets plot details"""
        # Set default plot values:
        self.setTitle()
        self.setXLabel()
        self.setYLabel()
        self.setGrid()
        self.setScale()
        self.setX()
        self.setY()

    def allowsManyPlots(self, allowed = True):
        """Changes value of self.__allowManyPlots to true to toggle many plots"""
        if ( not isinstance(allowed, bool) ):
            self.__write.message = "Toggling the allowance of many plot types accepts only boolean types. Turning many types on..."
            self.__write.print(1, 2)
            allowed = True

        # Ensure no data has been entered; if so, warn user that labels may be skewed.
        if ( not self.__numPlots == 0 ):
            self.__write.message = "Toggling the allowance of many plots should be done when no data has been specified for proper appearance."
            self.__write.print(1, 2)

        self.__allowManyPlots = allowed

    def addType(self):
        """Appends a new type for when many plots are used"""
        if ( self.__allowManyPlots ):
            self.__numTypes += 1
            # Rest number of plots for the type:
            self.__numPlots = 0
        else:
            self.__write.message = "Cannot add another plot type; specify prior to adding data."
            self.__write.print(1, 2)

    def setDynamicLimits(self, dynamicXLims = True, dynamicYLims = True):
        """Sets whether or not to use dynamic X/Y limits"""
        self.__dynamicXLimits = dynamicXLims
        self.__dynamicYLimits = dynamicYLims

    def setGrid(self, showGrid=True, whichAxis='both', gridColor='0.9', gridStyle=':'):
        """Sets grid on the plot"""
        self.__ax.minorticks_on()
        self.__ax.grid(b=showGrid, which=whichAxis, color=gridColor, linestyle=gridStyle, alpha=1)
    #    self.__ax.grid(b=showGrid, which='minor', color='0.6',     linestyle=gridStyle, alpha=0.2)

    def setTitle(self, newTitle=None):
        """Sets plot title"""

        # Print to user:
        if ( not newTitle == None ):
            self.__plotName = newTitle
            self.__write.message = "The plot will be titled \"%s\"." % (self.__plotName)
            self.__write.print(2, 3)

        if ( self.__boldText ):
            self.__plotName = "{\\bf " + self.__plotName + "}"

        # Set title:
        self.__ax.set_title(self.__plotName, fontsize=self.__titleFont)

    def setXLabel(self, newLabel=None ):
        """Sets the X label for the plot object"""
        if ( not newLabel == None ):
            self.__xLabel = newLabel

        if ( self.__boldText ):
            self.__xLabel = "{\\bf " + self.__xLabel + "}"

        self.__ax.set_xlabel( self.__xLabel, fontsize=self.__labelFont )

    def setYLabel(self, newLabel=None ):
        """Sets the Y label for the plot object"""
        if ( not newLabel == None ):
            self.__yLabel = newLabel

        if ( self.__boldText ):
            self.__yLabel = "{\\bf " + self.__yLabel + "}"

        self.__ax.set_ylabel( self.__yLabel, fontsize=self.__labelFont )

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
        if ( self.__dynamicXLimits and self.__numPlottedLines > 0 ):
            xMin = (1 - dynamicXScaling) * self.__minXPlotted
            if ( xMin < 0 ):
                xMin = 0
            xMax = (1 + dynamicXScaling) * self.__maxXPlotted
            if ( xMax <= xMin ):
                if ( xMin == 0 ):
                    xMax = 10
                else:
                    xMax = (1 + dynamicXScaling) * xMin
            print("Dynamic X:", xMin, xMax)
            self.__ax.set_xlim(xMin, xMax)
        else:
            self.__ax.set_xlim(self.__xMin, self.__xMax)

    def xMin(self, newXVal = 0 ):
        """Sets minimum X value"""
        # Set value:
        self.__xMin = newXVal
        self.__dynamicXLimits = False


        # Print to user:
        self.__write.message = "A new X min (%0.2f) will be used for this plot. Dynamic X is off." % (self.__xMin)
        self.__write.print(2, 3)


        # Set limits:
        self.setX()

    def xMax(self, newXVal = 1000 ):
        """Sets maximum X value"""
        self.__xMax = newXVal
        self.__dynamicXLimits = False


        # Print to user:
        self.__write.message = "A new X max (%0.2f) will be used for this plot. Dynamic X is off." % (self.__xMax)
        self.__write.print(2, 3)

        # Set limits:
        self.setX()

    def setScale(self, xScale=None, yScale=None):
        """Sets scale on the axis (linear or log for X/Y)"""
        __subXTicks = [5]
        __subYTicks = [2, 3, 4, 5, 6, 7, 8, 9]
        if ( not xScale == None ):
            self.__xScale = xScale
        if ( not yScale == None ):
            self.__yScale = yScale


        # Set X/Y scales:
        self.__ax.set_xscale(self.__xScale, subsx=__subXTicks)
        # Setting of yscale here makes smallest Y as 10^0 (insufficient)
        # self.__ax.set_yscale(self.__yScale, subsy=__subYTicks, nonposy='clip')

    def setY(self):
        """Set Y values (min, max) on the plot"""
        # Ensure limits are valid:
        if ( self.__yScale == "log" or self.__yScale == "symlog" ):
            if ( self.__yMin <= 0 ):
                self.__yMin = 1.0E-10
        else:
            if ( self.__yMin <= 0 ):
                self.__yMin = 0

        if ( self.__yMin >= self.__yMax ):
            if ( self.__yMin <= 0 ):
                self.__yMax = 1.0E+10
            else:
                self.__yMax = 1.0E3 * self.__yMin

        # Set new limits:
        if ( self.__dynamicYLimits and self.__numPlottedLines > 0 ):
            yMin = (1 - dynamicYScaling) * self.__minYPlotted
            if ( yMin < 0 ):
                yMin = 0
            yMax = (1 + dynamicYScaling) * self.__maxYPlotted
            if ( yMax <= yMin ):
                if ( yMin == 0 ):
                    yMax = 10
                else:
                    yMax = (1 + dynamicYScaling) * yMin
            print("Dynamic Y:", yMin, yMax)
            self.__ax.set_ylim(yMin, yMax)
        else:
            self.__ax.set_ylim(self.__yMin, self.__yMax)

    def yMin(self, newyVal = 1.0E-10 ):
        """Sets minimum Y value"""
        # Set value:
        self.__yMin = newyVal
        self.__dynamicYLimits = False


        # Print to user:
        self.__write.message = "A new Y min (%0.2e) will be used for this plot. Dynamic Y is off." % (self.__yMin)
        self.__write.print(2, 3)


        # Set limits:
        self.setY()

    def yMax(self, newYVal = 1.0E10 ):
        """Sets maximum Y value"""
        self.__yMax = newYVal
        self.__dynamicYLimits = False


        # Print to user:
        self.__write.message = "A new Y max (%0.2e) will be used for this plot. Dynamic Y is off." % (self.__yMax)
        self.__write.print(2, 3)

        # Set limits:
        self.setY()

    def legendPos(self, loc = "best", xStart = None, yStart = None ):
        """Sets position of legend"""
        # Default values (minimum for uniqueness)
        __uniqueLOC = ['b', 'upper r', 'upper l', 'lower l',
        'lower r', 'r', 'center l', 'center r', 'lower c',
        'upper c']
        # Full named values (ensures "LOC" is always valid)
        __validLOC = ['best', 'upper right', 'upper left', 'lower left',
        'lower right', 'right', 'center left', 'center right', 'lower center',
        'upper center', 'center']
        # For using coordinate values
        __coordinateFlag = "co"
        __defaultLOC = "best"


        # Reduced LOC (location)
        loc = loc.strip().lower()

        # Validate argument:
        validArgument = False
        for i in range(0, len(__validLOC), 1):
            if ( loc[ : len(__uniqueLOC[i]) ] == __uniqueLOC[i] ):
                loc = __validLOC[i]
                validArgument = True
                break

        # Set legend location:
        if ( validArgument ):
            self.__legendPos = loc
        elif ( loc[ : len(__coordinateFlag)] == __coordinateFlag ):
            # Use X/Y Position instead; ensure X/Y combo will appear in axis:
            if ( xStart < self.__xMin ):
                xStart = self.__xMin
            elif ( xStart > self.__xMax ):
                xStart = self.__xMax
            if ( yStart < self.__yMin ):
                yStart = self.__yMin
            elif ( yStart > self.__yMax ):
                yStart = self.__yMax

            self.__legendPos = (xStart, yStart)

        else:
            # Bad argument; assume "best" is used
            self.__write.message = "Bad legend position flag given. Assuming 'best'."
            self.__write.print(1, 3)
            loc = __defaultLOC
            self.__legendPos = loc

    def __setPlottedX(self, xValues):
        """Sets the min/max x values plotted in the class"""
        if ( not isinstance(xValues, list) ):
            self.__write.message = "The values must be a list. Cannot determine min/max plotted X values. Dynamic limits will be turned off."
            self.__write.print(1, 3)
            self.__dynamicXLimits = False
            return

        # Find min/max:
        for i in range(0, len(xValues), 1):
            self.__minXPlotted = min( self.__minXPlotted, xValues[i] )
            self.__maxXPlotted = max( self.__maxXPlotted, xValues[i] )

    def __setPlottedY(self, yValues):
        """Sets the min/max y values plotted in the class"""
        if ( not isinstance(yValues, list) ):
            self.__write.message = "The values must be a list. Cannot determine min/max plotted Y values. Dynamic limits will be turned off."
            self.__write.print(1, 3)
            self.__dynamicYLimits = False
            return

        # Find min/max:
        tempMin, temp2Min = float("inf"), float("inf")
        for i in range(0, len(yValues), 1):
            if ( self.__yScale == "log" or self.__yScale == "symlog" ):
                if ( yValues[i] < tempMin ):
                    temp2Min = tempMin
                    tempMin = yValues[i]
                elif ( (yValues[i] < temp2Min) and (not yValues[i] == tempMin)):
                    temp2Min = yValues[i]
            else:
                temp2Min = min( temp2Min, yValues[i] )
            self.__maxYPlotted = max( self.__maxYPlotted, yValues[i] )

        self.__minYPlotted = min( self.__minYPlotted, temp2Min)

    def lineColor(self):
        """Returns the line color to be used"""
        return lineColors[ self.__numTypes % numColors ]

    def lineStyle(self):
        """Returns the line style to be used"""
        return lineStyles[ self.__numPlots % numLineStyles ]

    def annotateLine(self, annotation = None, xVal = None, yVal = None, textColor = None):
        """Adds an annotation to the end of the line, or where requested by user (depending on dynamic X/Y)"""
        if ( annotation == None ):
            annotation = self.__legendEntries[len(self.__legendEntries)-1]
            self.__write.message = "No annotation text given to annotate line with. Using last line label (\"%s\")." % ( annotation )
            self.__write.print(1, 2)

        if ( xVal == None ):
            # Use dynamic X or a little less than requested x value:
            if ( self.__dynamicXLimits ):
                xVal = (1 - dynamicXScaling) * self.__maxXPlotted
            else:
                xVal = (1 - dynamicXScaling) * self.__xMax
        elif ( xVal < 0 ):
            xVal = abs(xVal)

        if ( yVal == None ):
            # Use dynamic X or a little less than requested x value:
            if ( self.__dynamicXLimits ):
                yVal = (1 - dynamicYScaling) * self.__maxYPlotted
            else:
                yVal = (1 - dynamicYScaling) * self.__yMax
        else:
            if ( yVal < 0 ):
                yVal = abs(yVal)

        if ( textColor == None ):
            textColor = self.lineColor()

        if ( self.__boldText ):
            annotation = "{\\bf " + annotation + "}"

        # Now create annotation:
        self.__ax.annotate(annotation,
        xy=(xVal, yVal),
        xycoords="data",
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=self.__annotationFont,
        color = textColor,
        alpha= opacity, clip_on=True )


    # For adding plots:
    def addHistogram(self, myBins, myValues, myLabel = "No label given", xScale = 1, yScale = 1):
        """Adds a histogram to the plot"""
        # Ensure scaling is >0:
        if ( xScale <= 0 ):
            xScale = 1
        if ( yScale <= 0 ):
            yScale = 1

        # Validate histogram data:
        if ( myBins[0] < 0 ):
            shift = -myBins[0]
            self.__write.message = "Histogram bins values will be shifted up by (%f) to ensure physicality." % (shift)
            self.__write.print(2, 2)
        else:
            shift = 0
        for i in range(0, len(myBins), 1):
            myBins[i] += shift
            myBins[i] *= xScale
        if ( myValues[0] < 0 ):
            shift = -myValues[0]
            self.__write.message = "Histogram bins values will be shifted up by (%f) to ensure physicality." % (shift)
            self.__write.print(2, 2)
        else:
            shift = 0
        for i in range(0, len(myValues), 1):
            myValues[i] += shift
            myValues[i] *= yScale

        # Determine the last value that has non-zero entry:
        lastValueIndx = len(myValues) - 1
        for i in range(0, lastValueIndx, 1):
            if ( not myValues[lastValueIndx-i] <= 0 ):
                lastValueIndx = lastValueIndx-i
                break

        # Use the minimum number of applicable data points:
        numValidData = min( lastValueIndx, len(myBins)-1 )

        plottedBins   = []
        plottedValues = []
        plottedBins.append( myBins[0] )
        for i in range(0, numValidData, 1):
            # Ensure positive (or non-zero) bin widths:
            if ( myBins[i+1] < myBins[i] ):
                self.__write.message = "In Plot class: Negative bin-width is not valid (range=[%.2f, %.2f). Using bin width of 0." % (myBins[i], myBins[i+1])
                self.__write.print(1, 2)
                myBins[i+1] = myBins[i]
            plottedBins.append( myBins[i+1] )

            # Ensure positive values:
            if ( myValues[i] < 0 ):
                myValues[i] = 0
                self.__write.message = "Values for histogram bins cannot be negative. Using value of (%f)." % (myValues[i])
                self.__write.print(1, 2)
            plottedValues.append( myValues[i] )

        # Obtain min/max X/Y:
        self.__setPlottedX( plottedBins )
        self.__setPlottedY( plottedValues )

        if ( not useOwnHistPlot ):
            # Plot histogram:
            self.__ax.hist(plottedValues, bins=plottedBins, histtype='step', color=self.lineColor())
            if ( self.__numTypes == 0 ):
                self.__legendEntries.append( myLabel )
            self.__numPlots += 1
            self.__numPlottedLines += 1
        else:
            # Create new X/Y values to emulate the look of a histogram (i.e. 2 Y values per X value, except at edges)
            xVals = []
            yVals = []

            # Left edge of first bin:
            xVals.append( plottedBins  [0] )
            yVals.append( plottedValues[0] )
            for i in range(1, len(plottedValues), 1):
                # Right edge of current bin:
                xVals.append( plottedBins  [i    ] )
                yVals.append( plottedValues[i - 1] )

                # Left edge of next bin:
                xVals.append( plottedBins  [i    ] )
                yVals.append( plottedValues[i    ] )

            xVals.append( plottedBins  [len(plottedBins  )-1] )
            yVals.append( plottedValues[len(plottedValues)-1] )

            # Now plot as a line:
            self.addLine(xVals, yVals, myLabel, xScale, yScale)

    def addLine(self, xVals, yVals, myLabel = "No label given", xScale = 1, yScale = 1):
        """Adds a line to the plot"""
        # Ensure scaling is >0:
        if ( xScale <= 0 ):
            xScale = 1
        if ( yScale <= 0 ):
            yScale = 1

        # Verify x/y coords. are lists:
        if ( not isinstance(xVals, list) or not isinstance(yVals, list) ):
            validXY = False
            self.__write.message = "X and Y coordinates for lines must be lists. Cannot add line..."
            self.__write.print(1, 2)
            return

        # Verify all values are physical (>0):
        xShift = 0
        yShift = 0
        for i in range(0, len(xVals), 1):
                xShift = min(xShift, xVals[i])   # Obtain miniminum x value in set:
        for i in range(0, len(yVals), 1):
                yShift = min(yShift, yVals[i])   # Obtain minimum y value in set:

        # Make shifts positive, warn user if shifting:
        xShift = abs(xShift)
        yShift = abs(yShift)
        if ( xShift > 0 or yShift > 0 ):
            self.__write.message = "The X/Y coordinates of the line will be shifted by %.2f and %.2f, respectively, to keep all values positive." % (xShift, yShift)
            self.__write.print(1, 2)
        # Shift values:
        for i in range(0, len(xVals), 1):
            xVals[i] += xShift
        for i in range(0, len(yVals), 1):
            yVals[i] += yShift

        # Determine the last value that has non-zero entry:
        lastValueIndx = len(yVals) - 1
        for i in range(0, lastValueIndx, 1):
            if ( not yVals[lastValueIndx-i] <= 0 ):
                lastValueIndx = lastValueIndx-i
                break

        # For multiple types, scale:
        yScaleFactor = -self.__numTypes * typeExpScaling
        yScale = yScale * pow(10, yScaleFactor)
        if ( self.__numTypes > 0 ):
            self.__write.message = "Sim. data for \"%s\" is being scaled by 10^(%.1f) for clarity." % (myLabel, yScaleFactor)
            self.__write.print(2, 2)

        # Obtain x/y set for as many pairs between X/Y coords:
        xCoord = []
        yCoord = []
        numPairs = min( len(xVals), len(yVals), lastValueIndx )
        if ( numPairs <= 0 ):
            self.__write.message = "No data passed in to create a line plot. No plot will be created."
            self.__write.print(1, 2)
            return
        for i in range(0, numPairs, 1):
            xCoord.append( xScale * xVals[i] )
            yCoord.append( yScale * yVals[i] )


        # Obtain min/max X/Y:
        self.__setPlottedX( xCoord )
        self.__setPlottedY( yCoord )

        # X/Y values are all valid, as well as scaling factors; create line:
        if ( self.__yScale == "log" or "symlog" ):
            self.__ax.semilogy( xCoord, yCoord,
            linestyle=self.lineStyle(), color = self.lineColor(), alpha= opacity )
        else:
            self.__ax.plot( xCoord, yCoord,
            linestyle=self.lineStyle(), color = self.lineColor(), alpha= opacity )

        # Add plot and legend entry:
        if ( self.__numTypes == 0 ):
            self.__legendEntries.append( myLabel )
        self.__numPlots += 1
        self.__numPlottedLines += 1


    # For finishing a plot:
    def __finalizePlot(self):
        """Finalizes the plot axis and behaviors"""
        self.setPlotDetails()
        self.__ax.legend(self.__legendEntries, loc=self.__legendPos)

    def showCurrent(self, pauseTime=100):
        """Shows the plot"""
        if ( self.__numPlottedLines <= 0 ):
            # No plots or types created; warn client
            self.__write.message = "Plot contains no lines. Plot will not be saved."
            self.__write.print(1, 2)
            return

        plt.ion()
        plt.show()
        time.sleep( pauseTime )
        plt.close('all')

    def savePlot(self, figName="temp", figDPI = 300, overrideExisting=False, figBBox = 'tight', figPad=0.15, showPlot = False):
        """Save the plot to a file"""

        # Set plot details:
        self.__finalizePlot()


        if ( self.__numPlottedLines <= 0 ):
            # No plots or types created; warn client
            self.__write.message = "Plot contains no lines. Plot will not be saved."
            self.__write.print(1, 2)
            return


        if ( figDPI > 1200 ):
            figDPI = 1200
        elif ( figDPI < 300 ):
            figDPI = 300


        # Write that plot is being saved
        ext = ".png"
        figName = fileModule.verifyFileName( figName, ext, overrideExisting )
        self.__write.message = "The figure is being saved as \"%s\"." % (figName)
        self.__write.print(2, 2)


        # Save file:
        plt.savefig(figName, bbox_inches=figBBox, pad_inches=figPad, dpi = figDPI)


        # Show the saved file:
        if ( showPlot ):
            self.showCurrent(3)
