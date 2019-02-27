

import datetime as dtime
import time
import math
import numpy as np

import GroupClass
from GroupClass import Group

class ManyGroup:
    """The 'ManyGroup' class is used to contain groups of people and can plot
    when the people came to visit"""


    def __init__(self):
        # Create empty list of groups
        self.__groups = []
        self.__numGroups = len(self.__groups)

    def __IOhandler(self, flag=0, message="Unknown error occurred"):
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
            statement = leftHandFlags[flag] + "   " + flagWord[flag] + ": " + message.rstrip()

        # Print out statement
        print(statement)


    def __checkExists(self, i=0):
        """Ensure that the group exists"""
        # Ensures the member exists

        # Check if grou[] exist
        if ( self.__numGroups <= 0 ):
            # No groups - cannot return anything
            self.__groupIO(2, "Cannot print group information; no groups exist.")
            return -1

        # Ensure member exists
        j = i
        if ( i < 0 ) or ( i >= self.__numGroups ):
            # Error - out of bound
            errorMessage = "Group " + str(i) + \
                " of the day does not exist. First group member " + \
                "will be used instead."
            self.__IOHandler(1, errorMessage)
            j = 0

        return j


    def __printGroup(self, i=0):
        # Prints name and age of member

        # Check for groups
        self.__checkExists(i)

        # Obtain information to print
        self.__groups[i].printDetails()


    def add_group(self, newGroup=Group()):
        # Add a group to the list
        self.__groups.append( newGroup )
        self.__numGroups += 1

    def add_groups(self, numGroups=1):
        for i in range(0, numGroups, 1):
            self.add_group()

    def getGroup(self, i=0):
        # Return a group member

        # Check for members
        self.__checkExists(i)

        # Return the member
        return self.__groups[i]


    def getNumGroups(self):
        return self.__numGroups


    def printDetails(self):
        # Print details of all groups
        self.__IOhandler(3, "=================================================")
        self.__IOhandler(3, "There are " + str(self.__numGroups) + " groups from today.")
        self.__IOhandler(3, "=================================================")
        if ( self.__numGroups > 0 ):
            for i in range(0, self.__numGroups, 1):
                self.__printGroup(i)



    def __getAllPeople(self):
        """Returns a consolidated list of group members
        (all members of all groups are here)"""
        # Obtain list of people
        allPeople = Group()
        if ( self.__numGroups > 0 ):
            for i in range(0, self.__numGroups, 1):
                if ( self.__groups[i].getNumMembers() > 0 ):
                    for j in range(0, self.__groups[i].getNumMembers(), 1):
                        allPeople.add_member( self.__groups[i].getMember(j) )

        return allPeople


    def saveData(self, fileName = None):
        """Saves all group data accoding to group's 'saveData' routine"""

        # Generate fileName if none passed in
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

        # Write group data to the file
        if ( self.getNumGroups() > 0 ):
            for i in range(0, self.getNumGroups(), 1):
                self.getGroup(i).saveData(fileName)


    def __printInstructions(self, stopFlags = [None], instruct = None ):
        """Prints out instructions for user during data collection"""

        self.__IOhandler(3, " ")
        self.__IOhandler(3, " ")
        self.__IOhandler(3, "---------------------------------------------------------------------------")
        self.__IOhandler(3, " ")
        self.__IOhandler(3, "To collect data, you may utilize a few methods...")
        self.__IOhandler(3, "   1. Enter a number. That many people will be added as a 'group' of people.")
        self.__IOhandler(3, "     1.1: A negative number will result in NO people being added (or deleted)")
        self.__IOhandler(3, "     1.2: A zero (0) will result in one (1) person being added as a group.")
        self.__IOhandler(3, "   2. Enter some characters (ex. 'candies'). This adds as many people as")
        self.__IOhandler(3, "      characters you entered.")
        self.__IOhandler(3, "     2.1: Regardless of what the character is, this is done (i.e. you may")
        self.__IOhandler(3, "          enter four (4) spaces to add four (4) people as a group)")
        self.__IOhandler(3, "   3. You may enter any combination of numbers and letters - this is treated")
        self.__IOhandler(3, "      the same as item (2).")
        self.__IOhandler(3, "   4. Forget the instructions? During data collection, just input '" + instruct + "',")
        self.__IOhandler(3, "      or anything starting with that, and these instructions will be reprinted.")
        self.__IOhandler(3, " ")
        self.__IOhandler(3, "Stopping Data Collection:")
        self.__IOhandler(3, "   To STOP data collection, enter any of the following keywords (regardless of case):")
        for i in range(0, len(stopFlags), 1):
            stopMessage = "      " + str(i+1) + ": " + stopFlags[i]
            self.__IOhandler(3, stopMessage)
        self.__IOhandler(3, " ")
        self.__IOhandler(3, "---------------------------------------------------------------------------")
        self.__IOhandler(3, " ")


    def collectData(self, fileName = None):
        """Collect data for the object"""
        instruct = "instruct"
        stopFlags = ["stop", "quit", "done", "end", "exit"]
        collect = True

        # Set default name
        if ( fileName == None ):
            fileName = "TrickOrTreaters-" + dtime.datetime.now().year + ".txt"

        # Print data collection instructions
        self.__printInstructions(stopFlags, instruct)
        self.__IOhandler(3, "Now that you are acquanted, it's time.")
        time.sleep(5)
        self.__IOhandler(3, "")
        self.__IOhandler(3, "\t READY...")
        time.sleep(2)
        self.__IOhandler(3, "\t SET...")
        time.sleep(2)
        self.__IOhandler(3, "GO!")
        self.__IOhandler(3, "")
        self.__IOhandler(3, "")


        # Collect group data
        self.__IOhandler(3, "--------------------------")
        self.__IOhandler(3, "DATA COLLECTION:")
        self.__IOhandler(3, "--------------------------")
        while ( collect ):
            # Collect information on groups
            data = input(" DATA >> ")
            data.lower()

            # Stop data collection
            for i in range(0, len(stopFlags), 1):
                if ( data == stopFlags[i] ):
                    collect = False
                    continue

            # Check if to reprint instructions
            if ( data[ : len(instruct) ] == instruct ):
                self.__printInstructions(stopFlags, instruct)
                continue

            # Check if a number (if collection occurs)
            if ( not collect ):
                continue
            try:
                numMembers = int( data )
                if ( numMembers == 0 ):
                    # Can this be?
                    self.__IOhandler(1, "Are you teasing me? You didn't have any visitors, did you? I'll count 1 anyways...")
                    numMembers = 1

                # Add group members
                if ( numMembers <= 0 ):
                    self.__IOhandler(2, "You entered a negative value...are you trying to remove groups? Ignoring input.")
                    continue
            except:
                # Entered characters instead...
                numMembers = len(data)
                if ( numMembers == 0 ):
                    self.__IOhandler(3, "You didn't enter anything, but I'll assume you wanted 1 person added.")
                    numMembers = 1

            # Obtain group data, save data
            self.add_group( Group(numMembers) )
            self.__IOhandler(3, "A group of " + str(numMembers) + " people was added [" \
            + str( self.getNumGroups() ) + " group(s)].")


        # Done collecting data, now save data
        self.__IOhandler(3, "--------------------------")
        self.__IOhandler(3, "Data collection is done, saving data...")
        self.saveData(fileName)
        self.__IOhandler(3, "--------------------------")



        # now plot data
        self.__IOhandler(3, "--------------------------")
        self.__IOhandler(3, "Plotting data...")
        self.__IOhandler(3, "--------------------------")
        self.plotVisits()



    def plotVisits(self, startT=-1, endT=-1, deltaT=-1):
        # Function plots graphically when people came to visit the house
        """This function plots when each person came to visit"""

        # Define detault Values
        defaultBinWidth = 10*60   # Default of 10 minutes wide bins


        # Obtain group of people from the day
        allPeople = self.__getAllPeople()
        numTimes = allPeople.getNumMembers()

        # Ensure that members exist in the group
        if ( allPeople.getNumMembers() <= 0 ):
            return (-1)


        # Print statistics on group
        allPeople.printTimeStatistics()


        # Obtain default range of histogram and numbre of bins
        xMin = allPeople.getFirstTime()
        xMax = allPeople.getLastTime()
        range = allPeople.getTimeRange()
        numBins = range / defaultBinWidth
        binWidth = range / numBins


        # Set histogram bin information (default values)
        histXMin = xMin
        histXMax = xMax
        histBinWidth = binWidth
        histNumBins = numBins

        # Obtain user-specific start, end and bin width times
        if ( startT >= 0 ):
            histXMin = startT
        if ( endT > 0 ):
            if ( endT > startT ):
                histXMax = endT
        if ( deltaT > 0 ):
            histBinWidth = deltaT

        # Ensure more than 10 bins exist
        histRange = histXMax - histXMin
        histNumBins = histRange / histBinWidth
        if ( histNumBins < 10 ):
            # Make 10 bins
            histNumBins = 10
            histBinWidth = histRange / histNumBins


        self.__IOhandler(3, "")
        self.__IOhandler(3, "==============================================")
        self.__IOhandler(3, "HISTOGRAM INFORMATION:")
        self.__IOhandler(3, "==============================================")
        histogramMessage = "The histogram will range from " + \
            str(histXMin) + " (s) to " + str(histXMax) + " (s), with " + \
            str(histNumBins) + " bins of width " + str(histBinWidth) + " (s)."
        self.__IOhandler(3, histogramMessage)


        allPeople.printTimeHistogram(histXMin, histXMax, int(histNumBins), "seconds", "hours")
