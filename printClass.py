
################################################################################
# File documentation:
"""
This module contains the printing class. This class controls all printing of
messages.
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

# VERSION Number:
__version__ = "1.0.0"


class Print:
    """
    This is a class that is used to print messages by various clients
    """
    __verboseLimit = 0
    message        = ""
    __print        = None


    # Default printing function:
    def __printDefault(self, msgType=None, verbFlag=None, verbLimit=None, message=None):
        """Handles all printing within the class"""
        # DEFAULT VARIABLES:
        __errPrnt = 0
        __wrnPrnt = 1
        __cmtPrnt = 2
        __blkPrint = 3
        __defaultMessageTypes = ("(E)     Error:", "(W)   Warning: ", "      Comment: ", "")
        __defaultVerbose = 2
        __defaultVerboseLimit = 2

        # Set message type:
        if ( msgType == None ):
            msgType = __errPrnt

        # Set verbosity flag:
        if ( verbFlag == None ):
            verbFlag = __defaultVerbose
        elif ( verbFlag < 0 ):
            verbFlag = 0

        # Set verbosity limit:
        if ( verbLimit == None ):
            verbLimit = __defaultVerboseLimit
        elif ( verbLimit < 0 ):
            verbLimit = 0

        # Set message:
        if ( message == None ):
            message = ""

        # Determine message type (NOTE: for negative msgType print to stderr)
        prntType = abs(msgType)
        if not ( (prntType == __errPrnt) or (prntType == __wrnPrnt) or (prntType == __cmtPrnt) or (prntType == __blkPrint)):
            prntType == __errPrnt


        # Check if verbosity flag is high enough:
        if ( verbFlag <= verbLimit or prntType == __errPrnt ):
            # Print all messages below the verbosity (and all error messages)

            # Concatenate message w/ flag:
            if ( not prntType == __blkPrint ):
                prntMessage = __defaultMessageTypes[prntType] + message.rstrip()
            else:
                prntMessage = ""

            # Print message
            if ( (prntType == __errPrnt) or (msgType < 0) ):
                print(prntMessage, file=sys.stderr)
            else:
                print(prntMessage)

        # Clear message:
        self.__message = ""

    def __init__(self, newVerbose = None, newPrint = None):
        """Constructor for printing class"""

        # Set verbosity limit:
        if ( newVerbose == None ):
            self.__verboseLimit = 3
        else:
            if ( newVerbose < 0 ):
                newVerbose = 0
            self.__verboseLimit = newVerbose


        # Set print function:
        if ( newPrint == None ):
            self.__print = self.__printDefault
        else:
            self.print = newPrint


    def print(self, msgType, verbFlag):
        """Prints out messages based on verbosity"""
        self.__print(msgType, verbFlag, self.__verboseLimit, self.message)
        self.message = ""   # Reset message
