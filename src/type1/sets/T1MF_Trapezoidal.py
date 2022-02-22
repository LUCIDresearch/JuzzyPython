
"""
T1MF_Trapezoidal.py
Created 17/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from typing import List

class T1MF_Trapezoidal(T1MF_Prototype):
    """
    Class T1MF_Trapezoidal
    Class for Trapezoidal Type-1 Fuzzy Membership Functions.
    The parameters of the MF are defined from left to right as a,b,c and d.
    The MF supports both normal MFs where the membership between b and c is 1.0,
    as well as non-normal MFs where this membership can be specified freely.

    Parameters: 
        parameters = Parameters list from left to right
        yLevels= The specific yLevels for the second and third point of the trapezoid. Normally, both values are equal.

    Functions:
        getFS
        getA
        getB
        getC
        getD
        getParameters
        getPeak
        setPeak
        getyLevels
        setyLevels
        compareTo
        getAlphaCut
        findLinearEquationParameters
        toString
        
    """

    def __init__(self, name: str,parameters: List[float], yLevels: List[float] = None) -> None:
        super().__init__(name)
        #left and right "leg" slope
        self.lS = None
        self.rS = None
        #left and right "leg" intercept   
        self.lI = None
        self.rI = None
        self.peak = None #peak is generally defined as the avg of b and c
        self.yLevels = [1.0,1.0]
        self.a = parameters[0]
        self.b = parameters[1]
        self.c = parameters[2]
        self.d = parameters[3]
        self.support = Tuple(self.a,self.d)
        if yLevels != None:
            self.yLevels = [yLevels[0],yLevels[1]]
        
    def getFS(self, x: float) -> float:
        """Return the maximum FS between two sets"""
        if (self.isLeftShoulder and x <= self.c) or (self.isRightShoulder and x >= self.b):
            return 1.0
        
        if x<self.b and x>self.a:
            out = self.yLevels[0] * (x-self.a)/(self.b-self.a)
        elif x>=self.b and x<=self.c:
            if self.yLevels[0] == self.yLevels[1]:
                out = self.yLevels[0]
            elif self.yLevels[0] < self.yLevels[1]:     
                out = (self.yLevels[1]*x-self.yLevels[0]*x-self.yLevels[1]*self.b+self.yLevels[0]*self.b)/(self.c-self.b)+self.yLevels[0]
            else:
                out = (self.yLevels[1]*x-self.yLevels[0]*x-self.yLevels[1]*self.b+self.yLevels[0]*self.b)/(self.c-self.b)+self.yLevels[0]
            if out<0:
                out = 0
        elif x>self.c and x<self.d:
            out = self.yLevels[1]*(self.d-x)/(self.d-self.c)
        else:
            out = 0.0

        if abs(1-out)<0.000001:
            out = 1.0
        if abs(out)<0.000001:
            out = 0.0
        
        return out
    
    def getA(self) -> float:
        """Return the a parameter of the function"""
        return self.a

    def getB(self) -> float:
        """Return the b parameter of the function"""
        return self.b
        
    def getC(self) -> float:
        """Return the c parameter of the function"""
        return self.c

    def getD(self) -> float:
        """Return the c parameter of the function"""
        return self.d
    
    def getParameters(self) -> List[float]:
        """Returns the MFs parameters
        Return a list of type float, holding all 4 parameters in order from
        left to right."""
        return [self.a,self.b,self.c,self.d]
    
    def getPeak(self) -> float:
        """As standard, the peak is generally defined as the average of b and c,
        however it may be changed using the setPeak() method if desired.
        Return The peak of either as average of b and c or as specified."""
        if self.peak == None:
            self.peak = (self.b+self.c)/2.0
        return self.peak
    
    def setPeak(self,peak: float) -> None:
        """Set the peak"""
        self.peak = peak
    
    def getyLevels(self) -> List[float]:
        """ Retrieves the yLevels of the second and third parameters (points B and C)
        This is useful for non-normal MFs.
        returns The degrees of membership of the inner parameters of the MF."""
        return self.yLevels
    
    def setyLevels(self,levels: List[float]) -> None:
        """Set the y levels """
        self.yLevels = levels
    
    def compareTo(self,o: object) -> int:
        """Compare to another trapezoidal object"""
        if not type(o) is T1MF_Trapezoidal:
            return None
        
        if (self.getA() == o.getA()) and (self.getB() == o.getB()) and (self.getC() == o.getC()) and (self.getD() == o.getD()):
            return 0
        if (self.getA() <= o.getA()) and (self.getB() <= o.getB()) and (self.getC() <= o.getC()) and (self.getD() <= o.getD()):
            return -1
        return 1

    def getAlphaCut(self, alpha: float) -> Tuple:
        """Get the alpha cut as a tuple"""
        self.findLinearEquationParameters()
        return Tuple((alpha-self.lI)/self.lS,(alpha-self.rI)/self.rS)
    
    def findLinearEquationParameters(self) -> None:
        """Finds the slopes and intercepts for the left and right "leg" of the membership function.
        If the parameters for the given set have previously been computed, the method returns directly."""
        if not self.lS == None:
            return
  
        self.lS = 1.0 / (self.b-self.a)
        self.lI = 0 - self.lS * self.a
        

        self.rS = -1.0 / (self.d-self.c)
        self.rI = 0 - self.rS * self.d
    
    def toString(self) -> str:
        """Convert membership function to string"""
        s = "T1MF_Trapezoidal:  "+ self.name() +"  -  "+str(self.a)+"  "+str(self.b)+" (y="+str(self.yLevels[0])+")  "+str(self.c)+" (y="+str(self.yLevels[1])+")  "+str(self.d)
        if self.isLeftShoulder():
            s += " (LeftShoulder)"
        if self.isRightShoulder():
            s += " (RightShoulder)"
        return s

