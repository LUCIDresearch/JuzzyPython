
"""
T1MF_Intersection.py
Created 17/12/2021
"""

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from typing import List

class T1MF_Intersection(T1MF_Prototype):
    """
    Class T1MF_Intersection
    Creates an intersection between the two sets, A and B

    Parameters: Membership functions setA and setB that you want to intersect

    Functions:
        getFS
        getAlphaCut
        getPeak
        compareTo
    """

    def __init__(self, name,setA,setB) -> None:
        super().__init__("Intersection: "+setA.getName()+"_"+setB.getName())
        self.support = Tuple(max(setA.getSupport().getLeft(),setB.getSupport().getLeft()),
                        min(setA.getSupport().getRight(),setB.getSupport().getRight()))
        self.setA = setA
        self.setB = setB
    
    def getFS(self, x) -> float:
        """Return the min FS from both sets"""
        return min(self.setA.getFS(x),self.setB.getFS(x))
    
    def getAlphaCut(self, alpha) -> Tuple:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
    
    def getPeak(self) -> float:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
    
    def compareTo(self, o) -> int:
        """Unsupported Function"""
        raise Exception("Unsupported Function")