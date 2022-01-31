"""
GenT2MF_Prototype.py
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

    def isLeftShoulder(self) -> bool:
        pass

    def isRightShoulder(self) -> bool:
        pass

    def toString(self) -> str:
        pass
    
    def getFSWeightedAverage(self,x) -> float:
        pass
    
    def getCentroid(self,primaryDiscretisationLevel) -> Tuple:
        pass
    
    def getZValues(self) -> List[float]:
        pass
    
    def getZValue(self,slice_number) -> float:
        pass

    def setZSlice(self,zSlice,zLevel) -> None:
        pass

    def getZSlice(self,slice_number) -> IntervalT2MF_Interface:
        pass

    def getNumberOfSlices(self) -> int:
        pass

    