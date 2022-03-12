
"""
T1MF_Interface.py
Created 10/12/2021
"""
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.type1.sets.T1MF_Interface import T1MF_Interface

class T1MF_Prototype(T1MF_Interface):
    """
    Class T1MF_Prototype
    Building on our interface class for the membership functions with base methods

    Parameters: None

    Functions:
        getName
        setName
        getSupport
        setSupport
        setLeftShoulder
        setRightShoulder
        isLeftShoulder
        isRightShoulder
        getDefuzzifiedCentroid
        getDefuzzifiedCOS
    """

    def __init__(self,name: str) -> None:
        super().__init__()
        self.name = name
        self.isLeftShoulder_ = False
        self.isRightShoulder_ = False
        self.support = Tuple()
        self.DEBUG = False

    def getName(self) -> str:
        """Return the name of the function"""
        return self.name

    def setName(self, name: str) -> None:
        """Set the name of the function"""
        self.name = name

    def getSupport(self) -> Tuple:
        """Get the current support tuple"""
        return self.support

    def setSupport(self, support: Tuple) -> None:
        """Change current support tuple to parameter"""
        self.support = support

    def setLeftShoulder(self, value: bool) -> None:
        """Set left shoulder value"""
        self.isLeftShoulder_ = value

    def setRightShoulder(self, value: bool) -> None:
        """Set right shoulder value"""
        self.setRightShoulder_ = value

    def isLeftShoulder(self) -> bool:
        """Return current left shoulder bool"""
        return self.isLeftShoulder_

    def isRightShoulder(self) -> bool:
        """Return current right shoulder bool"""
        return self.isRightShoulder_

    def getDefuzzifiedCentroid(self, numberOfDiscretizations: int) -> float:
        """Returns the defuzzified value of this set computed using the centroid algorithm."""
        if self.DEBUG:
            print(self.getSupport())
        stepSize = self.getSupport().getSize()/(numberOfDiscretizations-1.0)
        currentStep = self.getSupport.getLeft()
        numerator = 0.0
        denominator = 0.0
        fs = 0.0

        for i in range(numberOfDiscretizations):
            if self.DEBUG:
                print("currentStep = "+str(currentStep)+ "   FS = "+str(fs))
            fs = self.getFS(currentStep)
            numerator += currentStep * fs
            denominator += fs
            currentStep += stepSize
        
        if denominator == 0.0:
            return 0.0
        else:
            return numerator/denominator

    def getDefuzzifiedCOS(self) -> float:
        """Return center of this set"""
        return self.getPeak()
    
    def toString(self) -> str:
        return "T1 Membership function "+self.name
