
################################################################################
# File documentation:
"""
This module is simply used for testing syntax and ideas; nothing more. Sorry!
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


letsTest = False


class Food:

    __wasAlive = True

    def __init__(self, newTasty = True):
        print("New Food enters...")
        self.tasty = newTasty
        print("New Food leaves...")

    def initFood(self, newTasty):
        self.__init__(newTasty)

    def toggleTasty(self, newTasty):
        self.tasty = newTasty

    def printTasty(self):
        if ( self.tasty ):
            print("This food is tasty!")
        else:
            print("Yuck!")

class Vegetable(Food):

    __nutritious = True

    def __init__(self, newColor = "green"):
        print("New vegi enters...")
        super(Vegetable, self).__init__()
        self.color = newColor
        print("New vegi leaves...")

    def initVegetable(newColor):
        self.__init__(newColor)

    def printColor(self):
        print("This vegi is colored %s." % (self.color) )
        self.printTasty()

class Meat(Food):

    __tough = True

    def __init__(self, newMeat = "Chicken"):
        print("new meat")
        super(Meat, self).__init__()
        self.meat = newMeat
        print("old meat")

    def printMeat(self):
        print("%s is my favorite meat!" %(self.meat) )

class Pepper(Vegetable):

    fromMexico = True

    def __init__(self, isSpicy = True):
        print("Enter new pepper!")
        super(Pepper, self).__init__()
        self.__isSpicy = isSpicy
        print("Leave new pepper...")

    def printSpicy(self):
        if ( self.__isSpicy):
            print("This is a spicy one!")
        else:
            pritn("This is a sweet one!")


    def printAllData(self):
        print("\n------------------------------------")
        print(self)
        self.printSpicy()
        self.printColor()
        self.printTasty()

class Dinner(Meat, Pepper):

    def __init__(self, wasYummy = True):
        print("new dinner")
        super(Dinner, self).__init__()
        self.__wasYummy = wasYummy
        print("Dinner done.")

    def printFood(self):
        if ( self.__wasYummy ):
            print("Tonight's dinner was yummy!")
        else:
            print("Tonight's dinner was \"meh.\"")
        # Print from Food class:
        print("Food Class:")
        print("\t", self.tasty)
        print("From Vegi Class:")
        print("\t", self.color)
        print("From Meat Class:")
        print("\t", self.meat)
        print("From Pepper Class:")
        print("\t", fromMexico)
        print("\t", self.__isSpicy)
