
################################################################################
# File documentation:
"""
This module contains the output file class (for CEM, GSM, LAQGSM)
Each output type has separate sub-classes for each data type, each with a print function.
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
from fileModule import readFile, parseLine, fileExists
import gsmDataClasses as gsmData

# VERSION Number:
__version__ = "1.0.0"


# Class defaults:
# (PISA Data)
particleTypes = ("n", "p", "d", "t", "he3", "he4", "he6", "li6", "li7", "li8",
"li9", "be7", "be9", "be10", "b9", "b10", "b11", "b12", "c11", "c12", "c13",
"c14", "z=7", "z=8", "z=9", "z=10", "z=11", "z=12", "z=13", "z=14")
numParticleTypes = len( particleTypes )


class GSMOutput:
    """GSM Output Class"""
    __pisaAngleIntFlag = 361
    __pisaEnergyIntFlag = 362

    def __init__(self, fileName = None, newPrint = Print() ):
        """Constructor for the GSM Output class"""

        # Reset all values:
        self.__write = newPrint

        # Set values from constructor:
        if ( fileName == None ):
            self.__write.message = "A filename must be passed in to create an output file object."
            self.__write.print(0, 1)
            return

        self.__resetMembers()

        self.__fileName = fileName
        doesFileExist = fileExists( self.__fileName )
        if ( not doesFileExist ):
            self.__write.message = "File \"%s\" does not exist in this directory. Cannot obtain data." % ( self.__fileName )
            self.__write.print(1, 2)
            return

        # Read file:
        self.__fileData = readFile( self.__fileName )
        self.__fileLen  = len( self.__fileData )
        self.__fileRead = True

        # Parse file data:
        self.__parseData()

        return

    def __resetMembers(self):
        """Resets all members in the object"""

        self.__fileData = []
        self.__fileLen = 0
        self.__fileRead = False
        # PISA:
        self.__pisaData = gsmData.DoubleDiffPISA( self.__write )
        # Particle data:
        self.__particleData = []
        self.__numParticleData = 0
        # Yield data:
        self.__yieldData = gsmData.ParticleYields( self.__write )

        # Read file:
        self.__fileName = ""
        self.__fileData = []
        self.__fileLen  = 0
        self.__fileRead = False

        return

    def __del__(self):
        """Class destructor"""
        self.__resetMembers()

        return

    def __parseData(self):
        """Interface for parsing out all data from the read file"""

        # Print messages:
        self.__write.message = "\tParsing data..."
        self.__write.print(2, 3)

        # Reduce file data:
        for lineIndx in range(0, self.__fileLen, 1):
            self.__fileData[lineIndx] = self.__fileData[lineIndx].lower().strip()

        self.__parseParticleData()
        self.__parseYieldData()
        self.__parseDoubleDiff()

        return

    def __parseParticleData(self):
        """
        Parses out particle data for each particle in output file
        """
        __particleIDs = ("neutrons", "protons", "deuterons", "tritons",
        "helium-3", "alphas", "neg. pions", "neut pions", "pos. pions")
        __numParticleIDs = len(__particleIDs)
        __particleFlags = ("**********************************",
        "*********************************")

        # Look through data and find the particle flag; then, create object
        #    containing all the particles data:
        self.__write.message = "\t\tObtaining particle data..."
        self.__write.print(2, 3)
        for lineIndx in range(0, self.__fileLen, 1):

            # Skip all lines that don't start with ***'s
            if ( not self.__fileData[lineIndx].startswith(__particleFlags[0]) ):
                continue

            # Look for particle flag now and skip lines without the flag:
            validPart = False
            theParticle = None
            for parIndx in range(0, __numParticleIDs, 1):
                if ( __particleIDs[parIndx] in self.__fileData[lineIndx] ):
                    validPart = True
                    theParticle = __particleIDs[parIndx]
            if ( not validPart ):
                continue

            # Found a particle data's next flag; create new data lines and create particle
            parData = []
            numConsBlanks = 0
            findEnd = True
            while ( True ):
                lineIndx += 1
                parLine = self.__fileData[lineIndx].lower().strip()

                # Look for end of particle data:
                if ( findEnd ):
                    # Two blanks are present at end of the last particles information:
                    if ( parLine == "" ):
                        numConsBlanks += 1
                    else:
                        numConsBlanks = 0

                    if ( parLine.startswith(__particleFlags[0]) or (numConsBlanks > 1) ):
                        break

                # Add data to the set:
                parData.append( parLine )


            # The data relating to the particle was obtained; create object:
            self.__particleData.append( gsmData.ParticleData(theParticle, self.__write) )
            self.__particleData[ self.__numParticleData ].addFileData( parData )
            self.__numParticleData += 1

        return

    def __parseYieldData(self):
        """
        Parses out particle yield data:

        Parses out data for:
           Mass yields (mb)
           Charge yields (mb)
           More can be added easily
        """
        __yieldFlags = ("yields of different channels (with > 1 mb):",
        "*************** nuclide yields [mb]  (zero values suppressed) *****************",
        "mass yield [mb] and the mean and variance of the kinetic energy [mev]",
        "charge yield [mb] and the mean and variance of the  kinetic energy [mev]")
        __numYieldFlags = len(__yieldFlags)
        __yieldEndFlag = "**********************************"

        self.__write.message = "\t\tObtaining yield data..."
        self.__write.print(2, 3)

        # Look through file data for the start/end flags:
        for lineIndx in range(0, self.__fileLen, 1):

            # Skip all lines that don't flag yield data
            dataFlagged = False
            for flagIndx in range(0, __numYieldFlags, 1):
                if ( self.__fileData[lineIndx].startswith(__yieldFlags[flagIndx]) ):
                    dataFlagged = True
                    break
            if ( not dataFlagged ):
                continue

            # Found the start of the yield section; obtain data:
            yieldData = []
            yieldData.append( self.__fileData[lineIndx].lower().strip() )
            while ( True ):
                lineIndx += 1
                if ( lineIndx >= self.__fileLen ):
                    break
                dataLine = self.__fileData[lineIndx].lower().strip()

                # Look for end of yield data:
                if ( dataLine.startswith(__yieldEndFlag) ):
                    break

                # Add data to the set:
                yieldData.append( dataLine )

            # The data relating to the particle was obtained; create object:
            self.__yieldData.addFileData( yieldData )
            break

        return

    def __parseDoubleDiff(self):
        """
        Parse out double differential cross section data from PISA usage:

        Parses out data for:
            Double differential cross sections
            Angle  integrated distributions
            Energy integrated distributions
        """
        __dataFlags = ("Double differential cross-section d2S/dTdO (mb/MeV/sr) of".strip().lower(),
        "Angular distribution of produced fragments dS/dOm [mb/sr] for energy range(MeV)".strip().lower())
        __dataLen = ( len(__dataFlags[0]), len(__dataFlags[1]) )

        # Print message:
        self.__write.message = "\t\tObtaining PISA double differential data..."
        self.__write.print(2, 3)

        # Sections: Double differential and energy integrated are in the same table (angle integrated in separate table)
        # Search through data for double differential and energy integrated data:
        for i in range(0, self.__fileLen, 1):
            dataLine = self.__fileData[i].strip().lower()
            if ( dataLine.startswith(__dataFlags[0]) ):
                # Found the flag
                thisParticleType = dataLine[ __dataLen[0] : ].strip()

                # Search through particle types:
                for j in range(0, numParticleTypes, 1):
                    if ( thisParticleType == particleTypes[j] ):
                        particleIndx = j
                        break

                # Have the particle ID; obtain bins and associated values:
                particleID = particleTypes[ particleIndx ]
                # Skip a line:
                i += 2
                # Obtain angles now (parse line)
                newLine = self.__fileData[ i ]
                newLine = newLine[ len("T(MeV)/angle:") : ].strip()
                parsedData = parseLine( newLine )
                myParticleAngles = parsedData
                for j in range(0, len(myParticleAngles)-1, 1):
                    myParticleAngles[j] = float(myParticleAngles[j])
                myParticleAngles[ j+1 ] = self.__pisaAngleIntFlag
                myParticleTypes = (len(myParticleAngles)-1)*["Double Differential"]
                myParticleTypes.append( "Angle Integrated" )

                # Now obtain bin bounds and data (the particleID, types, and labels are created)
                numSets = len(myParticleTypes)
                myBins = []
                numBins = 0
                myValues = [ [] for j in range(0, numSets, 1) ]
                numValues = 0
                while True:
                    # Obtain bin bounds:
                    # (obtain new line)
                    i += 1
                    parsedLine = parseLine ( self.__fileData [ i ] )

                    # Check for exit:
                    if ( len(parsedLine) == 0 or parsedLine[0] == "energ." ):
                        break

                    # Remove the "-" from the first entry:
                    firstEntry = parsedLine[0]
                    if ( numSets <= len(parsedLine)-2 ):
                        # Space between bin start and end
                        parsedLine[0] = firstEntry[ : firstEntry.find("-") ]
                    else:
                        # No space between bin start end end; append bin end to middle of list
                        parsedLine = parseLine( firstEntry, "-") + parsedLine[1 : ]

                    # Convert parsed line to floats:
                    for j in range(0, len(parsedLine), 1):
                        try:
                            parsedLine[j] = float(parsedLine[j])
                        except:
                            self.__write.message = "Failed to convert line element to float (" + parsedLine[j] + ")"
                            self.__write.print(1, 2)
                            parsedLine[j] = 0.0

                    # Bin bounds are now contained in "parsedLine[0]" and "parsedLine[1]"
                    if ( numBins == 0 ):
                        # Set base bin:
                        myBins.append( parsedLine[0] )
                    else:
                        # Verify bin start matches last bin's end, if not then create empty bin here
                        if ( not parsedLine[0] == myBins[ numBins ] ):
                            myBins.append( parsedLine[0] )
                            numBins += 1
                            # Set bin value to 0 for all bins:
                            for j in range(0, numSets, 1):
                                myValues[j].append( 0.00 )   # Set bin value to 0
                            numValues += 1

                    # Set end of bin:
                    myBins.append( parsedLine[1] )
                    numBins += 1

                    # Set value for each of the bins:
                    for j in range(0, numSets, 1):
                        myValues[j].append( parsedLine[j+2] )

                # Reached end of data table; no more data (construct particle histograms)
                # Create particle object:
                self.__write.message = "\t\t\tStoring PISA histogram data for particle \"%s\"..." % (particleID)
                self.__write.print(2, 5)
                thisParticle = gsmData.ParticlePISAData(particleID, self.__write)

                # Create and append histogram data:
                for j in range(0, numSets, 1):
                    newHistogram = gsmData.Histogram(myParticleTypes[j], myParticleAngles[j], myBins, myValues[j], self.__write)
                    thisParticle.addHistogram( newHistogram )

                # Add particle to the list:
                self.__pisaData.addParticle(thisParticle)

            elif ( dataLine.startswith(__dataFlags[1]) ):
                # Advance 2 lines to where the data is:
                i += 2
                dataLine = self.__fileData[i].strip().lower()

                # Obtain particle identifiers:
                parsedLine = parseLine( dataLine )
                particleID = []
                for j in range(1, len(parsedLine), 1):
                    particleID.append( parsedLine[j] )

                # Obtain data:
                numSets = len(particleID)
                myBins = []
                numBins = 0
                myValues = [ [] for j in range(0, numSets, 1) ]
                numValues = 0
                while( True ):

                    # Obtain line's data:
                    i += 1
                    dataLine = self.__fileData[i].strip().lower()

                    # Exit if end of set was found:
                    if ( dataLine.startswith("int. x sec") or dataLine.startswith("int. xsec") ):
                        break

                    # Get bin bounds:
                    lowerBin = dataLine[ : dataLine.find("-") ]
                    parsedLine = parseLine( dataLine[ dataLine.find("-") + 1 : ] )
                    upperBin = parsedLine[0]
                    del parsedLine[0]

                    # Convert all values to floats:
                    try:
                        lowerBin = float(lowerBin)
                    except:
                        self.__write.message = "Unable to convert lower bin (%s) to a float for angular distributions." % lowerBin
                        self.__write.print(1, 2)
                        lowerBin = 0
                    try:
                        upperBin = float(upperBin)
                    except:
                        self.__write.message = "Unable to convert upper bin (%s) to a float for angular distributions." % upperBin
                        self.__write.print(1, 2)
                        upperBin = lowerBin
                    for j in range(0, len(parsedLine), 1):
                        try:
                            parsedLine[j] = float( parsedLine[j] )
                        except:
                            self.__write.message = "Unable to convert histogram value (%s) to a float for angular distributions." % (parsedLine[j])
                            self.__write.print(1, 2)

                    # Add a bin:
                    if ( numBins == 0 ):
                        # Set base bin:
                        myBins.append( lowerBin )
                    else:
                        # Verify bin start matches last bin's end, if not then create empty bin here
                        if ( not lowerBin == myBins[ numBins ] ):
                            myBins.append( lowerBin )
                            numBins += 1
                            # Set bin value to 0 for all bins:
                            for j in range(0, numSets, 1):
                                myValues[j].append( 0.00 )   # Set bin value to 0
                            numValues += 1
                    myBins.append( upperBin )
                    numBins += 1

                    # Set the value for the bin:
                    for j in range(0, min(numSets, len(parsedLine)), 1):
                        myValues[j].append( parsedLine[j] )
                    numValues += 1

                # Now apply histograms and add to existing particles:
                for j in range(0, numSets, 1):
                    self.__write.message = "\t\t\tStoring PISA energy integrated data for particle \"%s\"..." % (particleID[j])
                    self.__write.print(2, 5)

                    # Create histogram object, add to PISA data object:
                    theHistogram = gsmData.Histogram("energy integrated", self.__pisaEnergyIntFlag, myBins, myValues[j], self.__write)
                    self.__pisaData.addParticleHistogram(particleID[j], theHistogram)


        return

    # For retrieving data:
    def getPISAData(self):
        """Returns the PISA object to the user"""
        return self.__pisaData

    def getPISAParticle(self, particleID):
        """Returns the particle's PISA data"""
        return ( self.__pisaData.getParticle(particleID) )

    def getPISAParticleHistogram(self, particleID, someAngle):
        """Returns the specific histogram associated with the particle's PISA data"""
        return ( self.__pisaData.getParticleHistogram(particleID, someAngle) )

    def getParticleData(self, particleID):
        """Returns the particle data requested, if exists"""
        theData = None
        for parIndx in range(0, self.__numParticleData, 1):
            if ( particleID == self.__particleData[parIndx].queryParticleID() ):
                theData = self.__particleData[parIndx]
                break

        if ( theData == None ):
            self.__write.message = "No particle data exists for %s particle(s)." % particleID
            self.__write.print(1, 2)

        return theData

    def getParticleEnergySpectra(self, particleID):
        """Returns the particle data's energy spectra"""
        energySpectra = None

        theData = self.getParticleData(particleID)
        if ( not theData == None ):
            energySpectra = theData.queryEnergySpectra()

        if ( energySpectra == None ):
            self.__write.message = "No energy spectrum exists for %s particles." % particleID
            self.__write.print(1, 2)

        return energySpectra

    def getParticleLabeledEnergySpectra(self, particleID, histLabel):
        """Returns a histogram for the energy spectrum of the particle of some label"""
        theHistogram = None

        theESpectra = self.getParticleEnergySpectra(particleID)
        if ( not theESpectra == None ):
            theHistogram = theESpectra.queryHistogram(histLabel)

        if ( theHistogram == None ):
            self.__write.message = "No energy spectra histograms exist in the energy spectrum object."
            self.__write.print(1, 2)

        return theHistogram

    def queryYieldData(self):
        """Returns the yield data to the user/client"""
        yieldData = self.__yieldData
        if ( yieldData is None ):
            self.__write.message = "Cannot query: no yield data was present in the file."
            self.__write.print(1, 2)
        return yieldData

    def queryChannelYields(self):
        """Returns the channel yield found in the output file"""
        userData = None
        yieldData = self.queryYieldData()
        if ( not yieldData == None ):
            userData = yieldData.queryChannelYields()
        return userData

    def queryNuclideYields(self):
        """Returns the nuclide yield found in the output file"""
        userData = None
        yieldData = self.queryYieldData()
        if ( not yieldData == None ):
            userData = yieldData.queryNuclideYields()
        return userData

    def queryMassYields(self):
        """Returns the mass yield found in the output file"""
        userData = None
        yieldData = self.queryYieldData()
        if ( not yieldData == None ):
            userData = yieldData.queryMassYields()
        return userData

    def queryChargeYields(self):
        """Returns the charge yield found in the output file"""
        userData = None
        yieldData = self.queryYieldData()
        if ( not yieldData == None ):
            userData = yieldData.queryChargeYields()
        return userData


class CEMOutput( GSMOutput ):
    """CEM Output Class"""
    # Copy of GSM class (output files are consistent)
    pass
