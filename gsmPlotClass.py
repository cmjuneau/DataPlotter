
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
from generalPlotTypeClasses import Scatter
import fileModule


# VERSION Number:
__version__ = "1.0.0"



class PlotGSMInputFile:
    """Reads an input file and sets values based on input specification."""
    # Input arguments:
    __validParticles = ("n", "p", "d", "t", "he3", "he4", "he6", "li6", "li7", "li8",
    "li9", "be7", "be9", "be10", "b9", "b10", "b11", "b12", "c11", "c12", "c13",
    "c14", "z=7", "z=8", "z=9", "z=10", "z=11", "z=12", "z=13", "z=14")
    __validLaTeXParticles = ("Neutron", "Proton", "Deuterium", "Tritium", "$^{3}$He", "$^{4}$He",
    "$^{6}$He", "$^{6}$Li", "$^{7}$Li", "$^{8}$Li", "$^{9}$Li", "$^{7}$Be", "$^{9}$Be", "$^{10}$Be",
    "$^{9}$B", "$^{10}$B", "$^{11}$B", "$^{12}$B", "$^{11}$C", "$^{12}$C", "$^{13}$C", "$^{14}$C",
    "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si")
    __numParticleNames = len(__validParticles)
    __fileCommentFlag = "#"
    __axisLims = ("xrange", "yrange", "xscale", "yscale")
    __figLabels = ("xlabel", "ylabel", "title")
    __dataArgs = ("data", "sim", "simlabel", "datalabel")
    __plotArgs = ("particle", "plot", "angle")
    __annotateArgs = ("annotate", "annotatepos", "otherannotate", "otherannotatepos", "otherannotatecolor", "legend")
    __miscArgs = ("comment", "c", "save", "dpi", "show", "override", "scalesim", "scaledata")
    __endArgs = ("end", "quit", "stop", "done", "new")
    __defaultAnnotatePos = 1.0E-2
    __defaultAnnotationColor = "blue"
    __defaultExpLabel = "Exp. Data"
    __defaultXScaling = 1.00
    __defaultYScaling = 1.00

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
        self.__dataLabels = []
        self.__simFiles = []
        self.__simLabels = []
        self.__numDataFiles = 0
        self.__numSimFiles = 0
        self.__numSimLabels = 0
        self.__numDataLabels = 0
        self.__simObjects = []
        self.__numSimObjects = 0
        self.__expObjects = []
        self.__numExpObjects = 0
        # Whether or not to override:
        self.__override = False
        # Scaling of data:
        self.__scaleSimX = []
        self.__scaleSimY = []
        self.__scaleDataX = []
        self.__scaleDataY = []
        self.__numSimScale = 0
        self.__numDataScale = 0

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
        self.__latexParticleID = []
        self.__numParticles = 0
        self.__plotAngles = []
        self.__numAngles = 0
        self.__plotTypes = []
        self.__numPlotTypes = 0
        self.__plotSeveralTypes = True

        # Misc information:
        self.__figDPI = 1200
        self.__showPlot = False

        return

    def __applyPlotLabels(self):
        """Applies the X/Y axis labels and the plot title"""

        # Apply X-axis label specific to the requested plot:
        if ( self.__xLabel == None ):
            self.__xLabel = "No label given!"

        # Apply Y-axis label specific to the requested plot:
        if ( self.__yLabel == None ):
            self.__yLabel = "No label given!"

        # Apply plot title:
        if ( self.__plotTitle == None ):
            self.__plotTitle = "No title given!"


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
        """Plots all lines desired by the user"""

        # Turn off multiple plots if they weren't specified:
        if ( self.__numPlotTypes <= 1 and self.__numParticles <= 1 and self.__numAngles <= 1 ):
            self.__plotSeveralTypes = False
            self.__myPlot.toggleSeveralPlots( self.__plotSeveralTypes )

        # Plot data and simulation lines:
        self.__plotDataLines()   # Note: calling this first allows all legends for the line type to be shown
        self.__plotSimLines()

        # Legend information:
        self.__myPlot.setLegendPos( self.__legendPos, self.__legendPosX, self.__legendPosY )

        return

    def __plotDataLines(self):
        """Plots all data lines requested"""
        # Verify that the number of exp. data labels meets the minimum exp. data objects created
        if ( self.__numDataLabels < self.__numExpObjects ):
            # Warn user:
            self.__write.message = "%d label(s) for experimental data are missing." % (self.__numExpObjects - self.__numDataLabels)
            self.__write.print(1, 2)
            self.__write.message = "   Assuming the label for those sets is \"%s\"." % (self.__defaultExpLabel)
            self.__write.print(1, 2)
            # Append default label:
            for i in range(self.__numDataLabels, self.__numExpObjects, 1):
                self.__dataLabels.append( self.__defaultExpLabel )
                self.__numDataLabels += 1

        # Setup scaling factors for all values not passed in:
        if ( self.__numDataScale < self.__numExpObjects ):
            for i in range(self.__numDataScale, self.__numExpObjects, 1):
                self.__scaleDataX.append( self.__defaultXScaling )
                self.__scaleDataY.append( self.__defaultYScaling )
                self.__numDataScale += 1

        # Create lines:
        for i in range(0, self.__numExpObjects, 1):
            self.__write.message = "Plotting exp. data..."
            self.__write.print(2, 2)

        for expID in range(0, self.__numExpObjects, 1):
            xVals = self.__expObjects[expID].getXValues()
            yVals = self.__expObjects[expID].getYValues()
            dxVals = self.__expObjects[expID].getXError()
            dyVals = self.__expObjects[expID].getYError()

            self.__myPlot.addScatter(xVals, yVals, self.__dataLabels[expID],
            self.__scaleDataX[expID], self.__scaleDataY[expID])
            #self.__myPlot.addErrorBar(xVals, yVals, dxVals, dyVals,
            #self.__dataLabels[expID], self.__scaleDataX[expID], self.__scaleDataY[expID])

        return

    def __plotSimLines(self):
        """Plots all lines desired by the user"""
        __validPlotTypes = ("doubledif", "angleint", "energyint")
        __plotTypeName = ("double differential", "angle integrated", "energy integrated")
        __numValidPlotTypes = len(__validPlotTypes)

        # Ensure the the number of legend labels matches the sim. objects:
        if ( self.__numSimLabels < self.__numSimObjects ):
            self.__write.message = "Only %d simulation labels exist while %d files have been loaded." % (self.__numSimLabels, self.__numSimObjects)
            self.__write.print(1, 2)
            for i in range(self.__numSimLabels, self.__numSimObjects, 1):
                self.__simLabels.append( self.__simLabels[i%self.__numSimLabels] )
            self.__numSimLabels = len(self.__simLabels)

        # Setup scaling factors for all values not passed in:
        if ( self.__numSimScale < self.__numSimObjects ):
            for i in range(self.__numSimScale, self.__numSimObjects, 1):
                self.__scaleSimX.append( self.__defaultXScaling )
                self.__scaleSimY.append( self.__defaultYScaling )
                self.__numSimScale += 1

        for i in range(0, self.__numPlotTypes, 1):
            # Validate plot type, otherwise continue:
            validPlotType = False
            plotTypeIndx = -1
            for j in range(0, __numValidPlotTypes, 1):
                if ( self.__plotTypes[i].startswith(__validPlotTypes[j]) ):
                    validPlotType = True
                    plotTypeIndx = j
                    break
            if ( not validPlotType ):
                self.__write.message = "Invalid plot type specified: %s" % (self.__plotTypes[i])
                self.__write.print(1, 2)
                continue


            # Set angle/plot type for PISA angle/energy intergrated data (stored at angle=361, 362, respectively)
            if ( self.__plotTypes[i].startswith(__validPlotTypes[1]) ):
                # Set to doublediff and apply angle
                if ( self.__numAngles > 0 ):
                    self.__write.message = "Unable to plot angles with %s spectra. Clearing all angles..." % (__plotTypeName[plotTypeIndx])
                    self.__write.print(1, 2)
                self.__plotAngles = []
                self.__plotAngles.append( 361 )
                self.__numAngles = len( self.__plotAngles )
            elif ( self.__plotTypes[i].startswith(__validPlotTypes[2]) ):
                # Set to doublediff and apply angle
                if ( self.__numAngles > 0 ):
                    self.__write.message = "Unable to plot angles with %s spectra. Clearing all angles..." % (__plotTypeName[plotTypeIndx])
                    self.__write.print(1, 2)
                self.__plotAngles = []
                self.__plotAngles.append( 362 )
                self.__numAngles = len( self.__plotAngles )

            # Apply plot:
            if ( self.__plotTypes[i].startswith(__validPlotTypes[0]) or
            self.__plotTypes[i].startswith(__validPlotTypes[1]) or
            self.__plotTypes[i].startswith(__validPlotTypes[2]) ):
                # Plot PISA double differential cross sections:
                self.__write.message = "Plotting %s PISA predictions..." % (__plotTypeName[plotTypeIndx])
                self.__write.print(2, 2)

                # Determine X/Y/Title for plot labeling:
                if ( self.__xLabel == None ):
                    if ( self.__numParticles == 1 ):
                        self.__xLabel = self.__latexParticleID[0]
                    else:
                        self.__xLabel = "Particle"
                    self.__xLabel += " Energy [MeV]"
                if ( self.__yLabel == None ):
                    self.__yLabel = "Cross Section"
                    if ( self.__plotTypes[i].startswith(__validPlotTypes[0]) ):
                        self.__yLabel += " [mb/sr/MeV]"
                    elif ( self.__plotTypes[i].startswith(__validPlotTypes[1]) ):
                        self.__yLabel += " [mb/MeV]"
                    elif ( self.__plotTypes[i].startswith(__validPlotTypes[2]) ):
                        self.__yLabel += " [mb/sr]"
                if ( self.__plotTitle == None ):
                    if ( self.__plotTypes[i].startswith(__validPlotTypes[0]) ):
                        self.__plotTitle = "Double Differential Spectra"
                    elif ( self.__plotTypes[i].startswith(__validPlotTypes[1]) ):
                        self.__plotTitle = "Angle Integrated Spectra"
                    elif ( self.__plotTypes[i].startswith(__validPlotTypes[2]) ):
                        self.__plotTitle = "Energy Integrated Spectra"
                    if ( self.__numParticles == 1 ):
                        self.__plotTitle += " (" + self.__latexParticleID[0]
                    if ( self.__numAngles == 1 and self.__plotTypes[i].startswith(__validPlotTypes[0]) ):
                        self.__plotTitle += " at %.0f$^{\\circ}$)" % (self.__plotAngles[0])
                    else:
                        self.__plotTitle += ")"

                for j in range(0, self.__numParticles, 1):
                    for k in range(0, self.__numAngles, 1):
                        for l in range(0, self.__numSimObjects, 1):
                            # Obtain histogram for each sim. object:
                            thePISAData = self.__simObjects[l].getPISAData()
                            if ( thePISAData == None ):
                                self.__write.message = "No PISA data exists in the simulation file."
                                self.__write.print(2, 2)
                                continue
                            theParticle = thePISAData.getParticle(self.__particles[j])
                            if ( theParticle == None ):
                                self.__write.message = "Data for the %s particle does not exist in the sim file." % (self.__particles[j])
                                self.__write.print(2, 2)
                                continue
                            theHistogram = theParticle.getHistogram( self.__plotAngles[k] )
                            if ( theHistogram == None ):
                                self.__write.message = "No data exists for %s particles at %.2f degrees." % (self.__particles[j], self.__plotAngles[k])
                                self.__write.print(2, 2)
                                continue
                            self.__myPlot.addHistogram(theHistogram.getBinValues(), theHistogram.getDataPoints(), self.__simLabels[l], self.__scaleSimX[l], self.__scaleSimY[1])

                        # Add plot type to distinguish:
                        if ( self.__plotSeveralTypes ):
                            self.__myPlot.addPlotType()

        return

    def __applyAnnotations(self):
        """Applies the primary and all other annotations"""

        if ( not self.__mainAnnotation == None ):
            self.__myPlot.setMainAnnotation( self.__mainAnnotation, self.__mainAnnotationPosX, self.__mainAnnotationPosY)

        # Check that all "other" annotations have a color and position, otherwise use default:
        self.__numOtherAnnotations = len(self.__otherAnnotation)
        numXPos = len(self.__otherAnnotationX)
        numYPos = len(self.__otherAnnotationY)
        numColor = len(self.__otherAnnotationColor)
        # (X positions)
        if ( numXPos < self.__numOtherAnnotations ):
            # Append the default value to the list until the lengths match:
            self.__write.message = "The X-value for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numXPos)
            self.__write.print(1, 2)
            self.__write.message = "  The default X-value (%.3E) will be utilized for these annotations." % (self.__defaultAnnotatePos)
            self.__write.print(1, 2)
            for i in range( numXPos, self.__numOtherAnnotations, 1):
                self.__otherAnnotationX.append( self.__defaultAnnotatePos )
        # (Y positions)
        if ( numYPos < self.__numOtherAnnotations ):
            # Append the default value to the list until the lengths match:
            self.__write.message = "The Y-value for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numYPos)
            self.__write.print(1, 2)
            self.__write.message = "  The default Y-value (%.3E) will be utilized for these annotations." % (self.__defaultAnnotatePos)
            self.__write.print(1, 2)
            for i in range( numYPos, self.__numOtherAnnotations, 1):
                self.__otherAnnotationY.append( self.__defaultAnnotatePos )
        # (colors)
        if ( numColor < self.__numOtherAnnotations ):
            # Append the default color to the list until the lengths match:
            self.__write.message = "The color for the last %d other annotations was not specified." % (self.__numOtherAnnotations-numColor)
            self.__write.print(1, 2)
            self.__write.message = "   The default color, \"%s\", will be used for these annotations." % (self.__defaultAnnotationColor)
            self.__write.print(1, 2)
            for i in range( numColor, self.__numOtherAnnotations, 1):
                self.__otherAnnotationColor.append( self.__defaultAnnotationColor )

        # Apply annotations:
        if ( self.__numOtherAnnotations > 0 ):
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
        self.__myPlot = PlotClass(True, self.__write)

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
        # __dataArgs = ("data", "sim", "simlabel", "datalabel")
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
                # File exists; read data file:
                self.__numDataFiles += 1
                self.__write.message = "   Reading experimental data..."
                self.__write.print(2, 4)
                self.__expObjects.append( Scatter.importData(self.__dataFiles[self.__numDataFiles-1], self.__write) )
                if ( not self.__expObjects[self.__numExpObjects] == None ):
                    self.__numExpObjects += 1
                else:
                    del self.__expObjects[self.__numExpObjects]

        elif ( lineID == self.__dataArgs[1] ):
            # Load simulation data file:
            self.__simFiles.append( lineFlag.strip() )
            self.__numSimFiles += 1
            if ( not fileModule.fileExists( self.__simFiles[ len(self.__simFiles)-1 ] ) ):
                self.__write.message = "File \"%s\" does not exist for reading simulation data from." % (self.__simFiles[self.__numSimFiles])
                self.__write.print(1, 2)
            else:
                self.__simObjects.append( GSMOutput(self.__simFiles[self.__numSimFiles-1], self.__write) )
                self.__numSimObjects += 1

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

        elif ( lineID == self.__dataArgs[3] ):
            # Add custom data labels
            if ( len(lineFlag) > 0 ):
                self.__dataLabels.append( lineFlag.strip() )
                self.__numDataLabels += 1
            else:
                self.__write.message = "No data legend labels given. Ignoring line..."
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
                    # Ensure particle name is valid:
                    validParticle = False
                    particleIndx = 0
                    for j in range(0, self.__numParticleNames, 1):
                        if ( newParticles[i] == self.__validParticles[j] ):
                            validParticle = True
                            particleIndx = j
                            break

                    if ( validParticle ):
                        self.__particles.append( newParticles[i] )
                        self.__latexParticleID.append( self.__validLaTeXParticles[particleIndx] )
                        self.__numParticles += 1
                    else:
                        self.__write.message = "Invalid particle identifier found: %s" % (newParticles[i])
                        self.__write.print(1, 2)

        elif ( lineID == self.__plotArgs[1] ):
            # Plot given; specify plot type:
            plotTypes = fileModule.parseLine( lineFlag.strip().lower() )
            if ( len(plotTypes) > 0 ):
                for i in range(0, len(plotTypes), 1):
                    self.__plotTypes.append( plotTypes[i] )
                    self.__numPlotTypes += 1

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
                if ( angleFloat[i] < 0 ):
                    angleFloat[i] += 360
                    print("Is there a better way to do this?")
                elif ( angleFloat[i] >= 360 ):
                    angleFloat[i] = angleFloat[i] % 360
                self.__plotAngles.append( angleFloat[i] )
                self.__numAngles += 1

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
        # __miscArgs = ("comment", "c", "save", "dpi", "show", "override", "scalesim", "scaledata")

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

        elif ( lineID == self.__miscArgs[6] ):
            # scaleSim: read X and Y scaling:
            parsedLine = fileModule.parseLine( lineFlag )
            numFactors = len(parsedLine)
            if ( numFactors <= 0 ):
                self.__write.message = "No scaling factors provided for scaling simulation data."
                self.__write.print(1, 2)
                self.__write.message = "   No scaling will occur."
                self.__write.print(1, 2)
                xVal = self.__defaultXScaling
                yVal = self.__defaultYScaling
            else:
                # Obtain X value:
                if ( numFactors <= 1 ):
                    self.__write.message = "Scaling of simulation data should contain 2 arguments: %s" % (lineFlag)
                    self.__write.print(1, 2)
                    self.__write.message = "   Assuming given scaling factor is for Y axis..."
                    self.__write.print(1, 2)
                    xVal = self.__defaultXScaling
                    yIndx = 0
                else:
                    yIndx = 1
                    try:
                        xVal = float(parsedLine[0])
                    except:
                        xVal = self.__defaultXScaling
                        self.__write.message = "Unable to convert X scaling factor to float: %s" % (parsedLine[0])
                        self.__write.print(1, 2)
                        self.__write.message = "   X scaling of simulation data will not occur."
                        self.__write.print(1, 2)

                # Obtain Y value:
                try:
                    yVal = float(parsedLine[yIndx])
                except:
                    yVal = self.__defaultYScaling
                    self.__write.message = "Unable to convert Y scaling factor to float: %s" % (parsedLine[yIndx])
                    self.__write.print(1, 2)
                    self.__write.message = "   Y scaling of simulation data will not occur."
                    self.__write.print(1, 2)

            # Apply scaling factors:
            self.__scaleSimX.append ( xVal )
            self.__scaleSimY.append ( yVal )
            self.__numSimScale += 1

        elif ( lineID == self.__miscArgs[7] ):
            # scaleData: read X and Y scaling:
            parsedLine = fileModule.parseLine( lineFlag )
            numFactors = len(parsedLine)
            if ( numFactors <= 0 ):
                self.__write.message = "No scaling factors provided for scaling experimental data."
                self.__write.print(1, 2)
                self.__write.message = "   No scaling will occur."
                self.__write.print(1, 2)
                xVal = self.__defaultXScaling
                yVal = self.__defaultYScaling
            else:
                # Obtain X value:
                if ( numFactors <= 1 ):
                    self.__write.message = "Scaling of experimental data should contain 2 arguments: %s" % (lineFlag)
                    self.__write.print(1, 2)
                    self.__write.message = "   Assuming given scaling factor is for Y axis..."
                    self.__write.print(1, 2)
                    xVal = self.__defaultXScaling
                    yIndx = 0
                else:
                    yIndx = 1
                    try:
                        xVal = float(parsedLine[0])
                    except:
                        xVal = self.__defaultXScaling
                        self.__write.message = "Unable to convert X scaling factor to float: %s" % (parsedLine[0])
                        self.__write.print(1, 2)
                        self.__write.message = "   X scaling of experimental data will not occur."
                        self.__write.print(1, 2)

                # Obtain Y value:
                try:
                    yVal = float(parsedLine[yIndx])
                except:
                    yVal = self.__defaultYScaling
                    self.__write.message = "Unable to convert Y scaling factor to float: %s" % (parsedLine[yIndx])
                    self.__write.print(1, 2)
                    self.__write.message = "   Y scaling of experimental data will not occur."
                    self.__write.print(1, 2)

            # Apply scaling factors:
            self.__scaleDataX.append ( xVal )
            self.__scaleDataY.append ( yVal )
            self.__numDataScale += 1

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

        # Plot all lines requested:
        self.__plotLines()

        # Setup the plot's characteristics:
        self.__applyPlotLabels()
        self.__applyAxisDetails()
        self.__applyAnnotations()

        # Show and save plot:
        if ( self.__showPlot and self.__saveName == None ):
            self.__myPlot.showCurrentPlot()
        if ( not self.__saveName == None ):
            self.__myPlot.savePlot(self.__saveName, self.__figDPI, self.__showPlot, self.__override)
        if ( not self.__showPlot and self.__saveName == None ):
            self.__write.message = "The plot is not being saved or shown (as the input specified)."
            self.__write.print(1, 2)


        # Create new plot object:
        self.__newPlot()

        return
