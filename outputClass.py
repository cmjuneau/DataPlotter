
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
        self.__pisaData = gsmData.DoubleDiffPISA( self.__write )

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

        self.__parseDoubleDiff()

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
                myParticleAngles[ j+1 ] = 361
                myParticleTypes = (len(myParticleAngles)-1)*["Double Differential"]
                myParticleTypes.append( "Angle integrated" )

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
                self.__write.print(2, 3)
                thisParticle = gsmData.ParticlePISAData(particleID, self.__write)

                # Create and append histogram data:
                for j in range(0, numSets, 1):
                    newHistogram = gsmData.Histogram(myParticleTypes[j], myParticleAngles[j], myBins, myValues[j], self.__write)
                    thisParticle.addHistogram( newHistogram )

                    # Testing:
                    if ( particleID == "be9" and myParticleAngles[j] == 90 and False ):
                        print("Data contains %d bins (%d values)" % (len(myBins), len(myValues[j])) )
                        print("Histogram bins are %d (%d)." % (
                        len(thisParticle.getHistogram(myParticleAngles[j]).getBinValues()),
                        thisParticle.getHistogram(myParticleAngles[j]).getNumBins()) )
                        print("Histogram values are %d (%d)." % (
                        len(thisParticle.getHistogram(myParticleAngles[j]).getDataPoints()),
                        thisParticle.getHistogram(myParticleAngles[j]).getNumDataPoints()) )

                # Add particle to the list:
                self.__pisaData.addParticle(thisParticle)

        return

    # For retrieving data:
    def getPISAData(self):
        """Returns the PISA object to the user"""
        return self.__pisaData


class CEMOutput( GSMOutput ):
    """CEM Output Class"""
    # Copy of GSM class (output files are consistent)
    pass
