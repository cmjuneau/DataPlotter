
import datetime as dtime
import time

import numpy as np


class Person:
    """The 'Person' class is used to store information about each person that
    stops at the house on Halloween."""

    np.random.seed(19680801)

    def __init__(self, time_sec=None, firstName="", lastName="", age=-1, gender="u", numCandy=1, costume="none"):
        """Constructor for a person class"""
        testing = False
        # Person constructor
        self.__firstName = firstName
        self.__lastName  = lastName
        self.__age       = age
        self.__gender    = gender

        # Halloween specific information
        if ( time_sec == None ):
            time = dtime.datetime.now()
            time_sec = time.second + 60*(time.minute + 60*time.hour) # Convert to seconds
        self.__time      = time_sec    # Time the person was at door
        self.__numCandy  = numCandy   # Number of Candy pieces received
        self.__costume   = costume    # Costume person was wearing


        if ( testing ):
            # example data for a Guassian distribution
            mu = 68400  # mean of distribution (centered on 7 pm)
            sigma = 5000  # standard deviation of distribution (std. dev. of 1.37 hours)
            x = mu + sigma * np.random.randn()
            self.__time = x

    def getAge(self):
        return self.__age

    def setAge(self, newAge):
        self.__age = newAge

    def getTime(self):
        return self.__time

    # No setTime method

    def getCostume(self):
        return self.__costume

    def setCostume(self, costume):
        self.__costume = costume

    def getGender(self):
        return self.__gender

    def setGender(self, gender):
        self.__gender = gender

    def getFirstName(self):
        return self.__firstName

    def setFirstName(self, name):
        self.__firstName = name

    def getLastName(self):
        return self.__lastName

    def setLastName(self, name):
        self.__lastName = name

    def getNumCandy(self):
        return self.__numCandy

    def setNumCandy(self, numCandy):
        self.__numCandy = numCandy

    def getData(self):
        personData = ""
        delimeter = "; "


        personData +=                  self.getFirstName()
        personData += delimeter +      self.getLastName()
        personData += delimeter + str( self.getTime() )
        personData += delimeter + str( self.getAge() )
        personData += delimeter +      self.getGender()
        personData += delimeter + str( self.getNumCandy() )
        personData += delimeter +      self.getCostume()

        return personData
