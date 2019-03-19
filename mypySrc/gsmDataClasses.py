
################################################################################
# File documentation:
"""
This module contains the various data classes that store information from CEM,
GSM, and LAQGSM simulations.

USAGE (example):
   totalPISAData = DoubleDiffPISA()   # Initialize object to contain all PISA data

   for i in range(0, numParticles, 1):
       # Find a particle's PISA data table; create object to contain all PISA data for that particle:
       thisParticle = ParticlePISAData( myParticleName )

       # Obtain histogram data for an object; then initialize histogram object with its data (repeat for all histograms)
       for j in range(0, numHistograms, 1):
           thisHistogram = Histogram("Double differential", "Some random note", binBoundaries, binValues)

           # Add the histogram data to the collection for that particle:
           thisParticle.addHistogram( thisHistogram )

       # Append the particle's collection of histograms to the object:
       thisPISAData.addParticle( thisParticle )

   # Obtain the appropriate histogram data now (from within the layers)
   plottedParticle = totalPISAData.getParticle( someParticleName ) # Returns a class that contains all that particle's PISA data
   theDesiredHistogram = plottedParticle.getHistogram( queryByLabel )



   # Plot desired histograms data:
   someLabel = "A cool histogram!"
   plot.addHistogram( theDesiredHistogram.getBinValues(), theDesiredHistogram.getBinValues(), someLabel)


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

# MODULES:
import generalPlotTypeClasses as genPlotCls
from fileModule import parseLine
from printClass import Print

# VERSION Number:
__version__ = "1.0.0"


# Module defaults:
# (PISA Data)
particleTypes = ("n", "p", "d", "t", "he3", "he4", "he6", "li6", "li7", "li8",
"li9", "be7", "be9", "be10", "b9", "b10", "b11", "b12", "c11", "c12", "c13",
"c14", "z=7", "z=8", "z=9", "z=10", "z=11", "z=12", "z=13", "z=14")
numParticleTypes = len( particleTypes )

histType = ("double differential", "energy integrated", "angle integrated")
numHistTypes = len(histType)


class Histogram:
    """Stores particle data in histogram form"""

    def __init__(self, type, angle, bins, values, newPrint = Print() ):
        """Constructor for class"""
        self.__write = newPrint

        # Reset Histogram values:
        self.__angle = 0
        self.__type = None
        self.__dataPoints = []
        self.__numDataPoints = 0
        self.__binValues = []
        self.__numBins = 0

        # Set type of histogram data (double differential, energy integrated, angle integrated)
        validType = False
        typeIndx = 0
        for i in range(0, numHistTypes, 1):
            if ( type.strip().lower() == histType[ i ] ):
                validType = True
                typeIndx = i
                break
        if ( validType ):
            self.__type = histType[ typeIndx ]
        else:
            self.__write.message = "Invalid histogram type detected (\"%s\"). Using \"%s\" instead." % (type, histType[ typeIndx ])
            self.__write.print(1, 3)
            self.__type = histType[ typeIndx ]

        # Set angle for the plot:
        try:
            self.__angle = float(angle)
        except:
            # Data is either invalid; assume angle = 0
            self.__write.message = "Unable to convert angle parameter (%s) to a float. Assuming angle integrated." % ( str(angle) )
            self.__write.print(1, 2)
            self.__angle = 361

        # Ensure valid angle value (in range [0, 360) )
        if ( (not self.__angle == 361) and (not self.__angle == 362) ):
            if ( self.__angle < 0 ):
                self.__angle += 360
            elif ( self.__angle >= 360 ):
                self.__angle -= 360

        # Verify that bins and values are lists:
        validBins   = isinstance(bins,   list)
        validValues = isinstance(values, list)
        if ( (not validBins) or (not validValues) ):
            self.__write.message = "Invalid bins or values passed in to Histogram object. Parameters must be lists."
            self.__write.print(0, 1)
            return

        # Convert to floats:
        for i in range(0, len(bins), 1):
            try:
                bins[i] = float( bins[i] )
            except:
                self.__write.message = "Unable to convert bin boundary (%s) to float. Assuming value is 0." % ( str(bins[i]) )
                self.__write.print(1, 2)
                bins[i] = 0
        for i in range(0, len(values), 1):
            try:
                values[i] = float( values[i] )
            except:
                self.__write.message = "Unable to convert bin boundary (%s) to float. Assuming value is 0." % ( str(values[i]) )
                self.__write.print(1, 2)
                values[i] = 0

        # Ensure only positive values (for bins, values)
        # (Check for bins, shift all values up for non-physical values)
        shiftValue = 0
        badBinBound = 0
        for i in range(0, len(values), 1):
            shiftValue = min(shiftValue, values[i])
            badBinBound = min(badBinBound, values[i])
        shiftValue = abs(shiftValue)
        if ( shiftValue > 0 ):
            self.__write.message = "Unphysical lowest bin boundary (%f). Shifting all values up by (%f)." % (badBinBound, shiftValue)
            self.__write.print(0, 1)
        for i in range(0, len(values), 1):
            values[i] += shiftValue
        # (Do same for bins)
        if ( bins[0] < 0 ):
            shiftValue = -bins[0]
            self.__write.message = "Unphysical lower bin boundary (%f). Shifting all values up by (%f)." % (bins[0], shiftValue)
            self.__write.print(0, 1)
        else:
            shiftValue = 0
        for i in range(0, len(bins), 1):
            bins[i] = shiftValue + bins[i]

        # Determine how many values to use (only accept minimum of what given data allows)
        numValues = min( len(values), (len(bins)-1) )

        # Set bin values:
        self.__binValues.append( bins[0] )   # Append bin start:
        for i in range(1, (numValues+1), 1):
            # Ensure bin value is larger than last:
            if ( bins[i] < bins[i-1] ):
                self.__write.message = "The bin has smaller value than previous (range [%.2f, %.2f)). Setting bin width to 0..." % (bins[i-1], bins[i])
                self.__write.print(1, 3)
                bins[i] = bins[i-1]
            self.__binValues.append( bins[i] )
        self.__numBins = len( self.__binValues )


        # Valid particle was found, now set data:
        for i in range(0, numValues, 1):
            self.__dataPoints.append( values[i] )
        self.__numDataPoints = len( self.__dataPoints )

        return

    def appendDataPoint(self, newDataPoint, binValue):
        """Appends a data point to the end of the histogram"""
        # Check for errors:
        if ( newDataPoint < 0 ):
            self.__write.message = "Invalid data point (%f) given. Setting to 0..." % (newDataPoint)
            self.__write.print(1, 3)
            newDataPoint = 0
        if ( binValue < self.__binValues[ self.__numBins ] ):
            self.__write.message = "Invalid end-bin value (%f) given. Setting to 5 more than last bin..." % (binValue)
            self.__write.print(1, 3)
            binValue = self.__binValues[ self.__numBins ] + 5
        if ( len(self.__binValues) == 0 ):
            # No bins have been set; start at 0 for user:
            self.__write.message = "No starting bin value was established. Assuming 0..."
            self.__write.print(1, 3)
            self.__binValues.append( 0 )

        # Set values:
        self.__dataPoints.append( newDataPoint )
        self.__numDataPoints += 1
        self.__binValues.append( binValue )
        self.__numBins += 1

        return

    def getDataPoints(self):
        """Returns the data points for the histogram object"""
        return self.__dataPoints

    def getBinValues(self):
        """Returns the bin values for the histogram object"""
        return self.__binValues

    def getNumDataPoints(self):
        """Returns the number of data points that exist in the particle"""
        return self.__numDataPoints

    def getNumBins(self):
        """Returns the number of bins that exist in the particle"""
        return self.__numBins

    def getAngle(self):
        """Returns the angle (<360, or 361 for angle int. and 362 for energy int.) of the histogram data"""
        return self.__angle

    def getType(self):
        """Returns the type of histogram"""
        return self.__type


class ParticlePISAData:
    """Class that stores PISA data for each particle (many histogram data points)"""
    # Data contained here includes all double differential cross sections,
    # angle integrated cross sections, and energy integrated cross sections.

    def __init__(self, particleName, newPrint = Print() ):
        """Constructor for particle PISA data"""
        self.__write = newPrint
        self.__particleName = None
        self.__histData = []
        self.__numHistograms = 0

        # Verify particle name:
        validParticle = False
        for i in range(0, numParticleTypes, 1):
            if ( particleName == particleTypes[ i ] ):
                validParticle = True
                break

        # If validparticle found, then store, else print warning:
        if ( validParticle ):
            self.__particleName = particleName
        else:
            self.__write.message = "Invalid particle ID (%s) used for ParticlePISAData construction." % (particleName)
            self.__write.print(1, 2)

        return

    def __validateHistogramIndex(self, i):
        """Checks for valid index in histogram array"""
        if ( i < 0 ):
            return False
        elif( i >= self.__numHistograms ):
            return False
        else:
            return True

    def getParticleName(self):
        """Returns the particle name to the user/client"""
        return self.__particleName

    def addHistogram(self, newHistogram ):
        """Add a histogram to the particle type"""
        if ( isinstance(newHistogram, Histogram) ):
            self.__histData.append( newHistogram )
            self.__numHistograms += 1
        else:
            self.__write.message = "Incorrect parameter instance cannot be added (should be histogram)"
            self.__write.print(1, 2)

        return

    def getHistogram(self, someAngle):
        """Returns a histogram to the user with the corresponding label"""
        # Check if any histograms exist:
        if ( self.__numHistograms <= 0 ):
            self.__write.message = "No PISA-type histograms exist for \"%s\" particles in general." % (self.__particleName)
            self.__write.print(1, 2)
            return None

        # Migrate angle to float:
        if ( not isinstance(someAngle, (float, int)) ):
            try:
                someAngle = float(someAngle)
            except:
                self.__write.message = "Invalid angle type passed in. Should be numerical; assuming value of 0."
                self.__write.print(1, 2)
                someAngle = 0.0

        # Return histogram (for string, int)
        if ( isinstance(someAngle, (float, int)) ):
            # Look for histogram matching the passed in label:
            foundLabel = False
            associatedHist = 0
            # Reduce angle within range [0, 360)
            if ( someAngle < 0 ):
                someAngle += 360
            elif ( someAngle >= 360 ):
                if ( (not someAngle == 361) and (not someAngle == 362) ):
                    someAngle -= 360

            for i in range(0, self.__numHistograms, 1):
                if ( self.__histData[i].getAngle() == someAngle ):
                    foundLabel = True
                    associatedHist = i
                    break

            # If matching histogram found, return it:
            if ( foundLabel ):
                self.__write.message = "Histogram for particle \"%s\" found at angle \"%.2f\"" % (self.__particleName, someAngle)
                self.__write.print(2, 4)
                self.__write.message = "   Contains %d data points." % (self.__histData[associatedHist].getNumDataPoints() )
                self.__write.print(2, 4)
                someVals = self.__histData[ associatedHist ].getBinValues()
                return self.__histData[ associatedHist ]
            else:
                self.__write.message = "No histogram for particle \"%s\" with matching angle (%.2f) found." % (self.__particleName, someAngle)
                self.__write.print(2, 4)
                return None
        else:
            # Invalid label, warn user
            self.__write.message = "Invalid label type passed in (" + str(someAngle) + "), should be 'float'. Cannot return PISA histogram object."
            self.__write.print(1, 2)
            return None

        return None


class DoubleDiffPISA:
    """Data for when the PISA card is used in CEM and GSM"""
    # This data contains double differential cross sections (dSigma/dOmega/dE),
    # energy integrated and angle integrated cross sections (dSigma/dE, dSigma/dOmega)
    #
    # This information can be obtained for MANY particle types (see 'outputClass.py').
    # For each particle, the data is as follows:
    #
    # Double Differential Cross Sections [mb/sr/MeV]
    # ---Up to 10 angles can be used
    # ---Energy bins [histogram]
    # For this, the values are needed (n values) in addition to the bins (n+1 values).

    def __init__(self, newPrint = Print() ):
        """Class constructor"""
        self.__write = newPrint
        self.__particleData = []
        self.__numParticles = 0

        return

    def addParticleHistogram(self, particleID, newHistogram):
        """Adds a new histogram to the specified particle ID"""
        # Verify valid particleID was specified:
        validParticleID = False
        for i in range(0, numParticleTypes, 1):
            if ( particleID == particleTypes[i] ):
                validParticleID = True
                break
        if ( not validParticleID ):
            self.__write.message = "An invalid particle ID (%s) was specified when adding a histogram." % particleID
            self.__write.print(1, 2)
            self.__write.message = "   The histogram will not be added."
            self.__write.print(1, 2)
            return

        # See if particle exists in current set of particles:
        particleDataExists = False
        particleIndx = -1
        if ( self.__numParticles > 0 ):
            for i in range(0, self.__numParticles, 1):
                if ( particleID == self.__particleData[i].getParticleName() ):
                    particleDataExists = True
                    particleIndx = i
                    break

        # Add the histogram to the particle (or create new particle and add histogram)
        if ( particleDataExists ):
            self.__particleData[particleIndx].addHistogram( newHistogram )
        else:
            self.addParticle( ParticlePISAData(particleID, self.__write) )
            self.addParticleHistogram( particleID, newHistogram )

        return

    def addParticle(self, newParticleHist):
        """Adds a particle's histogram data to the class"""
        if ( isinstance(newParticleHist, ParticlePISAData) ):
            self.__particleData.append ( newParticleHist )
            self.__numParticles += 1
        else:
            self.__write.message = "Can only add particle's PISA histogram sets."
            self.__write.print(1, 2)

        return

    def __verifyParticleExists(self, i):
        """Verifies that the particle exists in the array"""
        if ( i < 0 ):
            self.__write.message = "Index out of bounds (low) in PISA histogram data."
            self.__write.print(1, 3)
            return False
        elif ( i >= self.__numParticles ):
            self.__write.message = "Index out of bounds (high) in PISA histogram data."
            self.__write.print(1, 3)
            return False
        else:
            return True

    def getParticle(self, particleID):
        """Returns a particle with the particle ID given"""
        # Reduced particleID:
        particleID = particleID.lower().strip()
        # Determine if any particles exist in array:
        if ( self.__numParticles <= 0 ):
            # No particles exist, warn and return
            self.__write.message = "No particles exist to return. Returning an empty particle."
            self.__write.print(1, 2)
            return None

        # Handle for strings:
        if ( isinstance(particleID, str) ):
            # Validate particle ID:
            validParticle = False
            for i in range(0, numParticleTypes, 1):
                if ( particleID == particleTypes[i] ):
                    validParticle = True
                    break

            # If valid particle found, check for particle histogram in data set:
            if ( not validParticle ):
                # Requested particle isn't valid; warn user
                self.__write.message = "An invalid particle ID was requested (%s). Cannot return a particle." % (particleID)
                self.__write.print(1, 2)
                return None

            # Now find if particle exists in data set:
            foundParticle = False
            particleIndx = -1
            for i in range(0, self.__numParticles, 1):
                if ( self.__particleData[ i ].getParticleName() == particleID ):
                    foundParticle = True
                    particleIndx = i
                    break

            # Return particle:
            if ( foundParticle ):
                return self.__particleData[ particleIndx ]
            else:
                self.__write.message = "Particle \"%s\" has no data."
                self.__write.print(1, 1)
                return None

        elif ( isinstance(particleID, int) ):
            # Handle for integers:
            validIndex = self.__verifyParticleExists( particleID )
            if ( validIndex ):
                return self.__particleData[ particleID ]
            else:
                return None
        else:
            # Invalid parameter type used:
            self.__write.message = "Invalid parameter type passed in for obtaining particle PISA data (%s)" % ( str(particleID) )
            self.__write.print(1, 2)
            return None

        return None

    def getParticleHistogram(self, particleID, someAngle):
        """Returns a histogram matching the particle ID and the angle specified"""
        theParticleObj = self.getParticle( particleID )
        if ( theParticleObj == None ):
            theHistogram = None
        else:
            theHistogram = theParticleObj.getHistogram( someAngle )
        return theHistogram

    def getNumParticles(self):
        """Returns the number of particles that exist in the object"""
        return self.__numParticles


class ParticleEnergySpectra:
    """The \"EnergySpectra\" class is mainly a histogram flagged by production
    type (\"Total\", \"Cascade\", \"Precompound\", and \"Total Evaporation\")
    containing a histogram for each production type for a single particle.
    """
    __particleIDs = ("neutrons", "protons", "deuterons", "tritons",
    "helium-3", "alphas", "neg. pions", "neut pions", "pos. pions")
    __numParticleIDs = len(__particleIDs)
    __histogramFlags = ("total", "cascade", "coalescence", "precompound", "evaporation")
    __numHistoFlags = len(__histogramFlags)

    def __init__(self, particleID, newPrint=Print() ):
        """Constructor for the class"""

        # Set default values:
        self.__write = newPrint
        self.__resetMembers()
        self.__constructed = True

        # Set particle name:
        particleID = particleID.lower().strip()
        for partIndx in range(0, self.__numParticleIDs, 1):
            if ( particleID == self.__particleIDs[partIndx] ):
                self.__particleID = particleID
                break
        if ( self.__particleID is None ):
            self.__write.message = "An invalid particle identifier (\"%s\") was used when creating a particle's energy spectra."
            self.__write.print(1, 2)
            self.__constructed = False

        return

    def __del__(self):
        """Deconstructor for the class"""
        self.__resetMembers()
        return

    def __resetMembers(self):
        """Resets all member variables of the object"""

        self.__constructed = False

        # Particle information:
        self.__particleID = None
        # Histogram information:
        self.__partHistograms = []
        self.__numHistograms = 0

        return

    def addHistogram(self, newHistogram):
        """Adds a histogram to the object"""
        validHisto = False
        if ( isinstance(newHistogram, genPlotCls.Histogram) ):
            # Verify histogram has a note consistent with the object:
            newHistoNote = newHistogram.queryNote().lower().strip()
            for flagIndx in range(0, self.__numHistoFlags, 1):
                if ( self.__histogramFlags[flagIndx] in newHistoNote ):
                    validHisto = True
                    break
            if ( not validHisto ):
                self.__write.message = "The histogram has a note inconsistent with this object: %s" % (newHistoNote)
                self.__write.print(1, 2)
                self.__write.message = "   The histogram will not be added to the object."
                self.__write.print(1, 2)
        else:
            self.__write.message = "Invalid parameter type for adding a histogram."
            self.__write.print(1, 2)

        if ( validHisto ):
            self.__partHistograms.append( newHistogram )
            self.__numHistograms += 1

        return

    def queryParticleID(self):
        """Returns the particle ID"""
        return self.__particleID

    def queryHistogram(self, histFlag=__histogramFlags[0]):
        """Returns a histogram with the given flag"""
        theHistogram = None

        # Validate desired histogram flag:
        validFlag = False
        histFlag = histFlag.lower().strip()
        for flagIndx in range(0, self.__numHistoFlags, 1):
            if ( self.__histogramFlags[flagIndx] in histFlag ):
                validFlag = True
                break

        # Search for histogram with the given flag:
        if ( validFlag ):
            containsHist = False
            for histIndx in range(0, self.__numHistograms, 1):
                if ( histFlag == self.__partHistograms[histIndx].queryNote().lower().strip() ):
                    containsHist = True
                    theHistogram = self.__partHistograms[histIndx]
                    break
            if ( not containsHist ):
                self.__write.message = "The histogram with flag \"%s\" does not exist within the %s particle's energy spectra." % (histFlag, self.__particleID)
                self.__write.print(1, 2)
        else:
            self.__write.message = "An invalid histogram flag (\"%s\") was used for querying the %s's histogram's energy spectra." % (histFlag, self.__particleID)
            self.__write.print(1, 2)

        return theHistogram


class ParticleData:
    """The \"ParticleData\" object contains information printed by CEM and GSM
    for the printed particle. This includes energy spectra and other misc.
    information
    """
    __particleIDs = ("neutrons", "protons", "deuterons", "tritons",
    "helium-3", "alphas", "neg. pions", "neut pions", "pos. pions")
    __numParticleIDs = len(__particleIDs)

    def __init__(self, particleID, newPrint = Print() ):
        """Constructor for object"""

        # Set defaults:
        self.__write = newPrint
        self.__resetMembers()

        # Set particle ID:
        self.__setParticleID(particleID)
        self.__resetObjects()
        self.__constructed = True

        if ( self.__particleID is None ):
            self.__constructed = False

        return

    def __del__(self):
        """Destructor for object"""
        self.__resetObjects()
        self.__resetMembers()
        return

    def __resetMembers(self):
        """Resets all members of the object"""
        self.__particleID = None
        self.__fileData = []
        self.__dataLen = 0

        return

    def __resetObjects(self):
        """Resets all internal objects"""
        self.__energySpectra = ParticleEnergySpectra( self.__particleID, self.__write)

        return

    def __setParticleID(self, particleID):
        """Sets the object's particle ID"""
        # Validate input:
        validID = False
        particleID = particleID.lower().strip()
        for partIndx in range(0, self.__numParticleIDs, 1):
            if ( particleID == self.__particleIDs[partIndx] ):
                validID = True
        if ( validID ):
            self.__particleID = particleID
        else:
            self.__write.message = "Invalid particle ID (\"%s\") was specified." % (particleID)
            self.__write.print(1, 2)
            self.__write.message = "   Unable to create particle data object."
            self.__write.print(1, 2)

        return

    def __parseData(self, start, end):
        """Parses out file data from the start and end indices"""
        __energySpecFlag = ("energy spectrum [mb/mev]", "integrated:")

        if ( start < 0 ):
            start = 0
        if ( end > self.__dataLen ):
            end = self.__dataLen

        energyData = []
        for lineIndx in range(start, end, 1):
            theline = self.__fileData[lineIndx]

            if ( __energySpecFlag[0] in theline ):
                # Add energy data:
                lineIndx += 2
                while( True ):
                    lineIndx += 1
                    theline = self.__fileData[lineIndx]

                    # Determine if at end of data:
                    stopFlag = False
                    if ( __energySpecFlag[1] in theline ):
                        stopFlag = True

                    if ( stopFlag ):
                        break
                    else:
                        energyData.append( theline )

                # Now create energy spectra object:
                self.__parseEnergySpectraData(energyData)

        return

    def __parseEnergySpectraData(self, data):
        """Parses out data for energy spectra"""

        # Remove "MeV" from the first line:
        header = data[0]
        header = header[ header.find("[mev]") + len("[mev]") : ].strip()
        if ( "pion" in self.__particleID ):
            numHeaders = 1
            headerFlags = ("total", "cascade")
        else:
            numHeaders = 4
            if ( "neutrons" == self.__particleID or "protons" == self.__particleID ):
                headerFlags = ("total", "cascade", "precompound", "evaporation")
            else:
                headerFlags = ("total", "coalescence", "precompound", "evaporation")

        del data[0]
        dataLen = len(data)
        myBins = []
        numBins = 0
        numHistograms = 2 * numHeaders
        myVals = [[] for i in range(0, numHeaders, 1)]
        myErrs = [[] for i in range(0, numHeaders, 1)]
        for lineIndx in range(0, dataLen, 1):
            theline = data[lineIndx]

            if ( theline == "" ):
                break

            # Get lower and upper bin bounds:
            lowerBin = theline[ : theline.find("-") ]
            theline = theline[ theline.find("-") + 1 : ]
            theline = parseLine( theline )
            upperBin = theline[0]
            del theline[0]
            # Remove all +/- flags:
            delIndx = []
            for i in range(0, len(theline), 1):
                if ( theline[i] == "+/-" ):
                    delIndx.append( i )
            for i in range(len(delIndx)-1, -1, -1):
                del theline[ delIndx[i] ]

            # Convert all values to floats:
            try:
                lowerBin = float(lowerBin)
            except:
                self.__write.message = "Could not convert lower bin to float: %s" % lowerBin
                self.__write.print(1, 2)
                lowerBin = 0.00
            try:
                upperBin = float(upperBin)
            except:
                self.__write.message = "Could not convert lower bin to float: %s" % upperBin
                self.__write.print(1, 2)
                upperBin = 0.00
            for i in range(0, len(theline), 1):
                try:
                    theline[i] = float(theline[i])
                except:
                    self.__write.message = "Could not convert lower bin to float: %s" % theline[i]
                    self.__write.print(1, 2)
                    theline[i] = 0.00

            # Set bin values:
            if ( numBins == 0 ):
                myBins.append( lowerBin )
            else:
                if ( not lowerBin == myBins[numBins] ):
                    # Gap in histogram; add bin and values:
                    myBins.append( lowerBin )
                    numBins += 1

                    for valIndx in range(0, numHeaders, 1):
                        myVals[valIndx].append( 0.00 )
                        myErrs[valIndx].append( 0.00 )
            myBins.append( upperBin )
            numBins += 1

            # Set histogram values:
            for histIndx in range(0, numHeaders, 2):
                myVals[histIndx].append( theline[histIndx] )
                myErrs[histIndx].append( theline[histIndx] )

        # Now set histograms (bins and values exist)
        for histIndx in range(0, numHeaders, 1):
            # Create histogram object with desired label:
            parHist = genPlotCls.Histogram(myBins, myVals[histIndx], headerFlags[histIndx], self.__write)
            errHist = genPlotCls.Histogram(myBins, myErrs[histIndx], "d" + headerFlags[histIndx], self.__write)
            self.__energySpectra.addHistogram( parHist )
            self.__energySpectra.addHistogram( errHist )

        return

    def addFileData(self, fileData):
        """Adds data to the file and parses it"""
        if ( not isinstance(fileData, list) ):
            self.__write.message = "File data must be a list of strings. Cannot parse data."
            self.__write.print(1, 2)
            return

        # Reduce file data:
        startingIndx = self.__dataLen
        for lineIndx in range(0, len(fileData), 1):
            fileData[lineIndx] = fileData[lineIndx].lower().strip()
            self.__fileData.append( fileData[lineIndx] )
            self.__dataLen += 1
        endingIndx = self.__dataLen

        self.__parseData(startingIndx, endingIndx)

        return

    def queryParticleID(self):
        """Returns the particle ID to client"""
        return self.__particleID

    def queryEnergySpectra(self):
        """Returns the energy spectra object"""
        return self.__energySpectra

    def queryEnergySpectraHistogram(self, label):
        """Returns the energy spectrum for the particle with a specific label"""
        theHistogram = self.__energySpectra.queryHistogram(label)
        if ( theHistogram == None ):
            self.__write.message = "No %s energy spectrum histogram exists for particle %s." % (label, self.__particleID)
            self.__write.print(1, 2)
        return theHistogram

    def parseFileData(self, newFileData ):
        """Parses the information given lines of a file"""
        if ( not isinstance(newFileData, list) ):
            self.__write.message = "The file data passed in must be a list."
            self.__write.print(1, 2)
            self.__write.message = "   Unable to parse data."
            self.__write.print(1, 2)
            return

        # Bring all data to lower case and remove empty lines:
        fileData = []
        for lineIndx in range(0, len(newFileData), 1):

            newFileData[lineIndx] = newFileData[lineIndx].lower().strip()
            if ( newFileData[lineIndx] == "" ):
                continue

            fileData.append( newFileData[lineIndx] )

        # Read through data:
        dataLen = len(fileData)

        return


class ParticleYields:
    """
    The \"ParticleYields\" object contains scatter plots (with associated error bars)
    of mass yields, charge yields, and really any yield that GSM can have.
    """



    def __init__(self, newPrint = Print() ):
        """Constructor"""
        
        self.__write = newPrint
        self.__resetMembers()

        return

    def __del__(self):
        """Destructor"""
        self.__resetMembers()
        return

    def __resetMembers(self):
        """Resets all member variables"""
        self.__fileData = []
        self.__dataLen = 0

        return

    def __parseFileData(self, start, end):
        """Parses the file data based on the given start and end indices"""
        if ( start < 0 ):
            start = 0
        if ( end > self.__dataLen ):
            end = self.__dataLen


        return

    def addFileData(self, fileData):
        """Adds data to the file and parses it"""
        if ( not isinstance(fileData, list) ):
            self.__write.message = "File data must be a list of strings. Cannot parse yield data."
            self.__write.print(1, 2)
            return

        # Reduce file data:
        startingIndx = self.__dataLen
        for lineIndx in range(0, len(fileData), 1):
            fileData[lineIndx] = fileData[lineIndx].lower().strip()
            self.__fileData.append( fileData[lineIndx] )
            self.__dataLen += 1
        endingIndx = self.__dataLen

        self.__parseData(startingIndx, endingIndx)

        return
