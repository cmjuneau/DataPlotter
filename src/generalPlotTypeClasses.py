
################################################################################
# File documentation:
"""
This module contains general class objects that can be used for easily storing
data and subsequently plotting the data.

The module contains class objects named:
-Histogram
-Scatter
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
import fileModule
from printClass import Print

# VERSION Number:
__version__ = "1.0.0"


class Histogram:
    """
    The \"Histogram\" object stores information for bin bounds and all
    associated values. The histogram object has some options that can be used:
    -enforceMinValues (True): Forces all Y-values and bin bounds to be larger
    \tthan some pre-specified value. Minimum values exist for both bins bounds
    \tand the associated values.
    \t-This shifts all Y-values and bin bounds up to be no smaller than specified.
    -removeLastZeroValuedBinValues (True): Removes all zero-valued Y-values
    \tthat exist at the end of the passed in histogram data.
    \tIn essence, this option truncates the data to only the data that is useful.
    """
    # Options:
    __enforceMinValues = True
    __minBinValAllowed = 0.00
    __minYValueAllowed = 0.00
    __removeLastZeroValuedBinValues = True
    # Defaults:
    __defaultNote = "No note given"
    __defaultBinWidth = 5.00

    def __init__(self, bins, values, newNote=None, newPrint = Print() ):
        """Constructor for class"""

        self.__write = newPrint
        self.__resetMembers()
        self.setNote(newNote)
        self.__setBinsAndValues(bins, values)

        return

    def __del__(self):
        """Deconstructor for the object"""
        self.__resetMembers()

        return

    def __resetMembers(self):
        """Resets all members"""
        self.__note = "No information given"
        self.__yValues = []
        self.__numYValues = 0
        self.__binBounds = []
        self.__numBins = 0

        return

    def __findLastNonZeroEntryIndex(self, someValues):
        """Finds the last non-zero valued entry in a list or tuple"""
        lastIndex = None

        # Ensure the numbers are a list/tuple of floats or ints:
        if ( not isinstance(someValues, (list, tuple)) ):
            self.__write.message = "Cannot find the last non-zero valued entry in any type except lists or tuples."
            self.__write.print(1, 2)
            return lastIndex

        # Find last non-zero valued index:
        lastValidIndex = len(someValues) - 1
        for i in range(0, lastValidIndex, 1):
            lastIndex = lastValidIndex-i
            if ( someValues[lastIndex] > 0 ):
                break

        return lastIndex

    def __setBinsAndValues(self, binBounds, yVals):
        """Sets bin bounds and values"""

        # Verify that bins and values are lists:
        validBins   = isinstance(binBounds,   list)
        validValues = isinstance(yVals, list)
        if ( (not validBins) or (not validValues) ):
            self.__write.message = "Invalid bins or values passed were passed in to the general Histogram object. Parameters must be lists."
            self.__write.print(0, 1)
            return

        # Convert to floats:
        for i in range(0, len(binBounds), 1):
            try:
                binBounds[i] = float( binBounds[i] )
            except:
                self.__write.message = "Unable to convert bin bound %d (%s) to float. Assuming value is 0." % ( (i+1), str(binBounds[i]) )
                self.__write.print(1, 2)
                binBounds[i] = 0
        for i in range(0, len(yVals), 1):
            try:
                yVals[i] = float( yVals[i] )
            except:
                self.__write.message = "Unable to convert bin value %i (%s) to float. Assuming value is 0." % ( (i+1), str(yVals[i]) )
                self.__write.print(1, 2)
                yVals[i] = 0

        # Ensure only positive values (for bins, values)
        if ( self.__enforceMinValues ):
            # (Shift all values up to ensure >=0)
            shiftValue = 0
            badBinBound = 0
            for i in range(0, len(yVals), 1):
                shiftValue = min(shiftValue, yVals[i])
                badBinBound = min(badBinBound, yVals[i])
            if ( shiftValue < self.__minYValueAllowed ):
                shiftValue = abs(shiftValue)
                self.__write.message = "Unallowed lowest bin value (%.3f). Shifting all values up by (%.3f)." % (badBinBound, shiftValue)
                self.__write.print(0, 1)
                for i in range(0, len(yVals), 1):
                    yVals[i] += shiftValue

            # (Do same for bins)
            if ( binBounds[0] < self.__minBinValAllowed ):
                shiftValue = -binBounds[0]
                self.__write.message = "The lower bin boundary (%.3f) is below %.3f. Shifting all values up by (%.3f)." % (binBounds[0], self.__minBinValAllowed, shiftValue)
                self.__write.print(0, 1)
            else:
                shiftValue = 0
            for i in range(0, len(binBounds), 1):
                binBounds[i] = shiftValue + binBounds[i]

        if ( self.__removeLastZeroValuedBinValues ):
            lastNonZeroIndx = self.__findLastNonZeroEntryIndex(yVals)
            if ( lastNonZeroIndx == None ):
                lastNonZeroIndx = len(yVals)
            else:
                lastNonZeroIndx += 1   # Shift up one for comparison by length (not index)
        else:
            lastNonZeroIndx = len(yVals)

        # Determine how many values to use (only accept minimum of what given data allows)
        numValues = min( lastNonZeroIndx, (len(binBounds)-1) )

        # Set bin values:
        self.__binBounds.append( binBounds[0] )
        for i in range(1, (numValues+1), 1):
            # Ensure bin value is larger than last:
            if ( binBounds[i] < binBounds[i-1] ):
                self.__write.message = "The bin has smaller value than previous (range [%.2f, %.2f))." % (binBounds[i-1], binBounds[i])
                self.__write.print(1, 3)
                self.__write.message = "   Setting bin width to %.3f." % (self.__defaultBinWidth)
                self.__write.print(1, 3)
                binBounds[i] = binBounds[i-1]
            self.__binBounds.append( binBounds[i] )
        self.__numBins = len( self.__binBounds ) - 1


        # Valid particle was found, now set data:
        for i in range(0, numValues, 1):
            self.__yValues.append( yVals[i] )
        self.__numYValues = len( self.__yValues )

        return

    def setNote(self, newNote):
        """Sets the information given to define the object"""
        # Ensure argument is a string:
        if ( newNote == None ):
            newNote = self.__defaultNote
        if ( not isinstance(newNote, str) ):
            try:
                newNote = str(newNote)
            except:
                self.__write.message = "Unable to convert desired histogram information to str type: ", newNote
                self.__write.print(1, 2)
                newNote = self.__defaultNote
                self.__write.message = "   Using default information label (\"%s\")." % (newNote)
                self.__write.print(1, 2)

        self.__note = newNote
        return

    def queryNote(self):
        """Returns the histogram's note"""
        return self.__note

    def appendDataPoint(self, upperBinBound, yValue):
        """Appends a data point to the end of the histogram"""
        # Check for errors:
        if ( self.__forcePositiveValues ):
            if ( yValue < 0 ):
                self.__write.message = "Cannot append bin value (%.3f) below 0. Setting to 0..." % (yValue)
                self.__write.print(1, 3)
                yValue = 0
        # Ensure new upper bin bound exceeds the last largest bin:
        if ( upperBinBound < self.__binBounds[ self.__numBins ] ):
            self.__write.message = "Invalid end-bin value (%f) given. Setting to 5 more than last bin..." % (upperBinBound)
            self.__write.print(1, 3)
            upperBinBound = self.__binBounds[ self.__numBins ] + 5
        if ( len(self.__binBounds) == 0 ):
            # No bins have been set; start at 0 for user:
            self.__binBounds.append( 0.00 )
            self.__write.message = "No starting bin value was established. Assuming starting bin value is %.3f." % (self.__binBounds[0])
            self.__write.print(1, 3)

        # Append data point:
        self.__binBounds.append( upperBinBound )
        self.__numBins += 1
        self.__yValues.append( yValue )
        self.__numYValues += 1

        return

    def queryYValues(self):
        """Returns the Y-vaules of the histogram object"""
        return self.__yValues

    def queryBinBounds(self):
        """Returns the bin bounds for the histogram object"""
        return self.__binBounds

    def queryNumYValues(self):
        """Returns the number of data points that exist in the particle"""
        return self.__numYValues

    def queryNumBins(self):
        """Returns the number of bins that exist in the particle"""
        return self.__numBins

    def queryBoundsAndValues(self):
        """Returns the bin bounds and associated values to client"""
        return (self.getBinBounds(), self.getYValues())

    def queryNote(self):
        """Returns the note stored in the histogram object"""
        return self.__note

    def queryLargestValue(self):
        """Returns the largest value in the histogram"""
        maxVal = -float("inf")
        for indx in range(0, self.__numYValues, 1):
            maxVal = max(maxVal, self.__yValues[indx])

        return maxVal


class Scatter:
    """
    The \"Scatter\" object stores X/Y data for a histogram. In addition, the
    relative error for each point can be stored in the scatter object as well
    for plotting error plots.
    \tNOTE: The object does NOT support assymetric errors, only single-valued
    \t      errors for both the X and Y points. Error values are assumed in
    \t      the case of mismatched list/tuple sizes.
    """
    __defaultXValue = 0.00
    __defaultYValue = 0.00
    __defaultXError = 0.00
    __defaultYError = 0.00

    def __init__(self, xVals, yVals, xErr=None, yErr=None, newPrint = Print()):
        """constructor for Scatter object"""

        # Set default values:
        self.__write = newPrint
        self.__resetMembers()
        self.__setXY(xVals, yVals)
        self.__setXYError(xErr, yErr)

        return

    @classmethod
    def importData(cls, fileName, newPrint = Print() ):
        """Reads X/Y points and associated error, if present, from a file"""
        __dataIdentifiers = ("x", "y", "dx", "dy", "skip")
        __numDataID = len(__dataIdentifiers)
        __commentFlags = ("#", "!", "//")
        __numCommentFlags = len(__commentFlags)
        __parseFlags = (",", ";", ":", " ")
        __numParseFlags = len(__parseFlags)

        newScatter = None

        # Check if file exists and read data:
        if ( not fileModule.fileExists(fileName) ):
            newPrint.message = "Unable to find filename to read the data from."
            newPrint.print(1, 2)
            return newScatter

        # Read data:
        theFilesData = fileModule.readFile( fileName )

        # Manipulate data read:
        for i in range(0, len(theFilesData), 1):
            # Remove all comments:
            for j in range(0, __numCommentFlags, 1):
                if ( __commentFlags[j] in theFilesData[i] ):
                    lineData = theFilesData[i]
                    lineData = lineData[ : len(__commentFlags[j]) ]
                    theFilesData[i] = lineData.rstrip()

            # Remote tabs:
            theFilesData[i] = theFilesData[i].replace("\t", " ")

        # Store fileData:
        fileData = []
        for i in range(0, len(theFilesData), 1):
            # Ignore blank lines:
            if ( theFilesData[i] == "" ):
                continue
            # Store information:
            fileData.append( theFilesData[i].strip().lower() )

        # Obtain headers line, remove from data set, and determine how data is parsed:
        headerLine = fileData[0]
        del fileData[0]
        theParseFlag = None
        for i in range(0, __numParseFlags, 1):
            if ( __parseFlags[i] in headerLine ):
                theParseFlag = __parseFlags[i]
                break
        if ( theParseFlag == None ):
            newPrint.message = "Unable to determine how to parse data."
            newPrint.print(1, 2)
            theParseFlag = input("Please enter the string by which to parse file data: ")

        # Obtain header flags and the appropriate indices:
        headerFlags = fileModule.parseLine( headerLine, theParseFlag )
        numHeaderFlags = len(headerFlags)
        xIndx = None
        yIndx = None
        dxIndx = None
        dyIndx = None
        skipIndx = []
        numSkipIndx = 0
        for hdrID in range(0, numHeaderFlags, 1):
            headerFlags[hdrID] = headerFlags[hdrID].strip()   # Remove excess spacing to help match:
            # Look for valid header:
            validHeader = False
            for flagID in range(0, __numDataID, 1):
                if ( headerFlags[hdrID].startswith(__dataIdentifiers[flagID]) ):
                    validHeader = True
                    headerFlags[hdrID] == __dataIdentifiers[flagID]
                    # Set index for X/Y values and associated errors, if present
                    if ( headerFlags[hdrID] == __dataIdentifiers[0] ):
                        # X flag
                        if ( xIndx == None ):
                            xIndx = hdrID
                        else:
                            newPrint.message = "X header already exists in file \"%s\". Using first X header for values." % (fileName)
                            newPrint.print(1, 2)
                    elif ( headerFlags[hdrID] == __dataIdentifiers[1] ):
                        # Y flag
                        if ( yIndx == None ):
                            yIndx = hdrID
                        else:
                            newPrint.message = "Y header already exists in file \"%s\". Using first Y header for values." % (fileName)
                            newPrint.print(1, 2)
                    elif ( headerFlags[hdrID] == __dataIdentifiers[2] ):
                        # dX flag
                        if ( dxIndx == None ):
                            dxIndx = hdrID
                        else:
                            newPrint.message = "dX header already exists in file \"%s\". Using first dX header for values." % (fileName)
                            newPrint.print(1, 2)
                    elif ( headerFlags[hdrID] == __dataIdentifiers[3] ):
                        # dY flag
                        if ( dyIndx == None ):
                            dyIndx = hdrID
                        else:
                            newPrint.message = "dY header already exists in file \"%s\". Using first dY header for values." % (fileName)
                            newPrint.print(1, 2)
                    else:
                        # Skip flag
                        skipIndx.append( hdrID )
                        numSkipIndx += 1
                    break

            if ( not validHeader ):
                # Treat as a skip header:
                skipIndx.append( hdrID )
                numSkipIndx += 1
                # Print to user:
                newPrint.message = "Invalid data header was given (%s). The valid headers are:" % (headerFlags[hdrID])
                newPrint.print(1,2)
                for i in range(0, __numDataID, 1):
                    newPrint.message = "   %d: %s" % ( (i+1), __dataIdentifiers[i] )
                    newPrint.print(1, 2)

        # Ensure X and Y are present at minimum:
        if ( xIndx == None or yIndx == None ):
            newPrint.message = "Both an X and Y data column must be specified for reading data in to a scatter plot."
            newPrint.print(0, 1)
            return newScatter

        # Parse and store data accordingly:
        xVals = []
        yVals = []
        if ( dxIndx == None ):
            dxVals = None
        else:
            dxVals  = []
        if ( dyIndx == None ):
            dyVals = None
        else:
            dyVals  = []
        for lineIndx in range(0, len(fileData), 1):
            # Parse the line:
            lineNum = lineIndx + 1
            parsedLine = fileModule.parseLine( fileData[lineIndx], theParseFlag )
            lineLength = len(parsedLine)

            # Ensure header indices are within the bounds:
            if ( xIndx >= lineLength ):
                newPrint.message = "Unable to determine X value on line %d: Parsed data doesn't have enough indices." % (lineNum)
                newPrint.print(0, 2)
                xVals.append( 0.00 )
            else:
                xVals.append( parsedLine[xIndx] )
            if ( yIndx >= lineLength ):
                newPrint.message = "Unable to determine Y value on line %d: Parsed data doesn't have enough indices." % (lineNum)
                newPrint.print(0, 2)
                yVals.append( 0.00 )
            else:
                yVals.append( parsedLine[yIndx] )
            if ( not dxIndx == None ):
                if ( dxIndx >= lineLength ):
                    newPrint.message = "Unable to determine dX value on line %d: Parsed data doesn't have enough indices." % (lineNum)
                    newPrint.print(0, 2)
                    dxVals.append( 0.00 )
                else:
                    dxVals.append( parsedLine[dxIndx] )
            if ( not dyIndx == None ):
                if ( dyIndx >= lineLength ):
                    newPrint.message = "Unable to determine dY value on line %d: Parsed data doesn't have enough indices." % (lineNum)
                    newPrint.print(0, 2)
                    dyVals.append( 0.00 )
                else:
                    dyVals.append( parsedLine[dyIndx] )

        # X/Y values are now obtained; create object:
        newScatter = Scatter(xVals, yVals, dxVals, dyVals, newPrint)

        return newScatter

    def __del__(self):
        """Deconstructor for the Scatter object"""
        self.__resetMembers()

        return

    def __resetMembers(self):
        """Resets all members in the Scatter object"""
        self.__xVals = []
        self.__yVals = []
        self.__xError = []
        self.__yError = []
        self.__numDataPoints = 0

        return

    def __validateXYInputs(self, someVals, type):
        """Validates the values passed in and returns the list"""
        newValues = None

        # Check type (for printing and default values)
        type = type.lower().strip()
        defaultValue = self.__defaultXValue
        if ( type == "x" ):
            defaultValue = self.__defaultXValue
        elif ( type == "y" ):
            defaultValue = self.__defaultYValue
        elif ( type == "x-error" ):
            defaultValue = self.__defaultXError
        elif ( type == "y-error" ):
            defaultValue = self.__defaultYError
        else:
            type == "?"
            defaultValue = self.__defaultXValue

        # Validate arguments:
        validVals = isinstance(someVals, (list, tuple))
        if ( not validVals ):
            self.__write.message = "A list or tuple of %s values must be used for establishing Scatter object's values." % (type)
            self.__write.print(1, 2)
            return newValues

        # Create a list of float values:
        if ( len(someVals) > 0 ):
            newValues = []
            for i in range(0, len(someVals), 1):
                # Convert value to float if not a float/int:
                theValue = someVals[i]
                if ( not isinstance(theValue, (float, int)) ):
                    try:
                        theValue = float(theValue)
                    except:
                        self.__write.message = "Unable to convert %s-value in Scatter object to float: " %( type ), theValue
                        self.__write.print(1, 2)
                        someVal = defaultValue
                        self.__write.message = "   Using a value of %.3f." % (theValue)
                        self.__write.print(1, 2)

                # Now append the value to the list:
                newValues.append( theValue )

        return newValues

    def __validateXYErrorInput(self, errorVals, flag):
        """Returns a list of values for the error bars (X or Y)."""
        newErrorVals = None

        flag = flag.strip().lower()
        if ( flag == "x-error" ):
            defaultValue = self.__defaultXError
        elif ( flag == "y-error" ):
            defaultValue = self.__defaultYError
        else:
            flag = "?"
            defaultValue = self.__defaultXError

        # Create valid list of numbers:
        errorVals = self.__validateXYInputs(errorVals, "x-error")
        if ( errorVals == None ):
            return newErrorVals

        # Append the default value if the length doesn't match the X/Y sets:
        if ( len(errorVals) < self.__numDataPoints ):
            self.__write.message = "The %s length doesn't match the X or Y value length." % (flag)
            self.__write.print(1, 2)
            self.__write.message = "   Using a default value of %.3f for all other %s values." % (defaultValue, flag)
            for i in range(len(errorVals), self.__numDataPoints, 1):
                errorVals.append( defaultValue )

        # Add to list of X-error bars:
        if ( len(errorVals) > 0 ):
            newErrorVals = []
            for i in range(0, len(errorVals), 1):
                newErrorVals.append( errorVals[i] )

        return newErrorVals

    def __setXY(self, xVals, yVals):
        """Sets the X and Y coordinates and error values (if present)"""

        # Obtain lists of valid numbers:
        xVals = self.__validateXYInputs(xVals, "x")
        yVals = self.__validateXYInputs(yVals, "y")

        # Append valid arguments if /= None:
        if ( (not xVals == None) and (not yVals == None) ):
            numCompletePairs = min( len(xVals), len(yVals) )
            # Warn user if numbers are being dropped:
            if ( not len(xVals) == len(yVals) ):
                self.__write.message = "Size of X/Y pairs for Scatter object do not match."
                self.__write.print(1, 2)
                self.__write.message = "   Using data up to the number of complete pairs (%d)." % (numCompletePairs)
                self.__write.print(1, 2)
            # Append values:
            for i in range(0, numCompletePairs, 1):
                self.__xVals.append( xVals[i] )
                self.__yVals.append( yVals[i] )
                self.__numDataPoints += 1

        return

    def __setXYError(self, xError=None, yError=None):
        """Sets the X/Y error values if given."""
        if( not xError == None ):
            self.__setXError(xError)
        if( not yError == None ):
            self.__setYError(yError)
        return

    def __setXError(self, xError):
        """Sets the X-error values."""
        xError = self.__validateXYErrorInput(xError, "x-error")
        if ( not xError == None ):
            for i in range(0, len(xError), 1):
                self.__xError.append( xError[i] )

        return

    def __setYError(self, yError):
        """Sets the Y-error values."""
        yError = self.__validateXYErrorInput(yError, "y-error")
        if ( not yError == None ):
            for i in range(0, len(yError), 1):
                self.__yError.append( yError[i] )

        return

    def addPoint(self, xVal, yVal, xErr=None, yErr=None):
        """Adds a point (and any potential data) to the Scatter object"""

        # Ensure X/Y variable is float/int and append:
        if ( not isinstance(xVal, (float, int)) ):
            try:
                xVal = float(xVal)
            except:
                self.__write.message = "Unable to convert the X-value to float: ", xVal
                self.__write.print(1, 2)
                xVal = self.__defaultXValue
                self.__write.message = "   Using value of %.3f for the X-value." % (xVal)
                self.__write.print(1, 2)
        self.__xVals.append( xVal )
        if ( not isinstance(yVal, (float, int)) ):
            try:
                yVal = float(yVal)
            except:
                self.__write.message = "Unable to convert the Y-value to float: ", yVal
                self.__write.print(1, 2)
                yVal = self.__defaultYValue
                self.__write.message = "   Using value of %.3f for the Y-value." % (yVal)
                self.__write.print(1, 2)
        self.__yVals.append( yVal )
        self.__numDataPoints += 1

        # Add x/y error points if present:
        if ( len(self.__xError) > 0 ):
            if ( xErr == None ):
                self.__xError.append( self.__defaultXError )
            else:
                if ( not isinstance(xErr, (float, int)) ):
                    try:
                        xErr = float(xErr)
                    except:
                        self.__write.message = "Unable to convert the X-error value to float: ", xErr
                        self.__write.print(1, 2)
                        xErr = self.__defaultXError
                        self.__write.message = "   Using value of %.3f for the X-error value." % (xErr)
                        self.__write.print(1, 2)
                self.__xError.append( xErr )
        if ( len(self.__yError) > 0 ):
            if ( yErr == None ):
                self.__yError.append( self.__defaultYError )
            else:
                if ( not isinstance(yErr, (float, int)) ):
                    try:
                        yErr = float(yErr)
                    except:
                        self.__write.message = "Unable to convert the Y-error value to float: ", yErr
                        self.__write.print(1, 2)
                        yErr = self.__defaultYError
                        self.__write.message = "   Using value of %.3f for the Y-error value." % (yErr)
                        self.__write.print(1, 2)
                self.__yError.append( yErr )

        return

    def getNumDataPoints(self):
        """Returns the number of data points that exist"""
        return self.__numDataPoints

    def getXValues(self):
        """Returns the X values of the points as a tuple"""
        xVals = None
        if ( len(self.__xVals) > 0 ):
            xVals = []
            for i in range(0, len(self.__xVals), 1):
                xVals.append(self.__xVals[i])
        return xVals

    def getYValues(self):
        """Returns the Y values of the points as a tuple"""
        yVals = None
        if ( len(self.__yVals) > 0 ):
            yVals = []
            for i in range(0, len(self.__yVals), 1):
                yVals.append(self.__yVals[i])
        return yVals

    def getXError(self):
        """Returns the X-error values of the points as a tuple"""
        xError = None
        if ( len(self.__xError) > 0 ):
            xError = []
            for i in range(0, len(self.__xError), 1):
                xError.append(self.__xError[i])
        return xError

    def getYError(self):
        """Returns the Y-error values of the points as a tuple"""
        yError = None
        if ( len(self.__yError) > 0 ):
            yError = []
            for i in range(0, len(self.__yError), 1):
                yError.append(self.__yError[i])
        return yError

    def getMaxXError(self):
        """Finds the max X error value"""
        maxErr = None
        if ( len(self.__xError) > 0 ):
            maxErr = 0.00
            for i in range(0, len(self.__xError), 1):
                maxErr = max(maxErr, self.__xError[i])

        return maxErr

    def getMaxYError(self):
        """Finds the max Y error value"""
        maxErr = None
        if ( len(self.__yError) > 0 ):
            maxErr = 0.00
            for i in range(0, len(self.__yError), 1):
                maxErr = max(maxErr, self.__yError[i])

        return maxErr

    def getMaxTotalError(self):
        """Finds the max X error value (None means no errors are present)"""
        maxXErr = self.getMaxXError()
        maxYErr = self.getMaxYError()

        maxErrorVal = 0.00
        if ( maxXErr == None and maxYErr == None ):
            maxErrorVal = None
        elif ( maxXErr == None ):
            maxErrorVal = maxYErr
        elif ( maxYErr == None ):
            maxErrorVal = maxXErr
        else:
            maxErrorVal = max( maxXErr, maxYErr)

        return maxErrorVal
