
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


class PISAPlots:
    """Container for all PISA related plot options"""
    __validPlotTypeFull = ("double differential", "energy integrated", "angle integrated")
    __validPlotTypes = ("doubled", "energyi", "anglei")
    __numValidPlotTypes = len(__validPlotTypes)
    # Regarding valid particles:
    __validParticles = ("n", "p", "d", "t", "he3", "he4", "he6", "li6", "li7", "li8",
    "li9", "be7", "be9", "be10", "b9", "b10", "b11", "b12", "c11", "c12", "c13",
    "c14", "z=7", "z=8", "z=9", "z=10", "z=11", "z=12", "z=13", "z=14")
    __validLaTeXParticles = ("Neutron", "Proton", "Deuterium", "Tritium", "$^{3}$He", "$^{4}$He",
    "$^{6}$He", "$^{6}$Li", "$^{7}$Li", "$^{8}$Li", "$^{9}$Li", "$^{7}$Be", "$^{9}$Be", "$^{10}$Be",
    "$^{9}$B", "$^{10}$B", "$^{11}$B", "$^{12}$B", "$^{11}$C", "$^{12}$C", "$^{13}$C", "$^{14}$C",
    "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si")
    __numValidParticles = len(__validParticles)

    def __init__(self, newPrint=Print() ):
        """Constructor"""
        self.__write = newPrint
        self.__resetMembers()

        return

    def __del__(self):
        """Destructor"""
        self.__resetMembers()
        return

    def __resetMembers(self):
        """Resets all class member-variables"""
        # Indicates double diff, energy int., and angle int.
        self.__plotTypes = []
        self.__plotTypeName = []
        self.__numPlotTypes = 0
        # Indiciates which particles to use:
        self.__particles = []
        self.__partLaTeX = []
        self.__numParticles = 0
        # For angles (regarding double diff spectra)
        self.__angles = []
        self.__numAngles = 0

        return

    def __validateAngle(self, angle):
        """Returns a valid angle (within range [0, 360))."""
        __minAngle = 0
        __maxAngle = 360

        validAngle = angle
        if ( not isinstance(angle, (int, float)) ):
            self.__write.message = "Unable to add angle not of type int or float: ", angle
            self.__write.print(1, 2)
            validAngle = -1
        else:
            # Ensure within range [__minAngle, __maxAngle)
            if ( validAngle < __minAngle ):
                # Increment until valid:
                while(True):
                    if ( validAngle < __minAngle ):
                        validAngle += __maxAngle
                    else:
                        break

            if ( validAngle >= __maxAngle ):
                validAngle = (validAngle % __maxAngle)

        return validAngle

    def isValidPlotType(self, newType):
        """Checks if the plot type is valid or not within the object"""
        isValid = False

        newType = newType.lower().strip()
        for pltIndx in range(0, self.__numValidPlotTypes, 1):
            if ( newType.startswith(self.__validPlotTypes[pltIndx]) ):
                isValid = True
                break

        return isValid

    def isValidParticle(self, newParticle):
        """Checks if the particle is valid for this object"""
        isValid = False

        newParticle = newParticle.lower().strip()
        for parIndx in range(0, self.__numValidParticles, 1):
            if ( newParticle == self.__validParticles[parIndx] ):
                isValid = True
                break

        return isValid

    def findFullPlotName(self, pltName):
        """Returns the full plot's name"""
        newPltName = "?"

        pltName = pltName.lower().strip()
        if ( self.isValidPlotType(pltName) ):
            for pltIndx in range(0, self.__numValidPlotTypes, 1):
                if ( pltName.startswith(self.__validPlotTypes[pltIndx]) ):
                    newPltName = self.__validPlotTypeFull[pltIndx]
                    break

        return newPltName

    def findParLaTeX(self, newParticle):
        """Returns the LaTeX version of the particle"""
        parLaTeX = "?"

        newParticle = newParticle.lower().strip()
        if ( self.isValidParticle(newParticle) ):
            for parIndx in range(0, self.__numValidParticles, 1):
                if ( newParticle == self.__validParticles[parIndx] ):
                    parLaTeX = self.__validLaTeXParticles[parIndx]
                    break

        return parLaTeX

    def addPlotType(self, newType):
        """Adds a plot type"""
        newType = newType.lower().strip()
        if ( self.isValidPlotType(newType) ):
            self.__plotTypes.append( newType )
            self.__plotTypeName.append( self.findFullPlotName(newType) )
            self.__numPlotTypes += 1
        else:
            self.__write.message = "Cannot add an invalid plot type to the PISA object: %s" % (newType)
            self.__write.print(1, 2)

        return

    def addParticle(self, newParticle):
        """Adds a particle to the object"""

        newParticle = newParticle.lower().strip()
        if ( self.isValidParticle(newParticle) ):
            self.__particles.append( newParticle )
            self.__partLaTeX.append( self.findParLaTeX(newParticle) )
            self.__numParticles += 1
        else:
            self.__write.message = "An invalid particle cannot be added to the PISA object: %s" % newParticle
            seslf.__write.print(1, 2)

        return

    def addAngle(self, newAngle):
        """Validates and adds a new angle(s) to the PISA object"""
        newAngles = []
        if ( not isinstance(newAngle, (int, float) ) ):
            # Convert to float or int:
            if ( isinstance(newAngle, (list, tuple)) ):
                # Add values to the newAngles list
                for indx in range(0, len(newAngle), 1):
                    newAngles.append( newAngles[indx] )
            else:
                newAngles.append( newAngle )

            for indx in range(0, len(newAngles), 1):
                try:
                    theAngle = float(newAngles[indx])
                except:
                    self.__write.message = "Unable to convert value to float: ", newAngles[indx]
                    self.__write.print(1, 2)
                    theAngle = None

                if ( theAngle is not None ):
                    theAngle = self.__validateAngle(theAngle)
                    self.__angles.append( theAngle )
                    self.__numAngles += 1
        else:
            newAngle = self.__validateAngle(newAngle)
            self.__angles.append( newAngle )
            self.__numAngles += 1

        return

    def queryNumPlotTypes(self):
        """Returns the number of plot types that exist"""
        return self.__numPlotTypes

    def queryPlotTypes(self, indx = None):
        """Returns the plot types or a single type if a valid index is given"""
        plotTypes = self.__plotTypes

        if ( indx is not None and isinstance(indx, (int, float)) ):
            # Return a specific value:
            if ( indx >= 0 and indx < self.__numPlotTypes ):
                plotTypes = self.__plotTypes[indx]
            else:
                self.__write.message = "Invalid index (%d) for obtaining plot type values." % indx
                self.__write.print(1, 2)

        return plotTypes

    def queryPlotTypeNames(self, indx = None):
        """Returns the plot type full names or a single full name if a valid index is given"""
        pltName = self.__plotTypeName

        if ( indx is not None and isinstance(indx, (int, float)) ):
            # Return a specific value:
            if ( indx >= 0 and indx < self.__numPlotTypes ):
                pltName = self.__plotTypeName[indx]
            else:
                self.__write.message = "Invalid index (%d) for obtaining plot type name." % indx
                self.__write.print(1, 2)

        return pltName

    def queryNumParticles(self):
        """Returns the number of particles"""
        return self.__numParticles

    def queryParticles(self, indx = None ):
        """Returns the list of particles or a single particle if avalid index is given"""
        theParticles = self.__particles

        if ( indx is not None and isinstance(indx, (int, float)) ):
            if ( indx >= 0 and indx < self.__numParticles ):
                theParticles = self.__particles[indx]
            else:
                self.__write.message = "An invalid index (%d) was given when querying the PISA particles." % indx
                self.__write.print(1, 2)

        return theParticles

    def queryParticleLaTeX(self, indx = None ):
        """Returns the LaTeX list of particles or a single particle if avalid index is given"""
        theParticles = self.__partLaTeX

        if ( indx is not None and isinstance(indx, (int, float)) ):
            if ( indx >= 0 and indx < self.__numParticles ):
                theParticles = self.__partLaTeX[indx]
            else:
                self.__write.message = "An invalid index (%d) was given when querying the PISA LaTeX particles." % indx
                self.__write.print(1, 2)

        return theParticles

    def queryNumAngles(self):
        """Returns the number of angles to be used"""
        return self.__numAngles

    def queryAngles(self, indx = None ):
        """Returns the list of angles or a single angle if avalid index is given"""
        theAngles = self.__angles

        if ( indx is not None and isinstance(indx, (int, float)) ):
            if ( indx >= 0 and indx < self.__numAngles ):
                theAngles = self.__angles[indx]
            else:
                self.__write.message = "An invalid index (%d) was given when querying the PISA angles." % indx
                self.__write.print(1, 2)

        return theAngles

    def recommendLineScaling(self):
        """Returns whether or not lines should be scaled"""
        recommended = False
        if ( self.__numAngles > 1 or self.__numParticles > 1 ):
            recommended = True

        return recommended

    def recommendMultiplePlots(self):
        """Returns whether or not multiple plots were requested to be plotted"""
        recommended = False
        if ( self.__numPlotTypes > 1 ):
            recommended = True

        return recommended


class PlotGSMInputFile:
    """Reads an input file and sets values based on input specification."""
    # Input arguments:
    __validParticleDataIDs = ("neutrons", "protons", "deuterons", "tritons",
    "helium-3", "alphas", "neg. pions", "neut pions", "pos. pions")
    __validLaTeXParticleDataIDS = ("Neutron", "Proton", "Deuterium", "Tritium", "$^{3}$He", "$^{4}$He",
    "$\pi^{-}$", "$\pi^{0}$", "$\pi^{+}$")
    __numValidParticleDataIDs = len(__validParticleDataIDs)
    __fileCommentFlag = "#"
    __axisLims = ("xrange", "yrange", "xscale", "yscale")
    __figLabels = ("xlabel", "ylabel", "title")
    __dataArgs = ("data", "sim", "simlabel", "datalabel")
    __plotArgs = ("particle", "plot", "angle", "origin")
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
        self.__myPlot = PlotClass(True, self.__write)
        self.__parseInput()

        return

    def __del__(self):
        """Destructor for the \"PlotInputFile\" class"""
        # self.__resetMembers()

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
        self.__resetPlotObj()
        self.__resetAnnotations()
        self.__resetAxis()
        self.__resetOther()

        return

    def __resetPlotObj(self):
        """Resets the plot object"""
        self.__myPlot = PlotClass(True, self.__write)
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
        # (PISA)
        self.__pisa = PISAPlots(self.__write)
        # (Particle Data)
        self.__particleDataPlot = []
        self.__latexParticleData = []
        self.__numParticleDataPlot = 0
        self.__particleDataOrigins = []
        self.__numParDataOrigins = 0
        # (Misc.)
        self.__plotTypes = []
        self.__numPlotTypes = 0
        self.__plotSeveralTypes = True

        # Misc information:
        self.__figDPI = 1200
        self.__showPlot = False

        return

    def __saveAndClearPlot(self):
        """Clears the plot object of all lines"""
        self.applyPlotSpecificsAndSaveShow()
        self.__resetAxis()

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
        if ( not self.__pisa.recommendLineScaling() and not self.__pisa.recommendMultiplePlots() ):
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

            self.__myPlot.addErrorBar(xVals, yVals, dxVals, dyVals,
            self.__dataLabels[expID], self.__scaleDataX[expID], self.__scaleDataY[expID])

        return

    def __plotSimLines(self):
        """Plots all lines desired by the user"""
        __validPlotTypes = ("energysp")
        __plotTypeName = ("energy spectrum")
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


        # Apply PISA plot(s):
        if ( self.__pisa.queryNumPlotTypes() >= 1 ):
            self.__plotPISA()


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

            if ( self.__plotTypes[i].startswith(__validPlotTypes[0]) ):
                self.__plotEnergySpectrum()

        return

    def __plotPISA(self):
        """Plots all PISA data"""
        __validPlotTypes = ("doubled", "anglei", "energyi")

        for typeIndx in range(0, self.__pisa.queryNumPlotTypes(), 1):

            pltType = self.__pisa.queryPlotTypes(typeIndx)
            pltTypeName = self.__pisa.queryPlotTypeNames(typeIndx)

            # Write to user:
            self.__write.message = "Plotting %s PISA predictions..." % (pltTypeName)
            self.__write.print(2, 2)

            # Determine X/Y/Title for plot labeling:
            if ( self.__xLabel == None ):
                if ( self.__pisa.queryNumParticles() == 1 ):
                    self.__xLabel = self.__pisa.queryParticleLaTeX(0)
                else:
                    self.__xLabel = "Particle"
                self.__xLabel += " Energy [MeV]"
            if ( self.__yLabel == None ):
                self.__yLabel = "Cross Section"
                if ( pltType.startswith(__validPlotTypes[0]) ):
                    self.__yLabel += " [mb/sr/MeV]"
                elif ( pltType.startswith(__validPlotTypes[1]) ):
                    self.__yLabel += " [mb/MeV]"
                elif ( pltType.startswith(__validPlotTypes[2]) ):
                    self.__yLabel += " [mb/sr]"
            if ( self.__plotTitle == None ):
                if ( pltType.startswith(__validPlotTypes[0]) ):
                    self.__plotTitle = "Double Differential Spectra"
                    if (   self.__pisa.queryNumParticles()  > 1 and self.__pisa.queryNumAngles() == 1 ):
                        self.__plotTitle += " (at %.0f$^{\\circ}$)" % ( self.__pisa.queryAngles(0) )
                    elif ( self.__pisa.queryNumParticles() == 1 and self.__pisa.queryNumAngles() == 1 ):
                        self.__plotTitle += " (%s at %.0f$^{\\circ}$)" % ( self.__pisa.queryParticleLaTeX(0), self.__pisa.queryAngles(0) )
                    elif ( self.__pisa.queryNumParticles() == 1 and self.__pisa.queryNumAngles()  > 1 ):
                        self.__plotTitle += " (%s)" % ( self.__pisa.queryParticleLaTeX(0) )
                elif ( pltType.startswith(__validPlotTypes[1]) ):
                    self.__plotTitle = "Angle Integrated Spectra"
                elif ( pltType.startswith(__validPlotTypes[2]) ):
                    self.__plotTitle = "Energy Integrated Spectra"

            # Set angle information:
            numAngles = self.__pisa.queryNumAngles()
            theAngles = self.__pisa.queryAngles()
            if ( not pltType.startswith(__validPlotTypes[0]) ):
                # Use only one angle (361 or 362) for energy/angle integrated plots:
                if ( pltType.startswith(__validPlotTypes[1]) ):
                    theAngles = [361]
                else:
                    theAngles = [362]
                numAngles = 1

            # Loop over various angles/particles now:
            for parIndx in range(0, self.__pisa.queryNumParticles(), 1):
                theParticle = self.__pisa.queryParticles(parIndx)
                theParticleLaTeX = self.__pisa.queryParticleLaTeX(parIndx)

                for angIndx in range(0, numAngles, 1):
                    # Use special angles for angle/energy integrated spectra:
                    theAngle = theAngles[angIndx]
                    for simIndx in range(0, self.__numSimObjects, 1):
                        # Obtain histogram for each sim. object:
                        theHistogram = self.__simObjects[simIndx].getPISAParticleHistogram(theParticle, theAngle)

                        if ( theHistogram is not None ):
                            self.__myPlot.addHistogram(theHistogram.getBinValues(), theHistogram.getDataPoints(), self.__simLabels[simIndx], self.__scaleSimX[simIndx], self.__scaleSimY[simIndx])
                        else:
                            self.__write.message = "No PISA histogram exists for the specified plot of %s particles." % theParticleLaTeX

                    # Add plot type to distinguish:
                    if ( self.__plotSeveralTypes and numAngles > 1):
                        self.__myPlot.addPlotType()

                # Add plot type to distinguish:
                if ( self.__plotSeveralTypes and self.__pisa.queryNumParticles() > 1):
                    self.__myPlot.addPlotType()

            # Save plot and create new figure object to save:
            if ( self.__pisa.queryNumPlotTypes() > 1 ):
                self.__override = False
            self.__saveAndClearPlot()

        return

    def __plotEnergySpectrum(self):
        """Plots the energy spectrum given the input"""

        self.__write.message = "Creating energy spectrum plot..."
        self.__write.print(2, 2)

        # Plot energy spectrum for each particle requested and each type:
        for partIndx in range(0, self.__numParticleDataPlot, 1):
            theParticle = self.__particleDataPlot[partIndx]
            for origIndx in range(0, self.__numParDataOrigins, 1):
                theOrigin = self.__particleDataOrigins[origIndx]
                for dataObj in range(0, self.__numSimObjects, 1):
                    # Obtain histogram from the output file:
                    theHistogram = self.__simObjects[dataObj].getParticleLabeledEnergySpectra(theParticle, theOrigin)

                    if ( theHistogram == None ):
                        continue

                    if ( theHistogram.queryLargestValue() <= 0.00 ):
                        self.__write.message = "No %s values exist for %s particles." % (theOrigin, theParticle)
                        self.__write.print(1, 2)
                        continue

                    self.__myPlot.addHistogram(theHistogram.queryBinBounds(),
                    theHistogram.queryYValues(), self.__simLabels[dataObj],
                    self.__scaleSimX[dataObj], self.__scaleSimY[dataObj])

                if ( self.__plotSeveralTypes and self.__numParDataOrigins > 1 ):
                    self.__myPlot.addPlotType()

            if ( self.__plotSeveralTypes and self.__numParticleDataPlot > 1 ):
                self.__myPlot.addPlotType()

        self.__saveAndClearPlot()

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
        self.__resetPlotObj()

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
        # __plotArgs = ("particle", "plot", "angle". "origin")
        foundFlag = True

        if ( lineID == self.__plotArgs[0] ):
            # Particle given; plot for a particle:
            newParticles = fileModule.parseLine( lineFlag.strip().lower() )
            if ( len(newParticles) > 0 ):
                for i in range(0, len(newParticles), 1):
                    # Ensure particle name is valid:
                    validParticle = self.__pisa.isValidParticle( newParticles[i] )

                    if ( validParticle ):
                        self.__pisa.addParticle( newParticles[i] )
                    else:
                        # Check if particle in particleData array:
                        validParticle = False
                        particleIndx = 0
                        for j in range(0, self.__numValidParticleDataIDs, 1):
                            if ( newParticles[i] == self.__validParticleDataIDs[j] ):
                                particleIndx = j
                                validParticle = True
                                break
                        if ( validParticle ):
                            self.__particleDataPlot.append( self.__validParticleDataIDs[j] )
                            self.__latexParticleData.append( self.__validLaTeXParticleDataIDS[j] )
                            self.__numParticleDataPlot += 1
                        else:
                            self.__write.message = "Invalid particle identifier found: %s" % (newParticles[i])
                            self.__write.print(1, 2)

        elif ( lineID == self.__plotArgs[1] ):
            # Plot given; specify plot type:
            plotTypes = fileModule.parseLine( lineFlag.strip().lower() )
            if ( len(plotTypes) > 0 ):
                for i in range(0, len(plotTypes), 1):
                    isValid = self.__pisa.isValidPlotType( plotTypes[i] )

                    if ( isValid ):
                        self.__pisa.addPlotType( plotTypes[i] )
                    else:
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
                self.__pisa.addAngle( angleFloat[i] )

        elif ( lineID == self.__plotArgs[3] ):
            # Plot based on origin (total, cascade, etc.)
            originFlags = fileModule.parseLine( lineFlag )
            for i in range(0, len(originFlags), 1):
                self.__particleDataOrigins.append( originFlags[i] )
                self.__numParDataOrigins += 1

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

        # Create new plot object:
        self.__newPlot()

        return

    def applyPlotSpecificsAndSaveShow(self):
        """Applies plot labels, axes, and annotations"""
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

        self.__resetPlotObj()

        return
