
"""
T1MF_Gaussian.py
Created 17/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
import math

class T1MF_Gaussian(T1MF_Prototype):
    """
    Class T1MF_Gaussian
    The gaussian membership function for type 1 sets

    Parameters: 
        Name: Name of the function
        Mean: The mean
        Spread: standard deviation

    Functions:
        getFS
        getAlphaCut
        getPeak
        compareTo
        getSpread
        getMean
        toString
    """

    def __init__(self, name: str,mean: float,spread: float) -> None:
        super().__init__(name)
        self.mean = mean
        self.spread = spread
        #The support is defined as 4 x spread to the left and to the right of the mean.
        self.support = Tuple(mean-4*spread,mean+4*spread)
    
    def getFS(self, x: float) -> float:
        """Return the maximum FS between two sets"""
        if x >= self.getSupport().getLeft() and x <= self.getSupport().getRight():
            if self.isLeftShoulder() and x <= self.mean:
                return 1.0
            if self.isRightShoulder() and x >= self.mean:
                return 1.0
            return math.exp(-0.5*math.pow(((x-self.mean)/self.spread),2))
        else:
            return 0.0
    
    def getPeak(self) -> float:
        """Return the mean of the membership function"""
        return self.mean
    
    def getSpread(self) -> float:
        """Return the standard deviation"""
        return self.spread
    
    def getMean(self) -> float:
        """Return the mean of the membership function"""
        return self.mean
    
    def toString(self) -> float:
        """Convert membership function to string"""
        s = self.name() + " - Gaussian with mean "+str(self.mean)+", standard deviation: "+str(self.spread)
        if self.isLeftShoulder():
            s += " (LeftShoulder)"
        if self.isRightShoulder():
            s += " (RightShoulder)"
        return s
    
    def getAlphaCut(self, alpha: float) -> Tuple:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
    
    def compareTo(self,o: object) -> int:
        """Unsupported Function"""
        raise Exception("Unsupported Function")