"""
IntervalT2MF_Trapezoidal.py
Created 8/1/2022
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
class IntervalT2MF_Trapezoidal(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Trapezoidal
    Class for Trapezoidal Interval Type-2 Fuzzy Sets

    Parameters: 
        upper: Upper membership function
        lower: Lower membership function

    Functions:
        toString
    """
    
    def __init__(self, name: str, upper: T1MF_Trapezoidal, lower: T1MF_Trapezoidal) -> None:
        super().__init__(name)
        if upper.getA()>lower.getA() or upper.getB()>lower.getB() or upper.getC()<lower.getC() or upper.getD()<lower.getD():
            raise Exception("The upper membership function needs to be higher than the lower membership function.")
        
        self.lMF = lower
        self.uMF = upper
        if self.DEBUG:
            print("Setting the support for the interval type-2 trapezoidal set: " + name)
        self.support = upper.getSupport()
    
    def toString(self) -> str:
        """Return the function as a string"""
        return "IntervalT2MF_Trapezoidal: "+self.getName()+ ",\nlower MF: "+str(self.lMF)+"\nupper MF: "+str(self.uMF)
