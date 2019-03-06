
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


# MODULES:
from printClass import Print
from plotClass import PlotClass
from outputClass import GSMOutput
import fileModule


# VERSION Number:
__version__ = "1.0.0"



class PlotGSMInputFile:
    """Reads an input file and sets values based on input specification."""
    # Input arguments:
    __fileCommentFlag = "#"
    __axisLims = ("xrange", "yrange", "xscale", "yscale")
    __figLabels = ("xlabel", "ylabel", "title")
    __dataArgs = ("data", "sim", "simlabel")
    __plotArgs = ("particle", "plot", "angle")
    __annotateArgs = ("annotate", "annotatepos", "otherannotate", "otherannotatepos", "otherannotatecolor", "legend")
    __miscArgs = ("comment", "c", "save", "dpi", "show", "override")
    __endArgs = ("end", "quit", "stop", "done", "new")
    __defaultAnnotatePos = 1.0E-2
    __defaultAnnotationColor = "blue"

    def __init__(self, inputName=None, newPrint = Print()):
        """Constructor for the \"PlotInputFile\" class"""

        # Set default values:
        self.__write = newPrint

        # Reset all values:
        self.__resetMembers()

        # Read input file and store data:
        if ( not isinstance(inputName, str) ):
            self.__write.message = "The required argument must be of string type: ", inputName
            self.__write.print(0, 1)
            return
        self.__inputName = inputName
        doesFileExist = fileModule.fileExists( self.__inputName )
        if ( not doesFileExist ):
            self.__write.message = "File \"%s\" does not exist in this directory. Cannot read input file." % ( self.__inputName )
            self.__write.print(0, 1)
            return

        # Read file:
        self.__fileData = fileModule.readFile( self.__inputName )
        self.__fileLen  = len( self.__fileData )
        self.__fileWasRead = True

        # Parse out information in the file:
        self.__parseInput()

        return

    def __del__(self):
        """Destructor for the \"PlotInputFile\" class"""
        self.__resetMembers()

        return

    def __resetMembers(self):
        """Resets all member-variables in the class"""

        # File names:
        self.__dataFiles = []
        self.__simFiles = []
        self.__simLabels = []
        self.__numDataFiles = 0
        self.__numSimFiles = 0
        self.__numSimLabels = 0
        self.__simObjects = []
        self.__numSimObjects = 0
        self.__expObjects = []
        self.__numExpObjects = 0
        # Whether or not to override:
        self.__override = False

        # Data regarding the file:
        self.__inputName = None
        self.__fileData = []
        self.__fileLen = 0
        self.__fileWasRead = False

        # Reset all others:
        self.__resetPlotSpecifics()

        return

    def __resetPlotSpecifics(self):
        """Resets all plot-specific variables"""

        # Reset all others:
        self.__resetAnnotations()
        self.__resetAxis()
        self.__resetOther()

        return

    def __resetAnnotations(self):
        """Resets all annotations in the class"""

        self.__mainAnnotation = None
        self.__mainAnnotationPosX = self.__defaultAnnotatePos
        self.__mainAnnotationPosY = self.__defaultAnnotatePos
        self.__otherAnnotation = []
        self.__otherAnnotationX = []
        self.__otherAnnotationY = []
        self.__otherAnnotationColor = []
        self.__numOtherAnnotations = 0
        self.__legendPos = "best"
        self.__legendPosX = self.__defaultAnnotatePos
        self.__legendPosY = self.__defaultAnnotatePos

        return

    def __resetAxis(self):
        """Resets all axis data in the class"""

        # Scales and limits:
        self.__xScale = "linear"
        self.__xMin = None
        self.__xMax = None
        self.__yScale = "log"
        self.__yMin = None
        self.__yMax = None

        # Plot labels:
        self.__xLabel = None
        self.__yLabel = None
        self.__plotTitle = None

        return

    def __resetOther(self):
        """Resets all other member-variables in the class"""

        # Comment information:
        self.__comments = []
        self.__numComments = 0
        # Reset name to be saved to:
        self.__saveName = None

        # Regarding what to plot:
        self.__particles = []
        self.__numParticles = 0
        self.__plotAngles = []
        self.__numAngles = 0
        self.__plotTypes = []
        self.__numPlotTypes = 0

        # Misc information:
        self.__figDPI = 1200
        self.__showPlot = False

        return

    def __applyPlotLabels(self):
        """Applies the X/Y axis labels and the plot title"""

        # Apply X-axis label specific to the requested plot:
        if ( self.__xLabel == None ):
            self.__xLabel = "Particle Energy [MeV]"

        # Apply Y-axis label specific to the requested plot:
        if ( self.__yLabel == None ):
            self.__yLabel = "Cross Section [mb/sr/MeV]"

        # Apply plot title:
        if ( self.__plotTitle == None ):
            self.__plotTitle = "Differential Cross Section"


        # Apply labels and plot title to the plot:
        self.__myPlot.setXLabel( self.__xLabel )
        self.__myPlot.setYLabel( self.__yLabel )
        self.__myPlot.setPlotTitle( self.__plotTitle )

        return

    def __applyAxisDetails(self):
        """Applies X/Y range and scale for the current plot"""

        self.__myPlot.setXScale( self.__xScale )
        self.__myPlot.setYScale( self.__yScale )
        if ( not self.__xMin == None and not self.__xMax == None ):
            self.__myPlot.setXLims(self.__xMin, self.__xMax)
        if ( not self.__yMin == None and not self.__yMax == None ):
            self.__myPlot.setYLims(self.__yMin, self.__yMax)

        return

    def __plotLines(self):
        """Plots all lines desired by the users"""




        # Legend information:
        self.__myPlot.setLegendPos( self.__legendPos, self.__legendPosX, self.__legendPosY )

        return

    def __applyAnnotations(self):
        """Applies the primary and all other annotations"""

        self.__myPlot.setMainAnnotation( self.__mainAnnotation, self.__mainAnnotationPosX, self.__mainAnnotationPosY)

        # Check that all "other" annotations have a color and position, otherwise use default:
        self.__numOtherAnnotations = len(self.__otherAnnotation)
        numXPos = len(self.__otherAnnotationX)
        numYPos = len(self.__otherAnnotationY)
        numColor = len(self.__otherAnnotationColor)
        # (X positions)
        if ( not numXPos == self.__numOtherAnnotations ):
            # Append the default value to the list until the lengths match:
            self.__write.message = "The X-value for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numXPos)
            self.__write.print(1, 2)
            self.__write.message = "  The default X-value (%.3E) will be utilized for these annotations." % (self.__defaultAnnotatePos)
            self.__write.print(1, 2)
            for i in range( numXPos, self.__numOtherAnnotations, 1):
                self.__otherAnnotationX.append( self.__defaultAnnotatePos )
        # (Y positions)
        if ( not numYPos == self.__numOtherAnnotations ):
            # Append the default value to the list until the lengths match:
            self.__write.message = "The Y-value for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numYPos)
            self.__write.print(1, 2)
            self.__write.message = "  The default Y-value (%.3E) will be utilized for these annotations." % (self.__defaultAnnotatePos)
            self.__write.print(1, 2)
            for i in range( numYPos, self.__numOtherAnnotations, 1):
                self.__otherAnnotationY.append( self.__defaultAnnotatePos )
        # (colors)
        if ( not numColor == self.__numOtherAnnotations ):
            # Append the default color to the list until the lengths match:
            self.__write.message = "The color for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numColor)
            self.__write.print(1, 2)
            self.__write.message = "   The default color, \"%s\", will be used for these annotations." % (self.__defaultAnnotationColor)
            self.__write.print(1, 2)
            for i in range( numColor, self.__numOtherAnnotations, 1):
                self.__otherAnnotationColor.append( self.__defaultAnnotationColor )

        # Apply annotations:
        for i in range(0, self.__numOtherAnnotations, 1):
            self.__myPlot.addOtherAnnotation( self.__otherAnnotation[i],
            self.__otherAnnotationX[i], self.__otherAnnotationY[i], self.__otherAnnotationColor[i])

        return

    def __unexpectedLineID(self, lineNumber, lineID):
        """Prints to a developer when an unsuspecting line identifier was found"""
        self.__write.message = "An unexpected line identifier was found on line %d: %s" % (lineNumber, lineID)
        self.__write.print(0, 1)
        self.__write.message = "   Ignoring line..."
        self.__write.print(0, 1)

        return

    def __newPlot(self):
        """Create a new plot for the object and comments to user"""

        # Reset plot specific information:
        self.__resetPlotSpecifics()

        # Print to client/user:
        self.__write.print(3, 1)
        self.__write.print(3, 1)
        self.__write.message = "-------------------------------------"
        self.__write.print(2, 1)
        self.__write.message = "Creating new figure..."
        self.__write.print(2, 1)
        self.__write.message = "-------------------------------------"
        self.__write.print(2, 1)

        # Create new plot class object:
        self.__myPlot = PlotClass()

        return

    def __parseInput(self):
        """Parses out the data in the input file"""

        # Create new plot object:
        self.__newPlot()

        for lineIndx in range(0, self.__fileLen, 1):

            # Get line information:
            lineNumber = lineIndx + 1
            theline = self.__fileData[lineIndx].strip()

            # Remove any end-line comments:
            if ( self.__fileCommentFlag in theline ):
                theline = theline[ : theline.find(self.__fileCommentFlag) ].strip()

            # Skip empty lines:
            if ( theline is "" ):
                # Line is empty, go to next:
                continue

            # Parse line; obtain line identifier and obtain a general flag (i.e. remainder of unparsed line)
            parsedLine = fileModule.parseLine( theline )
            lineFlag = theline[ len(parsedLine[0]) : ].strip()
            lineID = parsedLine[0].lower().strip()

            # Check for valid line identifier:
            foundFlag = self.__applyAxisLims(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyFigLabels(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyDataArgs(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyPlotArgs(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyAnnotateArgs(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyMiscArgs(lineID, lineFlag)
            if ( not foundFlag ):
                foundFlag = self.__applyEndArgs(lineID, lineFlag)

            # If no valid flags found, warn user:
            if ( not foundFlag ):
                self.__unexpectedLineID( lineNumber, lineID )

        return

    def __applyAxisLims(self, lineID, lineFlag):
        """Checks if the input has flag from the __axisLims tuple"""
        # __axisLims = ("xrange", "yrange", "xscale", "yscale")
        foundFlag = True

        if ( lineID == self.__axisLims[0] ):
            # X-range; obtain lower and upper values:
            axisRange = fileModule.parseLine( lineFlag )
            if ( len(lineFlag) < 2 ):
                self.__write.message = "Bad line flag found (line ID is \"%s\"): %s" % ( lineID, lineFlag )
                self.__write.print(0, 2)
                self.__write.message = "   A lower and upper X-axis limit must be supplied to set the range."
                self.__write.print(0, 2)
            else:
                try:
                    xMinVal = float( axisRange[0] )
                except:
                    self.__write.message = "Failed to convert lower X-axis bound to float (\"%s\")." % (axisRange[0])
                    self.__write.print(1, 2)
                    xMinVal = None
                try:
                    xMaxVal = float( axisRange[1] )
                except:
                    self.__write.message = "Failed to convert upper X-axis bound to float (\"%s\")." % (axisRange[1])
                    self.__write.print(1, 2)
                    xMaxVal = None
                self.__xMin = xMinVal
                self.__xMax = xMaxVal

        elif ( lineID == self.__axisLims[1] ):
            # Y-range; obtain lower and upper values:
            axisRange = fileModule.parseLine( lineFlag )
            if ( len(lineFlag) < 2 ):
                self.__write.message = "Bad line flag found (line ID is \"%s\"): %s" % ( lineID, lineFlag )
                self.__write.print(0, 2)
                self.__write.message = "   A lower and upper Y-axis limit must be supplied to set the range."
                self.__write.print(0, 2)
            else:
                try:
                    yMinVal = float( axisRange[0] )
                except:
                    self.__write.message = "Failed to convert lower Y-axis bound to float (\"%s\")." % (axisRange[0])
                    self.__write.print(1, 2)
                    yMinVal = None
                try:
                    yMaxVal = float( axisRange[1] )
                except:
                    self.__write.message = "Failed to convert upper Y-axis bound to float (\"%s\")." % (axisRange[1])
                    self.__write.print(1, 2)
                    yMaxVal = None
                self.__yMin = yMinVal
                self.__yMax = yMaxVal

        elif ( lineID == self.__axisLims[2] ):
            # X scale; apply locally
            self.__xScale = lineFlag.lower().strip()

        elif ( lineID == self.__axisLims[3] ):
            # Y scale; apply locally
            self.__yScale = lineFlag.lower().strip()

        else:
            foundFlag = False

        return foundFlag

    def __applyFigLabels(self, lineID, lineFlag):
        """Checks if the line has flag from the __figLabels tuple"""
        # __figLabels = ("xlabel", "ylabel", "title")
        foundFlag = True

        if ( lineID == self.__figLabels[0] ):
            # Apply custom X label:
            self.__xLabel = lineFlag

        elif ( lineID == self.__figLabels[1] ):
            # Apply custom Y label:
            self.__yLabel = lineFlag

        elif ( lineID == self.__figLabels[2] ):
            # Apply custom figure title:
            self.__plotTitle = lineFlag

        else:
            foundFlag = False


        return foundFlag

    def __applyDataArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __dataArgs tuple"""
        # __dataArgs = ("data", "sim")
        foundFlag = True

        if ( lineID == self.__dataArgs[0] ):
            # Load experimental data file:
            self.__dataFiles.append( lineFlag.strip() )
            self.__write.message = "Experimental data will read from file \"%s\"." % (self.__dataFiles[self.__numDataFiles])
            self.__write.print(2, 2)
            if ( not fileModule.fileExists( self.__dataFiles[self.__numDataFiles] ) ):
                self.__write.message = "   File \"%s\" does not exist for reading experimental data from." % (self.__dataFiles[self.__numDataFiles])
                self.__write.print(1, 2)
            else:
                self.__write.message = "   Reading experimental data..."
                self.__write.print(2, 4)
                self.__numDataFiles += 1

        elif ( lineID == self.__dataArgs[1] ):
            # Load simulation data file:
            self.__simFiles.append( lineFlag.strip() )
            self.__write.message = "Simulated data will read from file \"%s\"." % (self.__simFiles[self.__numSimFiles])
            self.__write.print(2, 2)
            if ( not fileModule.fileExists( self.__simFiles[ len(self.__simFiles)-1 ] ) ):
                self.__write.message = "   File \"%s\" does not exist for reading simulation data from." % (self.__simFiles[self.__numSimFiles])
                self.__write.print(1, 2)
            else:
                self.__write.message = "   Reading simulation data..."
                self.__write.print(2, 4)
                self.__simObjects.append( GSMOutput(self.__simFiles[self.__numSimFiles]) )
                self.__numSimFiles += 1

        elif ( lineID == self.__dataArgs[2] ):
            # Add simulation labels
            simLabels = fileModule.parseLine( lineFlag )

            if ( len(simLabels) > 0 ):
                for i in range(0, len(simLabels), 1):
                    self.__simLabels.append( simLabels[i] )
                    self.__numSimLabels += 1
            else:
                self.__write.message = "No simulation legend labels given. Ignoring line..."
                self.__write.print(1, 2)

        else:
            foundFlag = False

        return foundFlag

    def __applyPlotArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __plotArgs tuple"""
        # __plotArgs = ("particle", "plot", "angle")
        foundFlag = True

        if ( lineID == self.__plotArgs[0] ):
            # Particle given; plot for a particle:
            newParticles = fileModule.parseLine( lineFlag.strip().lower() )
            if ( len(newParticles) > 0 ):
                for i in range(0, len(newParticles), 1):
                    self.__particles.append( newParticles[i] )

            self.__numParticles = len(self.__particles)

        elif ( lineID == self.__plotArgs[1] ):
            # Plot given; specify plot type:
            plotTypes = fileModule.parseLine( lineFlag.strip().lower() )
            if ( len(plotTypes) > 0 ):
                for i in range(0, len(plotTypes), 1):
                    self.__plotTypes.append( plotTypes[i] )

            self.__numPlotTypes = len(self.__plotTypes)

        elif ( lineID == self.__plotArgs[2] ):
            # Plot given angle:
            anglesStr = fileModule.parseLine( lineFlag )
            angleFloat = []
            for i in range(0, len(anglesStr), 1):
                try:
                    angleFloat.append( float(anglesStr[i]) )
                except:
                    self.__write.message = "Could not convert angle flag from specified text: %s" % (anglesStr[i])
                    self.__write.print(1, 2)

            for i in range(0, len(angleFloat), 1):
                self.__plotAngles.append( angleFloat[i] )

            self.__numAngles = len(self.__plotAngles)

        else:
            foundFlag = False

        return foundFlag

    def __applyAnnotateArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __annotateArgs tuple"""
        # __annotateArgs = ("annotate", "annotatePos", "otherAnnotate", "otherAnnotatePos")
        foundFlag = True

        if ( lineID == self.__annotateArgs[0] ):
            # normal annotate (main annotation text)
            self.__mainAnnotation = lineFlag

        elif ( lineID == self.__annotateArgs[1] ):
            # position for main annotation
            posStr = fileModule.parseLine( lineFlag )
            if ( len(posStr) < 2 ):
                self.__write.message = "Two values must be given to specify the (X,Y) coordinate of the primary annotation."
                self.__write.print(1, 2)
                self.__write.message = "   Default position will be used."
                self.__write.print(1, 2)

            if ( len(posStr) >= 1 ):
                try:
                    xPos = float( posStr[0] )
                except:
                    self.__write.message = "Unable to convert X position of primary annotation to float: %s" % (posStr[0])
                    self.__write.print(1, 2)
                    xPos = self.__defaultAnnotatePos
            else:
                xPos = self.__defaultAnnotatePos

            if ( len(posStr) >= 2 ):
                try:
                    yPos = float( posStr[1] )
                except:
                    self.__write.message = "Unable to convert Y position of primary annotation to float: %s" % (posStr[1])
                    self.__write.print(1, 2)
                    yPos = self.__defaultAnnotatePos
            else:
                yPos = self.__defaultAnnotatePos

            if ( not xPos == None and not yPos == None ):
                self.__mainAnnotationPosX = xPos
                self.__mainAnnotationPosY = yPos

        elif ( lineID == self.__annotateArgs[2] ):
            # normal annotate (main annotation text)
            self.__otherAnnotation.append( lineFlag )
            self.__numOtherAnnotations += 1

        elif ( lineID == self.__annotateArgs[3] ):
            # position for other annotation
            posStr = fileModule.parseLine( lineFlag )
            if ( len(posStr) < 2 ):
                self.__write.message = "Two values must be given to specify the (X,Y) coordinate of other annotations."
                self.__write.print(1, 2)
                self.__write.message = "   The default position will be used."
                self.__write.print(1, 2)

            if ( len(posStr) >= 1 ):
                try:
                    xPos = float( posStr[0] )
                except:
                    self.__write.message = "Unable to convert X position of other annotation to float: %s" % (posStr[0])
                    self.__write.print(1, 2)
                    xPos = self.__defaultAnnotatePos
            else:
                xPos = self.__defaultAnnotatePos

            if ( len(posStr) >= 2 ):
                try:
                    yPos = float( posStr[1] )
                except:
                    self.__write.message = "Unable to convert Y position of other annotation to float: %s" % (posStr[1])
                    self.__write.print(1, 2)
                    yPos = self.__defaultAnnotatePos
            else:
                yPos = self.__defaultAnnotatePos

            if ( not xPos == None and not yPos == None ):
                self.__otherAnnotationX.append( xPos )
                self.__otherAnnotationY.append( yPos )

        elif ( lineID == self.__annotateArgs[4] ):
            # set color for other annotation
            otherColors = fileModule.parseLine( lineFlag )
            numColors = len(otherColors)

            if ( numColors > 0 ):
                for i in range(0, numColors, 1):
                    self.__otherAnnotationColor.append( otherColors[i] )

        elif ( lineID == self.__annotateArgs[5] ):
            # Set legend position:
            lineFlag = fileModule.parseLine( lineFlag.strip().lower() )
            numFlags = len(lineFlag)

            if ( numFlags >= 1 ):
                self.__legendPos = lineFlag[0]
            if ( numFlags >= 2 ):
                xPos = self.__defaultAnnotatePos
                try:
                    xPos = float( lineFlag[1] )
                except:
                    self.__write.message = "Unable to convert X-value of legend entry to float: %s" % lineFlag[1]
                    self.__write.print(1, 2)

                self.__legendPosX = xPos
            if ( numFlags >= 3 ):
                yPos = self.__defaultAnnotatePos
                try:
                    yPos = float( lineFlag[2] )
                except:
                    self.__write.message = "Unable to convert Y-value of legend entry to float: %s" % lineFlag[2]
                    self.__write.print(1, 2)

                self.__legendPosY = yPos

        else:
            foundFlag = False

        return foundFlag

    def __applyMiscArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __miscArgs tuple"""
        # __miscArgs = ("comment", "c", "save", "dpi", "show")

        foundFlag = True
        if ( lineID == self.__miscArgs[0] ):
            # Comment: Print out with low verbosity:
            self.__comments.append( lineFlag )
            self.__write.message = "%s" % (self.__comments[self.__numComments])
            self.__write.print(2, 2)
            self.__numComments += 1
        elif ( lineID == self.__miscArgs[1] ):
            # "c": Print out with high verbosity; don't append.
            self.__write.message = "%s" % (lineFlag)
            self.__write.print(2, 4)
        elif ( lineID == self.__miscArgs[2] ):
            # "save": create plot and save it:
            self.__saveName = lineFlag
            self.__write.message = "The plot will be saved into file \"%s.png\"." % (self.__saveName)
            self.__write.print(2, 3)
        elif ( lineID == self.__miscArgs[3] ):
            # "dpi":
            try:
                newDPI = int(lineFlag)
            except:
                newDPI = self.__figDPI
                self.__write.message = "Could not determine the desired figure's DPI (\"%s\"). Using default..." % (lineFlag, newDPI)
                self.__write.print(1, 2)

            # Keep DPI within limits:
            if ( newDPI < 300 ):
                self.__write.message = "Figure DPI below lower limit (300). Using lower limit..."
                self.__write.print(1, 2)
                newDPI = 300
            elif ( newDPI > 1200 ):
                self.__write.message = "Figure DPI below upper limit (1200). Using upper limit..."
                self.__write.print(1, 2)
                newDPI = 1200

            self.__figDPI = newDPI
        elif ( lineID == self.__miscArgs[4] ):
            # "show":
            lineFlag = lineFlag.strip().lower()

            if ( lineFlag == "false" ):
                self.__showPlot = False
            elif ( lineFlag == "true" ):
                self.__showPlot = True
            else:
                self.__write.message = "Invalid flag for showing plot: %s" % (lineFlag)
                self.__write.print(1, 2)

        elif ( lineID == self.__miscArgs[5] ):
            # "override"
            lineFlag = lineFlag.strip().lower()

            if ( lineFlag == "false" ):
                self.__override = False
            elif ( lineFlag == "true" ):
                self.__override = True
            else:
                self.__write.message = "Invalid flag for overriding plot: %s" % (lineFlag)
                self.__write.print(1, 2)

        else:
            foundFlag = False

        return foundFlag

    def __applyEndArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __endArgs tuple"""
        # __endArgs = ("end", "quit", "stop", "done")
        foundFlag = True

        if ( lineID == self.__endArgs[0] ):
            self.createPlot()
        elif ( lineID == self.__endArgs[1] ):
            self.createPlot()
        elif ( lineID == self.__endArgs[2] ):
            self.createPlot()
        elif ( lineID == self.__endArgs[3] ):
            self.createPlot()
        elif ( lineID == self.__endArgs[4] ):
            self.createPlot()
        else:
            foundFlag = False

        return foundFlag

    def createPlot(self):
        """Creates the plot and shows/saves it accordingly"""

        # Setup the plot's characteristics:
        self.__applyPlotLabels()
        self.__applyAxisDetails()
        self.__applyAnnotations()

        # Plot all lines requested:
        self.__plotLines()

        # Show and save plot:
        if ( self.__showPlot and self.__saveName == None ):
            self.__myPlot.showCurrentPlot()
        if ( not self.__saveName == None ):
            self.__myPlot.savePlot(self.__saveName, self.__figDPI, self.__showPlot, self.__override)


        # Create new plot object:
        self.__newPlot()

        return
