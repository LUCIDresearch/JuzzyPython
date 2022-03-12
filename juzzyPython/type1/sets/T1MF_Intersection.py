
"""
T1MF_Intersection.py
Created 17/12/2021
"""

from juzzyPython.generic.Tuple import Tuple
from juzzyPython.type1.sets.T1MF_Prototype import T1MF_Prototype
from juzzyPython.type1.sets.T1MF_Interface import T1MF_Interface


class T1MF_Intersection(T1MF_Prototype):
    """
    Class T1MF_Intersection
    Creates an intersection between the two sets, A and B

    Parameters:
        setA: T1MF
        setB: T1MF

    Functions:
        getFS
        getAlphaCut
        getPeak
        compareTo
    """

    def __init__(self, name: str,setA: T1MF_Interface,setB: T1MF_Interface) -> None:
        super().__init__("Intersection: "+setA.getName()+"_"+setB.getName())
        self.support = Tuple(max(setA.getSupport().getLeft(),setB.getSupport().getLeft()),
                        min(setA.getSupport().getRight(),setB.getSupport().getRight()))
        self.setA = setA
        self.setB = setB
    
    def getFS(self, x: float) -> float:
        """Return the min FS from both sets"""
        return min(self.setA.getFS(x),self.setB.getFS(x))
    
    def getAlphaCut(self, alpha: float) -> Tuple:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
    
    def getPeak(self) -> float:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
    
    def compareTo(self, o: object) -> int:
        """Unsupported Function"""
        raise Exception("Unsupported Function")