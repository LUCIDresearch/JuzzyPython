
"""
T1MF_Cylinder.py
Created 10/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype

class T1MF_Cylinder(T1MF_Prototype):
    """
    Class T1MF_Cylinder
    The T1MF_Cylinder class is mainly a support class for the IT2 class. It serves
    to implement the cylindrical extension of a firing strength. In terms of a 
    type-1 MF, a cylinder is in fact just a singleton over the whole universe of 
    discourse.

    Parameters: Name: Name of the variable
    Membership Degree: The value for the membership degree of the "cylinder" (for all x)

    Functions:
        getFS
        getAlphaCut
        toString
        compareTo
        getPeak
    """

    def __init__(self, name: str,membershipDegree: float) -> None:
        super().__init__(name)
        if membershipDegree < 0.0 or membershipDegree > 1.0:
            raise Exception("The membership degree should be between 0 and 1.")
        self.membershipDegree = membershipDegree
        self.support = Tuple(float('-inf'),float('inf'))
    
    def getFS(self, x: float) -> float:
        """Return the membership degree"""
        return self.membershipDegree
    
    def getAlphaCut(self, alpha: float) -> Tuple:
        """Transform into basic belief assignment"""
        if alpha <= self.membershipDegree:
            return Tuple(float('-inf'),float('inf'))
        else:
            return None
    
    def toString(self) -> str:
        """Return function to string"""
        return self.name + " - Cylindrical extension at :" + str(self.membershipDegree)
    
    def compareTo(self,o:object) -> int:
        """Unsupported method"""
        raise Exception("Unsupported Method")
    
    def getPeak(self) -> float:
        """Unsupported method"""
        raise Exception("Unsupported Method")
