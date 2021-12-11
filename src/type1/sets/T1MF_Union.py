
"""
T1MF_Union.py
Created 11/12/2021
"""

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype

class T1MF_Union(T1MF_Prototype):
    """
    Class T1MF_Union
    The union membership function between 2 sets

    Parameters: SetA and SetB both implementing the T1MF interface

    Functions:
        getFS
        getAlphaCut
        getPeak
        compareTo
    """

    def __init__(self, setA,setB) -> None:
        super().__init__("Union: "+setA.getName()+"_"+setB.getName())
        self.setA = setA
        self.setB = setB
        self.support = Tuple(min(setA.getSupport().getLeft(),setB.getSupport().getLeft()),
                             max(setA.getSupport().getRight(),setB.getSupport().getRight()))
        
    def getFS(self, x) -> float:
        """Return the maximum FS between two sets"""
        return max(self.setA.getFS(x),self.setB.getFS(x))
    
    def getAlphaCut(self, alpha) -> Tuple:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")
    
    def getPeak() -> float:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")
    
    def compareTo(o) -> int:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")