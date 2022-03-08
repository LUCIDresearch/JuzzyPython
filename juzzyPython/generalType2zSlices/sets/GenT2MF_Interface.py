"""
GenT2MF_Interface.py
Created 31/1/2022
"""
import sys
sys.path.append("..")

from generic.MF_Interface import MF_Interface
from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from type1.sets.T1MF_Discretized import T1MF_Discretized
from typing import List

class GenT2MF_Interface(MF_Interface):
    """
    Class GenT2MF_Interface

    Parameters: None

    Functions:
        getName
        setName
        getNumberOfSlices
        getFS
        getZSlice
        setZSlice
        getZValue
        getSupport
        setSupport
        getFSWeightedAverage
        isLeftShoulder
        isRightShoulder
        getZValues
        getCentroid
        getPeak
        toString
  
       
    """

    def getFS(self,x: float) -> float:
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

    def isLeftShoulder(self) -> bool:
        pass

    def isRightShoulder(self) -> bool:
        pass

    def toString(self) -> str:
        pass
    
    def getFSWeightedAverage(self,x: float) -> float:
        pass
    
    def getCentroid(self,primaryDiscretisationLevel: int) -> Tuple:
        pass
    
    def getZValues(self) -> List[float]:
        pass
    
    def getZValue(self,slice_number: int) -> float:
        pass

    def setZSlice(self,zSlice: IntervalT2MF_Interface,zLevel: int) -> None:
        pass

    def getZSlice(self,slice_number: int) -> IntervalT2MF_Interface:
        pass

    def getNumberOfSlices(self) -> int:
        pass

    