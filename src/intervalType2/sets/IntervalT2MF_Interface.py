"""
IntervalT2MF_Interface.py
Created 5/1/2022
"""
import sys
sys.path.append("..")

from generic.MF_Interface import MF_Interface
from generic.Tuple import Tuple
from type1.sets.T1MF_Interface import T1MF_Interface

class IntervalT2MF_Interface(MF_Interface):
    """
    Class IntervalT2MF_Interface

    Parameters: None

    Functions:
        getFS
        getPeak
        getName
        setName
        getSupport
        setSupport
        setLeftShoulder
        setRightShoulder
        isLeftShoulder
        isRightShoulder
        toString
        compareTo
        getLowerBound
        getUpperBound
        getCentroid
        getUMF
        getLMF
        getFSAverage
       
    """

    def getFS(self,x) -> float:
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

    def toString(self) -> str:
        pass
    
    def compareTo(self,o) -> int:
        pass

    def getUpperBound(self,x) -> float:
        pass
    
    def getLowerBound(self,x) -> float:
        pass
    
    def getUMF(self) -> T1MF_Interface:
        pass
    
    def getLMF(self) -> T1MF_Interface:
        pass

    def getFSAverage(self,x) -> float:
        pass
    
    def getCentroid(primaryDiscretisationLevel) -> Tuple:
        pass