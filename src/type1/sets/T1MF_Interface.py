
"""
T1MF_Interface.py
Created 10/12/2021
"""
import sys
sys.path.append("..")

from generic.MF_Interface import MF_Interface
from generic.Tuple import Tuple

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

    def getFS(self,x) -> float:
        pass
    
    def getAlphaCut(self,alpha) -> Tuple:
        pass

    def getPeak(self) -> float:
        pass    

    def getName(self) -> str:
        pass

    def setName(self, name) -> None:
        pass

    def getSupport(self) -> Tuple:
        pass

    def setSupport(self, support) -> None:
        pass

    def setLeftShoulder(self, value) -> None:
        pass

    def setRightShoulder(self, value) -> None:
        pass    

    def isLeftShoulder(self) -> bool:
        pass

    def isRightShoulder(self) -> bool:
        pass

    def getDefuzzifiedCentroid(self, numberOfDiscretizations) -> float:
        pass

    def getDefuzzifiedCOS(self) -> float:
        pass

    def toString(self) -> str:
        pass
    
    def compareTo(self,o) -> int:
        pass


