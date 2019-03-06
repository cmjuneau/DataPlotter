
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
                self.__write.message = "No histogram for particle \"%s\" with matching angle (%.2f) found." % (self.__particleName, someLabel)
                self.__write.print(2, 4)
                return None
        else:
            # Invalid label, warn user
            self.__write.message = "Invalid label type passed in (" + str(someLabel) + "), should be 'float'. Cannot return PISA histogram object."
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
            particleIndx = 0
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

    def getNumParticles(self):
        """Returns the number of particles that exist in the object"""
        return self.__numParticles
