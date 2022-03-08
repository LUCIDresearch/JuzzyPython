
"""
T1MF_Interface.py
Created 10/12/2021
"""
from juzzyPython.generic.MF_Interface import MF_Interface
from juzzyPython.generic.Tuple import Tuple

class T1MF_Interface(MF_Interface):
    """
    Class T1MF_Interface
    An interface for type 1 membership functions

    Parameters: None

    Functions:
        getFS
        getAlphaCut
        getPeak
        getName
        setName
        getSupport
        setSupport
        setLeftShoulder
        setRightShoulder
        isLeftShoulder
        isRightShoulder
        getDefuzzifiedCentroid
        getDefuzzifiedCOS
    """

    def getFS(self,x: float) -> float:
        pass
    
    def getAlphaCut(self,alpha: float) -> Tuple:
        pass

    def getPeak(self) -> float:
        pass    

    def getName(self) -> str:
        pass

    def setName(self, name: str) -> None:
        pass

    def getSupport(self) -> Tuple:
        pass

    def setSupport(self, support: Tuple) -> None:
        pass

    def setLeftShoulder(self, value: bool) -> None:
        pass

    def setRightShoulder(self, value: bool) -> None:
        pass    

    def isLeftShoulder(self) -> bool:
        pass

    def isRightShoulder(self) -> bool:
        pass

    def getDefuzzifiedCentroid(self, numberOfDiscretizations: int) -> float:
        pass

    def getDefuzzifiedCOS(self) -> float:
        pass

    def toString(self) -> str:
        pass
    
    def compareTo(self,o: object) -> int:
        pass


