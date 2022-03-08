
"""
T1MF_Union.py
Created 11/12/2021
"""
from juzzyPython.type1.sets.T1MF_Interface import T1MF_Interface
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.type1.sets.T1MF_Prototype import T1MF_Prototype

class T1MF_Union(T1MF_Prototype):
    """
    Class T1MF_Union
    The union membership function between 2 sets

    Parameters: 
        SetA: T1MF
        SetB: T1MF

    Functions:
        getFS
        getAlphaCut
        getPeak
        compareTo
    """

    def __init__(self, setA: T1MF_Interface ,setB: T1MF_Interface) -> None:
        super().__init__("Union: "+setA.getName()+"_"+setB.getName())
        self.setA = setA
        self.setB = setB
        self.support = Tuple(min(setA.getSupport().getLeft(),setB.getSupport().getLeft()),
                             max(setA.getSupport().getRight(),setB.getSupport().getRight()))
        
    def getFS(self, x: float) -> float:
        """Return the maximum FS between two sets"""
        return max(self.setA.getFS(x),self.setB.getFS(x))
    
    def getAlphaCut(self, alpha: float) -> Tuple:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")
    
    def getPeak(self) -> float:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")
    
    def compareTo(self,o: object) -> int:
        """Currently Unsupported"""
        raise Exception("Unsupported Function")