
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
import fileModule


# VERSION Number:
__version__ = "1.0.0"



class PlotGSMInputFile:
    """Reads an input file and sets values based on input specification."""
    # Input arguments:
    __axisLims = ("xrange", "yrange", "xscale", "yscale")
    __figLabels = ("xlabel", "ylabel", "title")
    __dataArgs = ("data", "sim")
    __plotArgs = ("particle", "plot", "angle")
    __annotateArgs = ("annotate", "annotatePos", "otherAnnotate", "otherAnnotatePos")
    __miscArgs = ("comment", "c", "save", "dpi", "show")
    __endArgs = ("end", "quit", "stop", "done")

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

        # Comment information:
        self.__comments = []

        # File names:
        self.__dataFiles = []
        self.__simFiles = []
        self.__numDataFiles = 0
        self.__numSimFiles = 0
        self.__saveName = []

        # Create defaults for clients to define:
        self.__xScale = "linear"
        self.__xMin = None
        self.__xMax = None
        self.__yScale = "log"
        self.__yMin = None
        self.__yMax = None

        # Plot labels:
        self.__xLabel = "Particle Energy"
        self.__yLabel = "Cross Section [Units]"
        self.__plotTitle = "Cross Section for a Reaction"

        # Regarding what to plot:
        self.__particles = []
        self.__plotTypes = []
        self.__plotAngles = []

        # For annotations:
        self.__mainAnnotation = None
        self.__mainAnnotationPosX = 0.00
        self.__mainAnnotationPosY = 0.00
        self.__otherAnnotation = []
        self.__otherAnnotationX = []
        self.__otherAnnotationY = []

        # Data regarding the file:
        self.__inputName = None
        self.__fileData = []
        self.__fileLen = 0
        self.__fileWasRead = False

        # Misc information:
        self.__figDPI = 1200

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
        foundFlag = False


        return foundFlag

    def __applyDataArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __dataArgs tuple"""
        foundFlag = False

        return foundFlag

    def __applyPlotArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __plotArgs tuple"""
        foundFlag = False

        return foundFlag

    def __applyAnnotateArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __annotateArgs tuple"""
        foundFlag = False

        return foundFlag

    def __applyMiscArgs(self, lineID, lineFlag):
        """Checks if the input has flag from the __miscArgs tuple"""

        foundFlag = True
        if ( lineID == self.__miscArgs[0] ):
            # Comment: Print out with low verbosity:
            self.__comments.append( lineFlag )
            self.__write.message = "%s" % (self.__comments[len(self.__comments)-1])
            self.__write.print(2, 2)
        elif ( lineID == self.__miscArgs[1] ):
            # "c": Print out with high verbosity; don't append.
            self.__write.message = "%s" % (lineFlag)
            self.__write.print(2, 4)
        elif ( lineID == self.__miscArgs[2] ):
            # "save": create plot and save it:
            self.__saveName = str(lineFlag)
            self.__write.message = "The plot will be saved into file \"%s\"." % (self.__saveName)
            self.__write.print(2, 3)
        elif ( lineID == self.__miscArgs[3] ):
            # "dpi":
            try:
                newDPI = int(lineFlag)
            except:
                newDPI = self.__figDPI
                self.__write.message = "Could not determine the desired figure's DPI (\"%s\"). Using default..." % (lineFlag, newDPI)
                self.__write.print(1, 2)
            self.__figDPI = newDPI
        elif ( lineID == self.__miscArgs[4] ):
            # "show":
            self.__write.message = "Showing plot for 2 minutes..."
            self.__write.print(2, 2)
            self.__myPlot.showCurrentPlot(120)
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
        else:
            foundFlag = False

        return foundFlag

    def createPlot(self):
        """Creates the plot and shows/saves it accordingly"""

        # Setup the plot's characteristics:
        # (X and Y range and scale)
        self.__myPlot.setXScale( self.__xScale )
        self.__myPlot.setYScale( self.__yScale )
        if ( not self.__xMin == None and not self.__xMax == None ):
            self.__myPlot.setXLims(self.__xMin, self.__xMax)
        if ( not self.__yMin == None and not self.__yMax == None ):
            self.__myPlot.setYLims(self.__yMin, self.__yMax)

        # Create new plot object:
        self.__newPlot()

        return
