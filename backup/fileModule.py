
################################################################################
# File documentation:
"""
This module contains various procedures to identify "facts" relating to files
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
import os.path as path


# Modules:
from printClass import Print

# VERSION Number:
__version__ = "1.0.0"


# Module defaults:
fileAppends = ( "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
"m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
numFileAppends = len(fileAppends)
__filePrint    = Print()



def fileExists(fileName = None):
    """Determines if a file exists in the directory"""
    if ( not fileName == None ):
        doesFileExist = path.isfile( fileName )
    else:
        doesFileExist = False
        __filePrint.message = "No filename was passed in during existence check."
        __filePrint.print(1, 2)

    return doesFileExist



def deleteFile( fileName ):
    """Deletes a file"""

    # Check for "wildcard"
    if ( "*" in fileName ):
        doesFileExist = True
    else:
        # Ensure file exists (if no wild card)
        doesFileExist = fileExists( fileName )


    # Remove file if appropriate
    if ( doesFileExist ):
        # File exists, delete it:
        os.remove( fileName )
        __filePrint.message = "Removed file \"%s\"." % (fileName)
        __filePrint.print(2, 3)
    else:
        # File doesn't exist, tell user:
        __filePrint.message = "File \"%s\" does not exist. Cannot delete file." % (fileName)
        __filePrint.print(1, 2)


def verifyFileName( fileName = None, ext = ".png" ):
    """Determines if filename is valid (if not, obtains filename that is)"""
    if ( fileName == None ):
        fileName = "file.txt"
        __filePrint.message = "No filename was passed to validate filename. Assuming name is \"%s\"." % (fileName)
        __filePrint.print(1, 2)


    # Verify file exists:
    doesFileExist = fileExists( fileName + ext )


    if ( doesFileExist ):
        # File exists; give new name and check again
        iteration = 0
        cycleNum  = 0
        while ( doesFileExist ):

            # Obtain valid index for new letter to try:
            iteration = iteration % numFileAppends
            tempFile = fileName + fileAppends[iteration]
            __filePrint.message = "File \"%s\" exists. Trying \"%s\" instead." % ((fileName+ext), (tempFile+ext))
            __filePrint.print(1, 2)

            # Check if file exists:
            doesFileExist = fileExists( tempFile + ext )

            # Go to next iteration
            if ( doesFileExist ):
                iteration = iteration + 1

                # Append a letter, check existence:
                if ( iteration >= numFileAppends ):
                    # Already cycled through list of letters, append the next letter
                    cycleNum = cycleNum + 1
                    cycleNum = cycleNum % numFileAppends
                    fileName = fileName + fileAppends[cycleNum]

            else:
                # Found a new filename;
                fileName = tempFile


    # Found a filename that doesn't exist (doesn't overwrite)
    return (fileName + ext)



def fileLength( fileName ):
    """Determines the length of a file"""
    doesFileExist = fileExists( fileName )

    if ( doesFileExist ):
        file = open(fileName, 'r', encoding='ascii', errors='ignore')
        # Determine number of lines in file
        k = 0
        for k, l in enumerate(file):
            pass
        file.close()
        return (k+1) # Return length of file
    else:
        __filePrint.message = "File ", fileName.strip(), " does not exist in this directory."
        __filePrint.print(1, 2)
        return 0


def readFile( fileName, printData = False ):
    """Reads data from a file, then returns the read data"""

    # Initialize returned object:
    fileData = []


    # Obtain data
    doesFileExist = fileExists( fileName )
    if ( doesFileExist ):
        # File exists, get data:
        numLines = fileLength( fileName )

        # Open file for reading:
        thisFile = open(fileName, 'r', encoding='ascii', errors='ignore')
        for i in range(0, numLines, 1):
            lineData = thisFile.readline().strip().lower()
            fileData.append( lineData )

            # Print line if desired:
            if ( printData ):
                __filePrint.message = lineData
                __filePrint.print(2, 0)

        # Close file now:
        thisFile.close()

    else:
        # File doesn't exist, no data to return
        __filePrint.message = "File \"%s\" doesn't exists." % (fileName)
        __filePrint.print(1, 2)


    # Return object:
    return fileData
