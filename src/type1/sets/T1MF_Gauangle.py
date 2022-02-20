
"""
T1MF_Gauangle.py
Created 18/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from typing import List
import math
from numpy import float64 as f
import functools

@functools.total_ordering
class T1MF_Gauangle(T1MF_Prototype):
    """
    Class T1MF_Gauangle
    Class for Gauangle Type-1 Fuzzy Membership Functions.
    The Gauangle MF combines the smooth "peak" of Gaussian MFs with the linearly
    decreasing "sides" of triangular MFs.

    Parameters: 
        name:Name of the set
        start:Start as for triangular MF.
        center:Center as for triangular MF
        end:End as for triangular MF.

    Functions:
        getFS
        getPeak
        getMean
        getStart
        getEnd
        toString
        getLineEquationParameters
        getXForYOnLine
        compareTo
        getAlphaCut
     
    """

    def __init__(self, name,start,center,end) -> None:
        super().__init__(name)
        self.start = start
        self.center = center
        self.end = end
        self.similarToGaussian = 0.5 

        self.spreadForLeft = (center-start)*(1.0-self.similarToGaussian)
        self.spreadForRight = (end-center)*(1.0-self.similarToGaussian)
        self.transitionPointLeft = center-((center-start)*self.similarToGaussian)
        self.transitionPointRight = center+((end-center)*self.similarToGaussian)
    
        if start == center:
            self.isLeftShoulder = True
            divLeft = float("nan")
            divRight = f(self.transitionPointRight-center)/self.spreadForRight
        elif center == end:
            self.isRightShoulder = True
            divRight = float("nan")
            divLeft = f(self.transitionPointLeft-center)/self.spreadForLeft
        else:
            divLeft = f(self.transitionPointLeft-center)/self.spreadForLeft
            divRight = f(self.transitionPointRight-center)/self.spreadForRight
        
        self.support = Tuple(start,end)

        ab = self.getLineEquationParameters(Tuple(start,0.0),
                Tuple(self.transitionPointLeft,
                math.exp(-0.5*math.pow(divLeft,2))))
        self.leftCalculationPoint = self.getXForYOnLine(1.0,ab)
        
        ab = self.getLineEquationParameters(Tuple(self.transitionPointRight,
                math.exp(-0.5*math.pow(divRight,2)))
                ,Tuple(end,0.0))
        self.rightCalculationPoint = self.getXForYOnLine(1.0,ab)

        if self.DEBUG:
            print("Transition points between triangular and gaussian functions are "
            +str(self.transitionPointLeft)+" and "+ str(self.transitionPointRight)+".")
        
    def getFS(self, x) -> float:
        """Return the maximum FS between two sets"""
        if self.support.contains(x):
            if (self.isLeftShoulder and x<=self.center) or (self.isRightShoulder and x>=self.center):
                return 1.0
            elif x<=self.transitionPointLeft:
                return f(x-self.start)/(self.leftCalculationPoint-self.start)
            elif x<=self.transitionPointRight:
                if x<=self.center:
                    return math.exp(-0.5*math.pow(f(x-self.center)/self.spreadForLeft,2))
                else:
                    return math.exp(-0.5*math.pow(f(x-self.center)/self.spreadForRight,2))
            else:
                return f(self.end-x)/(self.end-self.rightCalculationPoint)
        else:
            return 0.0
    
    def getPeak(self) -> float:
        """Return the peak of the set"""
        return self.getMean()
    
    def getMean(self) -> float:
        """Return the mean of the set"""
        return self.center
    
    def getStart(self) -> float:
        """Return the start of the set"""
        return self.start
    
    def getEnd(self) -> float:
        """Return the end of the set"""
        return self.end
    
    def toString(self) -> str:
        """Convert membership function to string"""
        s = self.name+"  interiorSet "+str(self.start)+"  "+str(self.center)+"  "+str(self.end)
        if self.isLeftShoulder():
            s += " (LeftShoulder)"
        if self.isRightShoulder():
            s += " (RightShoulder)"
        return s
    
    def getLineEquationParameters(self,x,y) -> List[float]:
        """returns the line equation parameters a and be (line equation = ax*b) for a line passing through the points defined by the tuples x and y.
        The first point (x), the Tuple consists of the x and y coordinates of the point in this order.
        The second point (y), the Tuple consists of the x and y coordinates of the point in this order."""
        ab = []
        ab.append(f(y.getRight()-x.getRight())/(y.getLeft()-x.getLeft()))
        ab.append(x.getRight()-ab[0]*x.getLeft())
        if self.DEBUG:
            print("x = "+str(x)+"   y = "+str(y))
            print("Line equation: "+str(ab[0])+" * x + "+str(ab[1]))
        return ab
    
    def getXForYOnLine(self,y,ab) -> float:
        """Returns the x coordinate for a specified y coordinate when considering the given line equation."""
        return f(y-ab[1])/ab[0]
    
    def compareTo(self, o) -> int:
        """Compare to another gauangle object """
        if not type(o) is T1MF_Gauangle:
            raise Exception("A T1MF_Gauangle object is expected for comparison with another T1MF_Triangular object.")
        
        if self.isLeftShoulder():
            if self.getEnd() == o.getEnd() and o.isLeftShoulder() and self.getPeak() == o.getPeak():
                return 0
            if self.getEnd() <= o.getEnd() and o.isLeftShoulder() and self.getPeak() <= o.getPeak():
                return -1
            return 1
        elif self.isRightShoulder():
            if self.getStart() == o.getStart() and o.isRightShoulder() and self.getPeak() == o.getPeak():
                return 0
            if self.getStart() <= o.getStart() and o.isRightShoulder() and self.getPeak() <= o.getPeak():
                return -1
            return 1
        else:
            if self.getEnd() == o.getEnd() and self.getStart() == o.getStart() and self.getPeak() == o.getPeak():
                return 0
            if self.getEnd() <= o.getEnd() and self.getStart() == o.getStart() and self.getPeak() <= o.getPeak():
                return -1
            return 1

    def __eq__(self, o):
        val = self.compareTo(o)
        if val == 0:
            return True
        else:
            return False

    def __lt__(self, o):
        val = self.compareTo(o)
        if val == -1:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.getName())
    
    def getAlphaCut(self, alpha) -> Tuple:
        """Unsupported Function"""
        raise Exception("Unsupported Function")


        





