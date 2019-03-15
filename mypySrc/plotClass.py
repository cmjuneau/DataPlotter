
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
_defaultFontSize = 11
__figureFont = _defaultFontSize
plotlib.rcParams['text.usetex'] = True
plotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
plotlib.rcParams.update({'font.size': __figureFont})
plt.rc('font', **{'family': 'serif'})   # Which font to use
plt.rc('axes', axisbelow=True)


# Contains the figure and axis objects to use when plotting
class _BaseFigure:
    """The \"_BaseFigure\" object contains the figure and axis object to be used
    when creating a plot. The object is intended to be inhereted by the
    _PlotLabeling, _AxisLimits, and Plot objects.

    No other clients should use this class when plotting
    \t(although they may if other features are desired).
    ----------------------------------------------------------------------------

    """
    __defaultWidth  = 6.811
    __defaultHeigth = 3.5
    __write = Print()

    def __init__(self, newFigWidth = __defaultWidth, newFigHeigth = __defaultHeigth):
        """Constructor for a figure object"""
        if ( newFigWidth <= 0 ):
            newFigWidth = __defaultWidth
        if ( newFigHeigth <= 0 ):
            newFigHeigth = __defaultHeigth
        self.__figure, self.__axis = plt.subplots( figsize=(newFigWidth, newFigHeigth) )

        return

    def __del__(self):
        """Destructor for the object"""
        return


# Controls the Plot classes axis info (labels, titles, annotations)
class _PlotLabeling(_BaseFigure):
    """The \"_PlotLabeling\" object is intended to control the axis labels
    (x label, y label, plot title) and all annotations.

    Two types of annotations exist in this object: a "main" and "others".
    Only one main annotation may exist, and as many as desired "other"
    annotations may exist. Annotations default to black; only "other" annotations
    may have their text color modified from the default.
    -Other annotations are included here to allow users to easily and quickly
    \tplace annotations for specifc sets of lines when printing multiple plots on
    \ta single plot, similar to a legend (however more customizable and movable).
    -Annotations are allowed to be draggable, and they may be clipped by the axes
    \tlimits, preventing them from being seen.

    The object utilizes LaTeX font (the amsmath package is loaded).
    \tClients/users have the option to turn on BOLD LaTeX font, where all labels
    \tand annotations are made bold.

    All annotations utilize the XY limits of the axis for placement.

    Accessible Member Functions ( Purpose ):
    -setXLabel            ( Sets the X-axis label that will be utilized )
    -setYLabel            ( Sets the Y-axis label that will be utilized )
    -setPlotTitle         ( Sets the plot title that will be utilized )
    -setMainAnnotation    ( Modifies the main annotation and position )
    -addOtherAnnotation   ( Adds an annotation of "other" type )
    -labelPlot            ( Applies all axis labels [x, y, title] and annotations )
    ----------------------------------------------------------------------------

    """
    # Default annotation locations (note: defaults don't conflict with axes scales):
    __defaultXAnnotation = float(1.0E-4)
    __defaultYAnnotation = float(1.0E-4)
    __colors = dict(plotlib.colors.BASE_COLORS, **plotlib.colors.CSS4_COLORS)
    __defaultAnnotationColor = "black"
    # Fonts (used for each class)
    __axisFont       = _defaultFontSize
    __annotationFont = _defaultFontSize
    __titleFont      = _defaultFontSize + 2

    def __init__(self, newPlotTitle = None, newXLabel = None, newYLabel = None, useBoldFont = True, newPrint = Print() ):
        """Constructor for plot labeling object"""

        # Construct parent class(es):
        super(_PlotLabeling, self).__init__( )

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

        return

    def __del__(self):
        """Class destructor"""
        self.__resetMembers()
        return

    def __resetMembers(self):
        """Resets all class member variables"""

        # Axis labeling (title, X/Y labels, fonts):
        self.__xLabel    = "X [Units]"
        self.__yLabel    = "Y [Units]"
        self.__plotTitle = "Plot Title"
        # In-plot annotations:
        self.__useBoldFont   = True   # Makes all text bold (axis labels, plot title, annotations)
        # (main annotation)
        self.__boxMainAnnotation = True   # Includes a box around the annotation
        self.__mainAnnotation = None
        self.__mainAnnotateX  = self.__defaultXAnnotation
        self.__mainAnnotateY  = self.__defaultXAnnotation
        self.__mainAnnotateColor = self.__defaultAnnotationColor
        # (secondary annotations)
        self.__boxOtherAnnotation  = True
        self.__useBoldFontOther = False
        self.__otherAnnotations    = []
        self.__otherAnnotateX      = []
        self.__otherAnnotateY      = []
        self.__otherAnnotateColor  = []
        self.__numOtherAnnotations = 0

        return

    def __applyXLabel(self):
        """Sets the X-axis label"""
        xLabel = self.__xLabel

        if ( self.__useBoldFont ):
            xLabel = "{\\bf " + xLabel + "}"

        self._BaseFigure__axis.set_xlabel( xLabel, fontsize=self.__axisFont )
        return

    def __applyYLabel(self):
        """Sets the Y-axis label"""
        yLabel = self.__yLabel

        if ( self.__useBoldFont ):
            yLabel = "{\\bf " + yLabel + "}"

        self._BaseFigure__axis.set_ylabel( yLabel, fontsize=self.__axisFont )
        return

    def __applyPlotTitle(self):
        """Titles the plot title"""
        title = self.__plotTitle

        if ( self.__useBoldFont ):
            title = "{\\bf " + title + "}"

        self._BaseFigure__axis.set_title( title, fontsize=self.__titleFont )
        return

    def __applyMainAnnotation(self):
        """Prints the main annotation if it exists"""
        if ( not self.__mainAnnotation == None ):

            theAnnotation = self.__mainAnnotation

            # Apply bold if desired:
            if ( self.__useBoldFont ):
                theAnnotation = "{\\bf " + theAnnotation + "}"

            if ( self.__boxMainAnnotation ):
                thisAnnotation = self._BaseFigure__axis.annotate(theAnnotation,
                xy=(self.__mainAnnotateX, self.__mainAnnotateY),
                xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                fontsize=self.__annotationFont, clip_on=True, color=self.__mainAnnotateColor,
                bbox=dict(boxstyle="round", fc="0.98", ec="0.75", alpha=0.75) )
            else:
                thisAnnotation = self._BaseFigure__axis.annotate(theAnnotation,
                xy=(self.__mainAnnotateX, self.__mainAnnotateY),
                xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                fontsize=self.__annotationFont, clip_on=True, color=self.__mainAnnotateColor)

            thisAnnotation.draggable()

        return

    def __applyOtherAnnotations(self):
        """Prints all other annotations if they exist"""
        if( self.__numOtherAnnotations > 0 ):
            for i in range(0, self.__numOtherAnnotations, 1):

                theAnnotation = self.__otherAnnotations[i]

                if ( self.__useBoldFontOther ):
                    theAnnotation = "{\\bf " + theAnnotation + "}"

                if ( self.__boxOtherAnnotation ):
                    thisAnnotation = self._BaseFigure__axis.annotate(theAnnotation,
                    xy=(self.__otherAnnotateX[i], self.__otherAnnotateY[i]),
                    xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                    fontsize=self.__annotationFont, clip_on=True, color=self.__otherAnnotateColor[i],
                    bbox=dict(boxstyle="round", fc="1.0", ec="0.75", alpha=0.60) )
                else:
                    thisAnnotation = self._BaseFigure__axis.annotate(theAnnotation,
                    xy=(self.__otherAnnotateX[i], self.__otherAnnotateY[i]),
                    xycoords="data", horizontalalignment="left", verticalalignment="bottom",
                    fontsize=self.__annotationFont, clip_on=True, color=self.__otherAnnotateColor[i])

                thisAnnotation.draggable()

        return

    def setXLabel(self, newXLabel = None):
        """Sets a new X Label"""
        if ( newXLabel is None ):
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

        return

    def setYLabel(self, newYLabel = None):
        """Sets a new Y Label"""
        if ( newYLabel is None ):
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

        return

    def setPlotTitle(self, newPlotTitle = None):
        """Sets a new plot title to use"""
        if ( newPlotTitle is None ):
            self.__write.message = "Must pass a plot title string to toggle the plot's title."
            self.__write.print(1, 2)
        else:
            if ( not isinstance(newPlotTitle, str) ):
                try:
                    newPlotTitle = str(newPlotTitle)
                except:
                    self.__write.message = "The passed in plot title could not be converted to a string for use. Unable to use."
                    self.__write.print(1, 2)
                    newPlotTitle = self.__plotTitle

            self.__plotTitle = newPlotTitle

        return

    def setMainAnnotation(self, newAnnotation=None, xVal = None, yVal = None):
        """Sets the main annotation for the plot"""
        if ( newAnnotation is None ):
            self.__write.message = "No primary annotation text given. Cannot apply annotation."
            self.__write.print(1, 2)
            return

        # Ensure arguments are valid:
        if ( not isinstance(newAnnotation, str) ):
            try:
                newAnnotation = str(newAnnotation)
            except:
                self.__write.message = "Could not create a primary annotation from given argument. The annotation will not be printed."
                self.__write.print(1, 2)
                return

        if ( xVal is not None ):
            if ( isinstance(xVal, (int, float)) ):
                xVal = float(xVal)
            else:
                # Attempt to create a float from the argument:
                try:
                    xVal = float(xVal)
                except:
                    xVal = self.__defaultXAnnotation
                    self.__write.message = "Could not determine a x-value for the primary annotation. Using value of %.2f." % (xVal)
                    self.__write.print(1, 2)
        else:
            xVal = self.__defaultXAnnotation

        if ( yVal is not None ):
            if ( isinstance(yVal, (int, float)) ):
                yVal = float(yVal)
            else:
                # Attempt to create a float from the argument:
                try:
                    yVal = float(yVal)
                except:
                    yVal = self.__defaultYAnnotation
                    self.__write.message = "Could not determine a y-value for the primary annotation. Using value of %.2f." % (yVal)
                    self.__write.print(1, 2)
        else:
            yVal = self.__defaultYAnnotation

        # Set annotation variables:
        self.__mainAnnotation = newAnnotation
        self.__mainAnnotateX  = xVal
        self.__mainAnnotateY  = yVal

        return

    def addOtherAnnotation(self, newAnnotation=None, xVal = None, yVal = None, newColor = None):
        """Adds a secondary annotation to the plot"""
        if ( newAnnotation is None ):
            self.__write.message = "No secondary annotation text given. Cannot apply annotation."
            self.__write.print(1, 2)
            return

        # Ensure arguments are valid:
        if ( not isinstance(newAnnotation, str) ):
            try:
                newAnnotation = str(newAnnotation)
            except:
                self.__write.message = "Could not create a secondary annotation from given argument. The annotation will not be printed."
                self.__write.print(1, 2)
                return

        if ( xVal is not None ):
            if ( isinstance(xVal, (int, float)) ):
                xVal = float(xVal)
            else:
                # Attempt to create a float from the argument:
                try:
                    xVal = float(xVal)
                except:
                    xVal = self.__defaultXAnnotation
                    self.__write.message = "Could not determine a x-value for the secondary annotation. Using value of %.2f." % (xVal)
                    self.__write.print(1, 2)
        else:
            xVal = self.__defaultXAnnotation

        if ( yVal is not None ):
            if ( isinstance(yVal, (int, float)) ):
                yVal = float(yVal)
            else:
                # Attempt to create a float from the argument:
                try:
                    yVal = float(yVal)
                except:
                    yVal = self.__defaultYAnnotation
                    self.__write.message = "Could not determine a y-value for the secondary annotation. Using value of %.2f." % (yVal)
                    self.__write.print(1, 2)
        else:
            yVal = self.__defaultYAnnotation

        if ( newColor is None ):
            newColor = self.__defaultAnnotationColor
        else:
            if ( newColor not in self.__colors ):
                self.__write.message = "Annotation color not supported: %s" % (newColor)
                self.__write.print(1, 2)
                newColor = self.__defaultAnnotationColor
                self.__write.message = "   The color \"%s\" will be used instead." % (newColor)
                self.__write.print(1, 2)


        # Set annotation variables:
        self.__otherAnnotations.append( newAnnotation )
        self.__otherAnnotateX.append( xVal )
        self.__otherAnnotateY.append( yVal )
        self.__otherAnnotateColor.append( newColor )
        self.__numOtherAnnotations += 1

        return

    def labelPlot(self):
        """Applies the X/Y axis labels, plot title, and all annotations"""
        # X/Y/Title:
        self.__applyXLabel()
        self.__applyYLabel()
        self.__applyPlotTitle()
        # Annotations:
        self.__applyMainAnnotation()
        self.__applyOtherAnnotations()

        return


# Controls the Plot class's axis limits and scale
class _AxisLimits(_BaseFigure):
    """The \"_AxisLimits\" object is used to control the X/Y limits on the axis
    and the scales applied (linear, log, or symlog allowed).

    This object defaults to use dynamic axes, meaning it will auto-scale its
    \taxis based on the value that are plotted, should the user/client update the
    \tdynamicX/Y values.

    Accessible Member Functions ( Purpose ):
    -setXScale         ( Sets scale of the X-axis, being linear, log, or symlog [logit not allowed] )
    -setYScale         ( Sets scale of the Y-axis, being linear, log, or symlog [logit not allowed] )
    -setXLims          ( Allows user to specify X-axis bounds [low, high]; dynamic X-axis is turned off )
    -setYLims          ( Allows user to specify Y-axis bounds [low, high]; dynamic Y-axis is turned off )
    -updateDynamicX    ( Given a list of X-values, determine the lowest and largest valid values [different by scale type] )
    -updateDynamicY    ( Given a list of X-values, determine the lowest and largest valid values [different by scale type] )
    -applyAxisLimits   ( Applies the X/Y scale, X/Y axis range [based on dynamicX/Y or user specified], and the grid )
    ----------------------------------------------------------------------------

    """
    __infinity = float("inf")
    __defaultUpperLim = float(100.00)
    # For X/Y scales and the associated limits allowed:
    __validScales = ("linear", "log", "symlog")
    __lowestLinScaleValueAllowed = float(0.00)
    __lowestLogScaleValueAllowed = float(1.0E-20)
    # For dynamicall scaling X/Y axes
    __dynamicXScalingFrac = 0.10
    __dynamicYScalingFrac = 0.10

    def __init__(self, newDynamicX = True, newDynamicY = True, newPrint = Print()):
        """Constructor for the axis limits class"""

        # Construct parent class(es):
        super(_AxisLimits, self).__init__()

        # Set main values and defaults:
        self.__write = newPrint
        self.__resetMembers()

        # Apply constructor specific values:
        if ( isinstance(newDynamicX, bool) ):
            self.__dynamicX = newDynamicX
        else:
            self.__write.message = "A boolean type must be passed in to toggle dynamic X-axis. Defaulting to %b." % (self.__dynamicX)
            self.__write.print(1, 2)
        if ( isinstance(newDynamicY, bool) ):
            self.__dynamicY = newDynamicY
        else:
            self.__write.message = "A boolean type must be passed in to toggle dynamic Y-axis. Defaulting to %b." % (self.__dynamicY)
            self.__write.print(1, 2)

        return

    def __del__(self):
        """Class destructor; this function resets all values in the class"""
        self.__resetMembers()

        return

    def __resetMembers(self):
        """Resets all class members to their original value"""
        # For X/Y scale:
        self.__xScale = "linear"
        self.__yScale = "log"

        # For dynamic axis:
        # (X)
        self.__dynamicX = True
        self.__minDynamicX = self.__infinity
        self.__maxDynamicX = -self.__infinity
        # (Y)
        self.__dynamicY = True
        self.__minDynamicY = self.__infinity
        self.__maxDynamicY = -self.__infinity

        # For tradiational limits:
        self.__minX = self.__lowestLinScaleValueAllowed
        self.__maxX = self.__defaultUpperLim
        self.__minY = self.__lowestLinScaleValueAllowed
        self.__maxY = self.__defaultUpperLim

        return

    def __validateLimits(self, lowVal, highVal, axisScale):
        """Ensures that the lower limit is smaller than the larger limit"""

        # Obtain a lowest value allowed (protects for log-type axis)
        if ( axisScale == self.__validScales[0] ):
            lowestValAllowed = self.__lowestLinScaleValueAllowed
            axis = "X-axis"
        elif ( (axisScale == self.__validScales[1]) or (axisScale == self.__validScales[2]) ):
            axis = "Y-axis"
            if ( lowVal < self.__infinity ):
                lowestValAllowed = max(lowVal, self.__lowestLogScaleValueAllowed)
            else:
                lowestValAllowed = self.__lowestLogScaleValueAllowed
        else:
            self.__write.print(3, 2)
            self.__write.message = "Invalid axis scale (\"%s\") was detected for validating limits. Assuming log scale..." % (axisScale)
            self.__write.print(1, 2)
            axis = "Y-axis"
            if ( lowVal < self.__infinity ):
                lowestValAllowed = max(lowVal, self.__lowestLogScaleValueAllowed)
            else:
                lowestValAllowed = self.__lowestLogScaleValueAllowed

        # Validate lower limit (0 <= Val < INF)
        if ( not abs(lowVal) < self.__infinity ):
            self.__write.print(3, 2)
            self.__write.message = "Lower limit (%.4E) for the %s is invalid." % (lowVal, axis)
            self.__write.print(1, 2)
            lowVal = lowestValAllowed
            self.__write.message = "   Using lower limit of %.4E for the %s instead." % (lowVal, axis)
            self.__write.print(1, 2)

        # Validate lower limit (0 <= Val < INF)
        if ( lowVal < lowestValAllowed ):
            self.__write.print(3, 2)
            self.__write.message = "Lower limit of %.4E is invalid for the %s (\"%s\")." % (lowVal, axis, axisScale)
            self.__write.print(1, 2)
            lowVal = lowestValAllowed
            self.__write.message = "   Using limit of %.4E instead for the %s." % (lowVal, axis)
            self.__write.print(1, 2)

        # Valid largest value:
        if ( highVal <= lowVal ):
            self.__write.print(3, 2)
            self.__write.message = "Upper limit of %.3E is too small (low limit is %.3E) for the %s." % (highVal, lowVal, axis)
            self.__write.print(1, 2)
            if ( lowVal > lowestValAllowed ):
                highVal = 1.10 * lowVal
            else:
                highVal = self.__defaultUpperLim
            self.__write.message = "   Using upper limit of %.3E for the %s instead." % (highVal, axis)
            self.__write.print(1, 2)

        return lowVal, highVal

    def __applyGrid(self, showGrid=True, whichAxis='both', gridColor='0.9', gridStyle=':'):
        """Sets the grid on the plot"""
        # self._BaseFigure__axis.minorticks_on()
        if ( showGrid ):
            self._BaseFigure__axis.grid(b=showGrid, which=whichAxis, color=gridColor, linestyle=gridStyle, alpha=0.9)

        return

    def __applyScales(self):
        """Applies the scale for the X/Y axis"""

        # Apply X scale:
        if ( self.__xScale == self.__validScales[0] ):
            self._BaseFigure__axis.set_xscale(self.__xScale)
        elif ( self.__xScale == self.__validScales[1] ):
            self._BaseFigure__axis.set_xscale(self.__xScale, nonposx='clip')
        elif ( self.__xScale == self.__validScales[2] ):
            self._BaseFigure__axis.set_xscale(self.__xScale)

        # Apply y scale:
        if ( self.__yScale == self.__validScales[0] ):
            self._BaseFigure__axis.set_yscale(self.__yScale)
        elif ( self.__yScale == self.__validScales[1] ):
            self._BaseFigure__axis.set_yscale(self.__yScale, nonposy='clip')
        elif ( self.__yScale == self.__validScales[2] ):
            self._BaseFigure__axis.set_yscale(self.__yScale)

        return

    def __applyXLimits(self):
        """Applies the X-limits to the axis."""
        # Set default values:
        xMin = self.__lowestLinScaleValueAllowed
        xMax = self.__defaultUpperLim

        # Obtain X min/max values:
        if ( self.__dynamicX ):
            xMin = (1 - self.__dynamicXScalingFrac) * self.__minDynamicX
            xMax = (1 + self.__dynamicXScalingFrac) * self.__maxDynamicX
        else:
            xMin = self.__xMin
            xMax = self.__xMax

        xMin, xMax = self.__validateLimits(xMin, xMax, self.__xScale)

        # Apply limits:
        self._BaseFigure__axis.set_xlim(xMin, xMax)

        return

    def __applyYLimits(self):
        """Applies the Y-limits to the axis."""
        # Set default values:
        yMin = self.__lowestLinScaleValueAllowed
        yMax = self.__defaultUpperLim

        # Obtain X min/max values:
        if ( self.__dynamicY ):
            yMin = (1 - self.__dynamicYScalingFrac) * self.__minDynamicY
            yMax = (1 + self.__dynamicYScalingFrac) * self.__maxDynamicY
        else:
            yMin = self.__yMin
            yMax = self.__yMax

        yMin, yMax = self.__validateLimits(yMin, yMax, self.__yScale)

        # Apply limits:
        self._BaseFigure__axis.set_ylim(yMin, yMax)

        return

    def setXScale(self, newScale = None):
        """Sets the X scale"""

        if ( newScale is not None ):
            if ( not isinstance(newScale, str) ):
                # Convert to string if possible:
                try:
                    newScale = str(newScale)
                except:
                    newScale = self.__xScale
                    self.__write.message = "Could not convert desired x scale to text for usage. Defaulting to \"%s\"." % (newScale)
                    self.__write.print(1, 2)

            # Ensure "newScale" is a valid assignment:
            if ( newScale not in self.__validScales ):
                self.__write.message = "Invalid X scale text passed in (\"%s\"). Defaulting to \"%s\"." % (newScale, self.__xScale)
                self.__write.print(1, 2)
                newScale = self.__xScale

        else:
            newScale = self.__xScale
            self.__write.message = "No X scale text was passed in. Defaulting to \"%s\"." % (newScale)
            self.__write.print(1, 2)

        self.__xScale = newScale

        return

    def setYScale(self, newScale = None):
        """Sets the Y scale"""

        if ( newScale is not None ):
            if ( not isinstance(newScale, str) ):
                # Convert to string if possible:
                try:
                    newScale = str(newScale)
                except:
                    newScale = self.__yScale
                    self.__write.message = "Could not convert desired y scale to text for usage. Defaulting to \"%s\"." % (newScale)
                    self.__write.print(1, 2)

            # Ensure "newScale" is a valid assignment:
            if ( newScale not in self.__validScales ):
                self.__write.message = "Invalid Y scale text passed in (\"%s\"). Defaulting to \"%s\"." % (newScale, self.__yScale)
                self.__write.print(1, 2)
                newScale = self.__yScale

        else:
            newScale = self.__yScale
            self.__write.message = "No Y scale text was passed in. Defaulting to \"%s\"." % (newScale)
            self.__write.print(1, 2)

        self.__yScale = newScale
        return

    def setXLims(self, newXMin = None, newXMax = None):
        """Sets the X limits for the program"""

        # Set default X min/max:
        if ( newXMin is None ):
            if ( self.__dynamicX ):
                newXMin = self.__minDynamicX
            else:
                newXMin = self.__xMin
        if ( newXMax is None ):
            if ( self.__dynamicX ):
                newXMax = self.__maxDynamicX
            else:
                newXMax = self.__xMax

        # Validate and set limits:
        self.__xMin, self.__xMax = self.__validateLimits(newXMin, newXMax, self.__xScale)

        # Print to user:
        self.__write.message = "The plot's X-axis will have range [%.4E, %.4E]." % (self.__xMin, self.__xMax)
        self.__write.print(2, 3)

        # Turn off dynamic X scaling:
        if ( self.__dynamicX ):
            self.__dynamicX = False
            self.__write.message = "   Dynamic X limits will not be used."
            self.__write.print(2, 3)

        return

    def setYLims(self, newYMin = None, newYMax = None):
        """Sets the Y limits for the program"""

        # Set default X min/max:
        if ( newYMin is None ):
            if ( self.__dynamicY ):
                newYMin = self.__minDynamicY
            else:
                newYMin = self.__yMin
        if ( newYMax is None ):
            if ( self.__dynamicY ):
                newYMax = self.__maxDynamicY
            else:
                newYMax = self.__yMax

        # Validate and set limits:
        self.__yMin, self.__yMax = self.__validateLimits(newYMin, newYMax, self.__yScale)

        # Print to user:
        self.__write.message = "The plot's Y-axis will have range [%.4E, %.4E]." % (self.__yMin, self.__yMax)
        self.__write.print(2, 3)

        # Turn off dynamic X scaling:
        if ( self.__dynamicY ):
            self.__dynamicY = False
            self.__write.message = "   Dynamic Y limits will not be used."
            self.__write.print(2, 3)

        return

    def updateDynamicX(self, xValues):
        """Updates the min/max X values for a dynamic X-axis."""

        # Ensure input parameters is a list:
        if ( not isinstance(xValues, list) ):
            self.__write.message = "A list of floats must be used to update dynamic X limits. Limits will not be updated."
            self.__write.print(1, 3)
            return

        # Find min/max:
        tempMin  = float("inf")
        temp2Min = float("inf")
        for i in range(0, len(xValues), 1):
            # Find the lowest and the second lowest unique value:
            if ( xValues[i] < tempMin ):
                temp2Min = tempMin
                tempMin = xValues[i]
            elif ( (xValues[i] < temp2Min) and (not xValues[i] == tempMin)):
                temp2Min = xValues[i]

            # Find maximum value:
            self.__maxDynamicX = max( self.__maxDynamicX, xValues[i] )


        # Use lowest or second lowest value (depending on scale)
        if ( self.__xScale == self.__validScales[0] ):
            self.__minDynamicX = min( self.__minDynamicX, tempMin)
        else:
            appliedMin = tempMin
            if ( appliedMin <= 0.00 ):
                appliedMin = temp2Min
            self.__minDynamicX = min( self.__minDynamicY, appliedMin)

        return

    def updateDynamicY(self, yValues):
        """Updates the min/max Y values for a dynamic X-axis."""

        # Ensure input parameters is a list:
        if ( not isinstance(yValues, list) ):
            self.__write.message = "A list of floats must be used to update dynamic Y limits. Limits will not be updated."
            self.__write.print(1, 3)
            return

        # Find min/max:
        tempMin  = float("inf")
        temp2Min = float("inf")
        for i in range(0, len(yValues), 1):
            # Find the lowest and the second lowest unique value:
            if ( yValues[i] < tempMin ):
                temp2Min = tempMin
                tempMin = yValues[i]
            elif ( (yValues[i] < temp2Min) and (not yValues[i] == tempMin)):
                temp2Min = yValues[i]

            # Find maximum value:
            self.__maxDynamicY = max( self.__maxDynamicY, yValues[i] )

        # Use lowest or second lowest value (depending on scale)
        if ( self.__yScale == self.__validScales[0] ):
            self.__minDynamicY = min( self.__minDynamicY, tempMin)
        else:
            appliedMin = tempMin
            if ( appliedMin <= 0.00 ):
                appliedMin = temp2Min
            self.__minDynamicY = min( self.__minDynamicY, appliedMin)

        return

    def applyAxisLimits(self):
        """Sets the axis scale, range for both the X/Y axes, and applies a grid."""

        self.__applyXLimits()
        self.__applyYLimits()
        self.__applyScales()
        self.__applyGrid()

        return


# Actual Plot class:
class PlotClass(_PlotLabeling, _AxisLimits):
    """The \"PlotClass\" object is meant to help users/clients use some of the
    main plotting functions allowed by Matplotlib.

    Accessible Member Functions ( Purpose ):
    -toggleSeveralPlots   ( Allows user to change behavior )
    -addPlotType          ( Adds a plot type; used to create multiple plot "types" on a single figure [i.e. several angles, etc.] )
    -setLegendPos         ( Sets the legend position on the axis )
    -addHistogram         ( Adds a histogram to the plot )
    -addLine              ( Adds a line to the plot )
    -finalizePlot         ( Sets up axis labels, scale, limits, annotations, and legend before showing )
    -showCurrentPlot      ( Shows the current plot to the user )
    -savePlot             ( Saves the plot to a file )
    ----------------------------------------------------------------------------

    """
    # Defaults for the legend:
    __defaultLegendX = float(1.0E-4)
    __defaultLegendY = float(1.0E-4)
    __defaultLegendPos = "best"
    # Defaults for the plot class:
    __defaultAllowSeveralPlots = True

    # For line coloring and styles:
    __lineColors = ('blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', \
    'olive', 'c', 'mediumaquamarine', 'y', 'rosybrown')
    __expDataColor = ("dimgray")
    __lineStyles = ('-','--',':','-.')
    __markers = ("v", "8", "s", "p", "*", "h", "D", "o", "^")
    __numMarkers = len(__markers)
    __myMarkerIndx = 0
    __numColors = len( __lineColors )
    __numLineStyles = len( __lineStyles )

    # Misc. defaults:
    __opacity = 0.60          # Allows line to be seen through (for overlapping lines)
    __typeExpScaling = 2      # Scale Y-Values by 10^(numPlotTypes * thisValue)
    __useOwnHistPlot = True   # Use a line to represent a histogram

    def __init__(self, allowSeveralPlots = __defaultAllowSeveralPlots, newPrint=Print()):
        """PlotClass main constructor"""

        # Construct parent classes:
        super(PlotClass, self).__init__()

        # Set default values:
        self.__write = newPrint
        self.__resetMembers()

        # Set user/client specified values:
        self.toggleSeveralPlots( allowSeveralPlots )

        return

    def __del__(self):
        """PlotClass destructor method"""
        self.__resetMembers()

        return

    def __resetMembers(self):
        """Resets all the class's member-variables to their defaults"""

        # Regarding legend information:
        self.__legendPos = self.__defaultLegendPos
        self.__legendPosXY = None

        # Regarding plot information
        self.__totNumPlottedLines = 0
        self.__allowSeveralPlots = self.__defaultAllowSeveralPlots
        self.__numPlotTypes = 0       # Number of plot types created
        self.__numPlotTypeLines = 0   # Number of lines in the plot type

        return

    def __applyLegend(self):
        """Applies the legend to the plot"""
        if ( self.__legendPosXY == None ):
            self._BaseFigure__axis.legend(loc=self.__legendPos)
        else:
            self._BaseFigure__axis.legend(loc=self.__legendPos, bbox_to_anchor=self.__legendPosXY)

        return

    def __addedLine(self):
        """Checks to add a legend label and adds a plot line to the object"""

        self.__numPlotTypeLines += 1
        self.__totNumPlottedLines += 1

        return

    def __findLastNonZeroValueIndex(self, someNumbers):
        """This function returns the index of the last non-zero valued entry
        in a list or tuple."""
        lastIndex = None

        # Ensure the numbers are a list/tuple of floats or ints:
        if ( not isinstance(someNumbers, (list, tuple)) ):
            self.__write.message = "Cannot find the last non-zero valued entry in any type except lists or tuples."
            self.__write.print(1, 2)
            return lastIndex

        # Find last non-zero valued index:
        lastValidIndex = len(someNumbers) - 1
        for i in range(0, lastValidIndex, 1):
            lastIndex = lastValidIndex-i
            if ( someNumbers[lastIndex] > 0 ):
                break

        return lastIndex

    def __getLineColor(self):
        """Returns the line color to be used (based on allowance of several plot types)"""

        colorFlag = 0
        if ( self.__allowSeveralPlots ):
            colorFlag = self.__numPlotTypes
        else:
            colorFlag = self.__totNumPlottedLines

        return self.__lineColors[ colorFlag % self.__numColors ]

    def __getLineStyle(self):
        """Returns the line style to be used (based on allowance of several plot types)"""

        styleFlag = 0
        if ( self.__allowSeveralPlots ):
            styleFlag = self.__numPlotTypeLines
        else:
            styleFlag = 0   # Use consistent style for a plot of single-type
            # styleFlag = self.__totNumPlottedLines

        return self.__lineStyles[ styleFlag % self.__numLineStyles ]

    def __getMarker(self):
        """Returns the marker for the plot"""
        self.__myMarkerIndx = (self.__myMarkerIndx % self.__numMarkers)
        theMarker = self.__markers[ self.__myMarkerIndx ]
        self.__myMarkerIndx += 1
        return theMarker

    def toggleSeveralPlots(self, allowSeveralPlots = True):
        """Toggles the allowance of printing several plots on the graph.
        Allowance gives lines new colors
        \t(lines within the same \"plot\" have same color, different line style)
        """
        # Validate argument:
        if ( not isinstance(allowSeveralPlots, bool) ):
            try:
                allowSeveralPlots = bool(allowSeveralPlots)
            except:
                self.__write.print(3, 2)
                self.__write.message = "Unable to determine argument (\"%s\") type for allowing several plots." % ( str(allowSeveralPlots) )
                self.__write.print(1, 2)
                allowSeveralPlots = self.__defaultAllowSeveralPlots
                self.__write.message = "  The default (%r) will be used." % ( allowSeveralPlots )
                self.__write.print(1, 2)

        # Ensure no data has been entered; if so, warn user that labels may be skewed.
        if ( self.__totNumPlottedLines > 0 ):
            self.__write.print(3, 3)
            self.__write.message = "Toggling the allowance of many plots should be done when no data has been specified for proper appearance."
            self.__write.print(1, 3)
            self.__write.message = "   All data plotted herein will have the same color."
            self.__write.print(1, 3)

        self.__allowSeveralPlots = allowSeveralPlots

        return

    def addPlotType(self):
        """Creates a new plot within the figure
        (modifies scaling, colors and/or linestyle of proceeding lines)
        """
        if ( self.__allowSeveralPlots ):
            self.__numPlotTypes += 1
            self.__numPlotTypeLines = 0
        else:
            self.__write.message = "Cannot add a plot type. Allowance of several plots must be toggled on prior."
            self.__write.print(1, 2)

        return

    def setLegendPos(self, loc = __defaultLegendPos, xStart = __defaultLegendX, yStart = __defaultLegendY ):
        """Sets position of legend"""
        # Default values (minimum for uniqueness)
        __uniqueLOC = ['b', 'upper r', 'upper l', 'lower l',
        'lower r', 'r', 'center l', 'center r', 'lower c',
        'upper c', "ce"]
        # Full named values (ensures "LOC" is always valid)
        __validLOC = ['best', 'upper right', 'upper left', 'lower left',
        'lower right', 'right', 'center left', 'center right', 'lower center',
        'upper center', 'center']
        # For using coordinate values
        __coordinateFlag = "co"

        # Reduced LOC (location)
        loc = loc.strip().lower()

        # Validate argument:
        validArgument = False
        for i in range(0, len(__uniqueLOC), 1):
            if ( loc.startswith(__uniqueLOC[i]) ):
                loc = __validLOC[i]
                validArgument = True
                break

        # Set legend location:
        if ( validArgument ):
            self.__legendPos = loc
        elif ( loc.startswith(__coordinateFlag) ):
            # Use X/Y Position instead; ensure X/Y combo will appear in axis:
            if ( xStart <= 0.00 ):
                xStart = self.__defaultLegendX
            if ( yStart <= 0.00 ):
                yStart = self.__defaultLegendY

            self.__legendPos = "upper left"
            self.__legendPosXY = (xStart, yStart)

        else:
            # Bad argument; use defaults
            self.__write.print(3, 3)
            self.__write.message = "Unable to validate legend position flag (\"%s\")." % (loc)
            self.__write.print(1, 3)
            loc = self.__defaultLegendPos
            self.__write.message = "   \"%s\" will be used." % loc
            self.__write.print(1, 3)
            self.__legendPos = loc

        return

    # For adding plots:
    def addHistogram(self, myBins, myValues, myLabel="No label given", xScale=1, yScale=1):
        """Adds a histogram to the plot"""
        # Ensure scaling is valid (>0):
        if ( isinstance(xScale, (float, int)) ):
            if ( xScale <= 0 ):
                xScale = 1.00
        else:
            xScale = 1.00
        if ( isinstance(yScale, (float, int)) ):
            if ( yScale <= 0 ):
                yScale = 1.00
        else:
            yScale = 1.00

        # Validate the types of the bins and values:
        if ( not isinstance(myBins, list) ):
            self.__write.message = "The passed in histogram bins must be a list."
            self.__write.print(1, 2)
            self.__write.message = "   Unable to create histogram."
            self.__write.print(1, 2)
            return
        if ( not isinstance(myValues, list) ):
            self.__write.message = "The passed in histogram values must be a list."
            self.__write.print(1, 2)
            self.__write.message = "   Unable to create histogram."
            self.__write.print(1, 2)
            return

        # Shift and scale histogram data accordingly:
        # (shift and scale bins)
        shift = 0.00
        if ( myBins[0] < 0.00 ):
            shift = -myBins[0]
            self.__write.message = "Histogram bins values will be shifted up by (%f) to ensure physicality." % (shift)
            self.__write.print(2, 2)
        for i in range(0, len(myBins), 1):
            myBins[i] += shift
            myBins[i] *= xScale
        # (shift and scale values)
        shift = 0.00
        for i in range(0, len(myValues), 1):
            shift = min(shift, myValues[i] )
        if (shift < 0.00 ):
            shift = abs(shift)
            self.__write.message = "Histogram bins values will be shifted up by (%f) to ensure physicality." % (shift)
            self.__write.print(2, 2)
        else:
            shift = 0.00
        for i in range(0, len(myValues), 1):
            myValues[i] += shift
            myValues[i] *= yScale

        # Determine the last value that has non-zero entry:
        lastValueIndx = self.__findLastNonZeroValueIndex( myValues )

        # Use the minimum number of applicable data points (base off num. bins/num. values):
        numValidData = min( lastValueIndx+1, len(myBins)-1 )

        # Obtain bin bounds and associated values:
        plottedBins   = []
        plottedValues = []
        plottedBins.append( myBins[0] )
        for i in range(0, numValidData, 1):
            # Ensure positive (or non-zero) bin widths:
            if ( myBins[i+1] < myBins[i] ):
                self.__write.message = "Negative bin-width is not valid (range=[%.2f, %.2f). Using bin width of 0." % (myBins[i], myBins[i+1])
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
        self.updateDynamicX( plottedBins )
        self.updateDynamicY( plottedValues )

        # Only use first few labels:
        if ( self.__numPlotTypes > 0 ):
            theLabel = None
        else:
            theLabel = myLabel

        if ( not self.__useOwnHistPlot ):
            # Plot histogram:
            self._BaseFigure__axis.hist(plottedValues, bins=plottedBins,
            histtype='step', color=self.__getLineColor(), label=theLabel)
            self.__addedLine()

        else:
            # Create new X/Y values to emulate the look of a histogram (i.e. 2 Y values per X value, except at edges)
            xVals = []
            yVals = []
            xVals.append( plottedBins[0] )
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

            # Now plot as a line (note: scaling has already been done)
            self.addLine(xVals, yVals, myLabel, 1.00, 1.00)

        return

    def addLine(self, xVals, yVals, myLabel="No label given", xScale=1, yScale=1):
        """Adds a line to the plot"""
        # Ensure scaling is valid (>0):
        if ( isinstance(xScale, (float, int)) ):
            if ( xScale <= 0 ):
                xScale = 1.00
        else:
            xScale = 1.00
        if ( isinstance(yScale, (float, int)) ):
            if ( yScale <= 0 ):
                yScale = 1.00
        else:
            yScale = 1.00

        # Validate the types of the bins and values:
        if ( not isinstance(xVals, list) ):
            self.__write.message = "The passed in histogram bins must be a list."
            self.__write.print(1, 2)
            self.__write.message = "   Unable to create histogram."
            self.__write.print(1, 2)
            return
        if ( not isinstance(yVals, list) ):
            self.__write.message = "The passed in histogram values must be a list."
            self.__write.print(1, 2)
            self.__write.message = "   Unable to create histogram."
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

        # For multiple types, scale:
        yScaleFactor = -self.__numPlotTypes * self.__typeExpScaling
        yScale = yScale * pow(10, yScaleFactor)
        if ( self.__numPlotTypes > 0 ):
            self.__write.message = "Sim. data for \"%s\" is being scaled by 10^(%.1f) for clarity." % (myLabel, yScaleFactor)
            self.__write.print(2, 2)

        # Obtain x/y set for as many pairs between X/Y coords (base on number of points):
        lastIndex = self.__findLastNonZeroValueIndex( yVals )
        numPairs = min( len(xVals), len(yVals), lastIndex+1 )
        xCoord = []
        yCoord = []
        if ( numPairs <= 0 ):
            self.__write.message = "No data passed in to create a line plot. No plot will be created."
            self.__write.print(1, 2)
            return
        for i in range(0, numPairs, 1):
            xCoord.append( xScale * xVals[i] )
            yCoord.append( yScale * yVals[i] )

        # Obtain min/max X/Y:
        self.updateDynamicX( xCoord )
        self.updateDynamicY( yCoord )

        thisLineColor = self.__getLineColor()
        thisLineStyle = self.__getLineStyle()

        # Remove legend label if desired:
        if ( self.__numPlotTypes > 0 ):
            theLabel = None
        else:
            theLabel = myLabel

        # X/Y values are all valid; create line:
        if ( self._AxisLimits__yScale == self._AxisLimits__validScales[0] ):
            self._BaseFigure__axis.plot( xCoord, yCoord, linestyle=thisLineStyle,
            color=thisLineColor, alpha=self.__opacity, label=theLabel)
        else:
            self._BaseFigure__axis.semilogy( xCoord, yCoord, linestyle=thisLineStyle,
            color=thisLineColor, alpha=self.__opacity, label=theLabel)

        # Add legend entry for first few lines (w/ multiple plots)
        self.__addedLine()

        return

    def addScatter(self, xVals, yVals, myLabel="No label given", xScale=1.00, yScale=1.00, expData=False):
        """Adds a scatter plot to the object"""

        # Verify inputs are valid:
        invalidInput = False
        if ( not isinstance(xVals, list) ):
            self.__write.message = "Scatter plot requires a list of numbers for its X values."
            self.__write.print(1, 2)
            invalidInput = True
        if ( not isinstance(yVals, list) ):
            self.__write.message = "Scatter plot requires a list of numbers for its Y values."
            self.__write.print(1, 2)
            invalidInput = True
        if ( invalidInput ):
            self.__write.message = "   Unable to plot values."
            self.__write.print(1, 2)
            return

        # Scale data:
        if ( xScale <= 0.00 ):
            self.__write.message = "Cannot scale X values by %.3f. Values will not be scaled." % (xScale)
            self.__write.print(1, 2)
            xScale = 1.00
        if ( yScale <= 0.00 ):
            self.__write.message = "Cannot scale Y values by %.3f. Values will not be scaled." % (yScale)
            self.__write.print(1, 2)
            yScale = 1.00
        # Increase Y-scale based on plot type:
        yScaleFactor = -self.__numPlotTypes * self.__typeExpScaling
        yScale = yScale * pow(10, yScaleFactor)
        if ( self.__numPlotTypes > 0 ):
            self.__write.message = "Data for \"%s\" is being scaled by 10^(%.1f) for clarity." % (myLabel, yScaleFactor)
            self.__write.print(2, 2)
        for i in range(0, len(xVals), 1):
            xVals[i] = xVals[i] * xScale
        for i in range(0, len(yVals), 1):
            yVals[i] = yVals[i] * yScale

        # Update dynamic min/max limits for X and Y:
        self.updateDynamicX( xVals )
        self.updateDynamicY( yVals )

        # Remove legend label if desired:
        if ( self.__numPlotTypes > 0 and not expData ):
            theLabel = None
        else:
            theLabel = myLabel

        # Obtain what will be the line's properties:
        if ( expData ):
            theColor = self.__expDataColor
        else:
            theColor = self.__getLineColor()
        theMarker = self.__getMarker()

        self._BaseFigure__axis.scatter(xVals, yVals, s=60, marker=theMarker,
        edgecolors=theColor, facecolors='none', linewidth=1.5, label=theLabel,
        alpha=0.5)

        # Add plot if not experimental data:
        if ( not expData ):
            self.__addedLine()

        return

    def addErrorBar(self, xVals, yVals, xErr=None, yErr=None, myLabel = "No label given", xScale = 1.00, yScale = 1.00, expData = True):
        """Create an errorbar type plot line"""

        # Verify inputs are valid:
        invalidInput = False
        if ( not isinstance(xVals, list) ):
            self.__write.message = "Error bar plot requires a list of numbers for its X values."
            self.__write.print(1, 2)
            invalidInput = True
        if ( not isinstance(yVals, list) ):
            self.__write.message = "Error bar plot requires a list of numbers for its Y values."
            self.__write.print(1, 2)
            invalidInput = True
        if ( invalidInput ):
            self.__write.message = "   Unable to plot values."
            self.__write.print(1, 2)
            return

        # Scale data:
        if ( xScale <= 0.00 ):
            self.__write.message = "Cannot scale X values by %.3f. Values will not be scaled." % (xScale)
            self.__write.print(1, 2)
            xScale = 1.00
        if ( yScale <= 0.00 ):
            self.__write.message = "Cannot scale Y values by %.3f. Values will not be scaled." % (yScale)
            self.__write.print(1, 2)
            yScale = 1.00
        # Increase Y-scale based on plot type:
        yScaleFactor = -self.__numPlotTypes * self.__typeExpScaling
        yScale = yScale * pow(10, yScaleFactor)
        if ( self.__numPlotTypes > 0 ):
            self.__write.message = "Exp. data for \"%s\" is being scaled by 10^(%.1f) for clarity." % (myLabel, yScaleFactor)
            self.__write.print(2, 2)
        for i in range(0, len(xVals), 1):
            xVals[i] = xVals[i] * xScale
        for i in range(0, len(yVals), 1):
            yVals[i] = yVals[i] * yScale

        # Update dynamic min/max limits for X and Y:
        self.updateDynamicX( xVals )
        self.updateDynamicY( yVals )

        # Remove legend label if desired:
        if ( self.__numPlotTypes > 0 and not expData ):
            theLabel = None
        else:
            theLabel = myLabel

        # Obtain what will be the line's properties:
        if ( expData ):
            theColor = self.__expDataColor
        else:
            theColor = self.__getLineColor()
        theMarker = self.__getMarker()

        self._BaseFigure__axis.errorbar(xVals, yVals, xerr=xErr, yerr=yErr,
        marker=theMarker, mec=theColor, ecolor=theColor, ms=6.5, mew=1.5,
        mfc='none', linewidth=0, label=theLabel)

        # Add plot if not experimental data:
        if ( not expData ):
            self.__addedLine()

        return

    def clearLines(self):
        """Clears all lines from the current plot"""
        self._BaseFigure__axis.lines = []
        return

    # For finishing a plot:
    def finalizePlot(self):
        """Finalizes the plot axis and behaviors"""

        self.labelPlot()         # Apply labels to the plot:
        self.applyAxisLimits()   # Sets up axis range and scale
        self.__applyLegend()

        return

    def showCurrentPlot(self):
        """Shows the plot"""

        # Set plot details:
        self.finalizePlot()

        # plt.ion()
        self.__write.message = "Showing plot..."
        self.__write.print(2, 2)
        plt.show()
        time.sleep( 0.00 )

        return

    def savePlot(self, figName="temp", figDPI = 300, showPlot = False, overrideExisting=False, figBBox = 'tight', figPad=0.15):
        """Save the plot to a file"""

        # Set plot details:
        self.finalizePlot()

        # Skip plotting if nothing exists on the plot:
        if ( self.__totNumPlottedLines <= 0 ):
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
        self.__write.print(2, 1)

        # Save file:
        plt.savefig(figName, bbox_inches=figBBox, pad_inches=figPad, dpi = figDPI)

        if ( showPlot ):
            self.showCurrentPlot()

        return
