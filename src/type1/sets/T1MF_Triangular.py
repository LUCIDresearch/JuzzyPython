"""
T1MF_Triangular.py
Created 17/12/2021
"""
import sys
sys.path.append("..")
import math
from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
import type1.sets.T1MF_Singleton 
import functools

@functools.total_ordering
class T1MF_Triangular(T1MF_Prototype):
    """
    Class T1MF_Triangular
    The triangular membership function for type 1 fuzzy sets

    Parameters: 
        name: The name of the membership function
        peak: the current peak
        start: Start of triangle
        end: End of the triangle

    Functions:
        getFS
        getStart
        getPeak
        getEnd
        toString
        compareTo
        getAlphaCut
        findLinearEquationParameters
        
    """

    def __init__(self, name: str,start: float,peak: float,end: float) -> None:
        super().__init__(name)
        #left and right "leg" slope
        self.lS = float("nan")
        self.rS = float("nan")
        #left and right "leg" intercept   
        self.lI = float("nan")
        self.rI = float("nan")
        self.start = start
        self.peak = peak
        self.end = end
        self.support = Tuple(start,end)

    def getFS(self, x: float) -> float:
        """Return the maximum FS between two sets"""
        if (self.isLeftShoulder and x <= self.peak) or (self.isRightShoulder and x >= self.peak):
            return 1.0
        
        if x<self.peak and x>self.start:
            out = (x-self.start)/(self.peak-self.start)
        elif x == self.peak:
            out = 1.0
        elif x>self.peak and x<self.end:
            out = (self.end-x)/(self.end-self.peak)
        else:
            out = 0.0
        
        return out
    
    def getStart(self) -> float:
        """Get the start value of the function"""
        return self.start
    
    def getPeak(self) -> float:
        """Get the peak value of the function"""
        return self.peak
    
    def getEnd(self) -> float:
        """Get the end value of the function"""
        return self.end

    def toString(self) -> str:
        """Convert membership function to string"""
        s = self.name+"  -  "+str(self.start)+"  "+str(self.peak)+"  "+str(self.end)
        if self.isLeftShoulder():
            s += " (LeftShoulder)"
        if self.isRightShoulder():
            s += " (RightShoulder)"
        return s

    def compareTo(self, o: object) -> int:
        """Compare the function against triangular or singleton functions"""
        if type(o) is T1MF_Triangular:
            if self.getEnd() == o.getEnd() and self.getStart() == o.getStart() and self.getPeak() == o.getPeak():
                return 0
            if self.getEnd() <= o.getEnd() and self.getStart() <= o.getStart() and self.getPeak() <= o.getPeak():
                return -1
            return 1
        elif type(o) is type1.sets.T1MF_Singleton.T1MF_Singleton:
            if self.getPeak() < o.getValue():
                return -1
            return 1
        else:
            return None

    def __eq__(self, o: object):
        val = self.compareTo(o)
        if val == 0:
            return True
        else:
            return False

    def __lt__(self, o: object):
        val = self.compareTo(o)
        if val == -1:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.getName())

    def getAlphaCut(self, alpha: float) -> Tuple:
        """Get the alpha cut as a tuple with input float"""
        self.findLinearEquationParameters()
        return Tuple((alpha-self.lI)/self.lS,(alpha-self.rI)/self.rS)
    
    def findLinearEquationParameters(self) -> None:
        """Finds the slopes and intercepts for the left and right "leg" of the membership function.
        If the parameters for the given set have previously been computed, the method returns directly."""
        if not math.isnan(self.lS):
            return
  
        self.lS = 1.0 / (self.peak-self.start)
        self.lI = 0 - self.lS * self.start
        

        self.rS = -1.0 / (self.end-self.peak)
        self.rI = 0 - self.rS * self.end 
    