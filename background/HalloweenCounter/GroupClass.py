

import math   # For sqrt() function
# For plotting
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


import PersonClass
from PersonClass import Person


class Group:
    """The 'Group' class is used to determine statistics on groups of people
    and when they stopped by."""


    def __init__(self, numMembers = 0):
        """Group Constructor"""
        # Create empty list of people
        self.__members = []

        # Generate some people
        if ( numMembers > 0 ):
            for i in range(0, numMembers, 1):
                self.__members.append( Person() )

        # Obtain number of people
        self.__numMembers = len(self.__members)

    def __groupIO(self, flag=0, message="Unknown error occurred"):
        # Handles all printing within the class
        # Values of FLAG:
        #    =0: Fatal Error [quits]
        #    =1: Error [resolves]
        #    =2: Warning [resolves]
        #    =3: Comment [no action]
        leftHandFlags = ("FE", "E ", "W ", "  ")
        flagWord = ("Fatal Error", "Error", "Warning", "Comment")

        # Ensure valid flag
        if flag < 0 or flag > 3:
            # Default to fatal error if invalid value of FLAG given
            flag = 0

        # Obtain statement type
        if ( len(message)==0 ):
            statement=""
        else:
            statement = leftHandFlags[flag] + "   " + flagWord[flag] + ": " + message.strip()

        # Print out statement
        print(statement)

    def __checkExists(self, i=0):
        """Ensure that the group member exists"""
        # Ensures the member exists

        # Check if members exist
        if ( self.__numMembers <= 0 ):
            # No members - cannot return anything
            self.__groupIO(2, "Cannot print member information; no group members exist.")
            return -1

        # Ensure member exists
        j = i
        if ( i < 0 ) or ( i >= self.__numMembers ):
            # Error - out of bound
            errorMessage = "Member " + str(i) + \
                " of the group does not exist. First group member " + \
                "will be used instead."
            self.__groupIO(1, errorMessage)
            j = 0

        return j

    def __printMember(self, i=0):
        # Prints name and age of member

        # Ensure existence
        i = self.__checkExists(i)

        # Obtain information to print
        myMember = self.__members[i]
        memberInfo = ""
        if ( myMember.getFirstName() != "" ):
            memberInfo = myMember.getFirstName().strip()

        if ( myMember.getLastName() != "" ):
            memberInfo += " " + myMember.getLastName().strip()

        if ( myMember.getAge() >= 0 ):
            memberInfo += ", age " + str( myMember.getAge() ) + ","

        memberInfo += " visited on " + str ( myMember.getTime() )

        # Print member information
        self.__groupIO(3, memberInfo)


    def add_member(self, member=Person()):
        # Add a person to the list
        self.__members.append( member )
        self.__numMembers += 1

    def getMember(self, i=0):
        # Return a group member

        # Ensure existence
        i = self.__checkExists(i)
        if ( i < 0 ):
            return

        # Return the member
        return self.__members[i]


    def printDetails(self):
        # Print details of all __members
        self.__groupIO(3, "-------------------------------------------------")
        self.__groupIO(3, "There are " + str(self.__numMembers) + " members in this group.")
        self.__groupIO(3, "-------------------------------------------------")
        if ( self.__numMembers > 0 ):
            for i in range(0, self.__numMembers, 1):
                self.__printMember(i)



    def getAge(self, i=0):
        """Returns age of a member in the array"""
        # Returns age of member i

        # Ensure existence
        i = self.__checkExists(i)
        if ( i < 0 ):
            return -1

        return self.__members[i].getAge()


    def getNumMembers(self):
        """Returns number of members in the group"""
        # Returns the number of members that exist in the group
        return self.__numMembers


    def getTime(self, i=0):
        """Returns the time that a group member visisted"""
        # Returns the time the member i visited

        # Ensure existence
        i = self.__checkExists(i)
        if ( i < 0 ):
            return -2

        return self.__members[i].getTime()


    def getMeanAge(self):
        # Obtain mean age of group (for those whose age was input)
        if ( self.__numMembers <= 0 ):
            self.__groupIO(2, "Mean age cannot be determined, no group members exist.")
            return -1

        mean = 0.0
        numAgeGiven = 0
        for i in range(0, self.__numMembers, 1):
            age = self.__members[i].getAge()
            if ( age >= 0 ):
                mean += age
                numAgeGiven += 1

        # Obtain mean
        if ( numAgeGiven > 0 ):
            mean = mean / numAgeGiven
        else:
            mean = -1

        # Return mean
        return mean


    def getMeanTime(self):
        """Returns the average time group members arrived"""
        meanTime = 0

        # Sum time all group members arrived
        sum = 0
        for i in range(0, self.getNumMembers(), 1):
            sum += self.getTime(i)

        # Calculate mean time
        meanTime = sum / self.getNumMembers()

        return meanTime


    def getStdDevTime(self):
        """Returns the std. dev. of times group members arrived"""
        stdDevTime = 0

        # Obtain mean value
        meanTime = self.getMeanTime()

        # Sum all squared deviations from mean
        deviationSum = 0
        for i in range(0, self.getNumMembers(), 1):
            deviationSum += pow( (self.getTime(i) - meanTime ), 2 )


        # Divide by number of samples
        stdDevTime = math.sqrt( deviationSum / self.getNumMembers() )


        return stdDevTime


    def getFirstTime(self):
        """Returns the time (in seconds) that the first group member visited"""

        firstTime = self.getMember(0).getTime()
        for i in range(1, self.getNumMembers(), 1):
            firstTime = min( firstTime, self.getMember(i).getTime() )

        return firstTime


    def getLastTime(self):
        """Returns the time (in seconds) that the last group member visited"""

        lastTime = self.getMember(0).getTime()
        for i in range(1, self.getNumMembers(), 1):
            lastTime = max( lastTime, self.getMember(i).getTime() )

        return lastTime


    def getTimeRange(self):
        """Returns the time difference between when the last and first group members arrive"""
        return ( self.getLastTime() - self.getFirstTime())


    def printTimeStatistics(self):
        """Prints group statistics"""

        # Default values for statistics
        mean   = self.getMeanTime()
        stdDev = self.getStdDevTime()
        xMin   = self.getFirstTime()
        xMax   = self.getLastTime()
        range  = self.getTimeRange()



        # Print statistics on group
        self.__groupIO(3, "")
        self.__groupIO(3, "")
        self.__groupIO(3, "==========================================")
        self.__groupIO(3, "TIMES STATISTICS TABLE (values in seconds)")
        self.__groupIO(3, "==========================================")
        self.__groupIO(3, "mean = " + str(mean) )
        self.__groupIO(3, "std. dev = " + str(stdDev) )
        self.__groupIO(3, "range = " + str(range) )
        self.__groupIO(3, "minX  = " + str(xMin) )
        self.__groupIO(3, "maxX  = " + str(xMax) )


    def __generateTimeList(self):
        """Generate a list of times that people in the group visited"""

        peopleTimes = []
        for i in range(0, self.getNumMembers(), 1):
            peopleTimes.append( self.getTime(i) )

        return peopleTimes

    def saveData(self, fileName = None):
        """Saves all member information to a file"""

        # Generate fileName
        if ( fileName == None ):
            # Obtain specific date and time
            groupTime = dtime.datetime.now()

            # Obtain date
            day = groupTime.day
            month = groupTime.month
            year = groupTime.year
            date = str(month) + "-" + str(day) + "-" + str(year0)

            # Obtain specific time (military)
            hour = groupTime.hour
            minutes = groupTime.minute
            sec = groupTime.second
            time = str(hour) + str(minutes) + ":" + str(sec)
            fileName = "GroupData." + date + "." + timestamp


            # Check if file exists
            notExists = True
            numTries = 0
            while ( notExists ):
                tempName = fileName + ".txt"
                numTries += 1
                try:
                    temp = open(tempName, 'r')
                    # Success means that the file does exist; close and modify name
                    temp.close()
                    if ( numTries <= 1 ):
                        fileName += "-"
                    fileName += "a"
                except FileNotFoundError:
                    # File doesn't exist, we can use it.
                    notExists = False

            # File does NOT exist now (given default attempts) - cannot overwrite!
            fileName += ".txt"

        # Print what file data is written to
        try:
            myFile = open(fileName, "a")
        except FileNotFoundError:
            self.__groupIO(1, "File '" + fileName + "' was not able to be opened.")
            return

        for i in range(0, self.getNumMembers(), 1):
            # Obtain a string for each person and write that to the file
            personData = self.getMember(i).getData()
            myFile.write(personData + "\n")

        # Close file (no more data)
        myFile.close()
        return

    def printTimeHistogram(self, minX=16, maxX=22, numBins=36, units="hours", histUnits="hours"):
        """Print a histogram of Num. people vs. when they arrived"""
        # Note: Default times are [4 pm] to [10 pm] with [10 min] intervals


        # Default values
        someSpace = 0.00   # Gives looser spacing of bins
        allowedUnits = ["sec", "min", "h"]
        numUnits = len(allowedUnits)
        allowedUnitLen = []
        for i in range(0, numUnits, 1):
            allowedUnitLen.append( len(allowedUnits[i]) )


        # Generate bin boundaries
        minX = ( 1 - someSpace ) * minX   # Give some space on left  edge of histogram
        maxX = ( 1 + someSpace ) * maxX   # Give some space on right edge of histogram
        if ( maxX <= minX ):
            maxX = 1.3 * minX


        # Convert to desired units
        units = units.lower().strip()
        histUnits = histUnits.lower().strip()
        # Ensure allowed units were passed in
        inputUnit = -10
        histUnit  = -10
        for i in range(0, numUnits, 1):
            if ( inputUnit < 0 ):
                if ( units[ : allowedUnitLen[i] ] == allowedUnits[i] ):
                    inputUnit = i
            if ( histUnit < 0 ):
                if ( histUnits[ : allowedUnitLen[i] ] == allowedUnits[i] ):
                    histUnit = i
        # Print if invalid, use default
        if ( inputUnit < 0 ):
            self.__groupIO(2, "Invalid time unit specified for desired histogram input time (" + units + "). Default of hours will be used.")
            inputUnit = 2
        if ( histUnit < 0 ):
            self.__groupIO(2, "Invalid time unit specified for desired histogram time (" + histUnits + "). Default of hours will be used.")
            histUnit = 2


        # Convert as necessary
        identifier = (histUnit - inputUnit)
        if ( identifier == 0 ):
            # Same units, no converting necessary
            self.__groupIO(3, "Histogram will be printed with time in units of hours.")
        elif ( identifier < 0 ):
            # Convert from hours to minutes, minutes to seconds, or hours to seconds
            self.__groupIO(3, "Down converting time from (" + allowedUnits[inputUnit] + ") to (" + allowedUnits[histUnit] + ") for the histogram.")
            minX = minX * ( pow(60, -identifier) )
            maxX = maxX * ( pow(60, -identifier) )
        elif ( identifier > 0 ):
            # Convert from seconds to minutes, minutes to hours, or seconds to hours
            self.__groupIO(3, "Up converting time from (" + allowedUnits[inputUnit] + ") to (" + allowedUnits[histUnit] + ") for the histogram.")
            minX = minX * ( pow(60, -identifier) )
            maxX = maxX * ( pow(60, -identifier) )



        # Generate bin boundaries
        xRange = maxX - minX
        binWidth = xRange / numBins
        bin = []
        binX = minX
        for i in range(0, numBins+1, 1):
            binX += binWidth
            bin.append( binX )


        # Generate list of times
        peopleTimes = self.__generateTimeList()
        # Convert times
        for i in range(0, self.getNumMembers(), 1):
            peopleTimes[i] *= ( pow(60, -identifier) )

        # Generate plot objects
        fig, ax = plt.subplots()

        # the histogram of the data
        n, bins, patches = ax.hist(peopleTimes, bin)

        # Set labeling
        xLabel = 'Military Time (' + allowedUnits[histUnit] + ')'
        ax.set_xlabel(xLabel)
        ax.set_ylabel('Number of Trick-or-Treaters')
        ax.set_title(r"How Busy was I on Halloween? Here's the visitors I had.")

        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()
