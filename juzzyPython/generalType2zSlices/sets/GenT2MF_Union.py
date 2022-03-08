"""
GenT2MF_Union.py
Created 2/1/2022
"""
from __future__ import annotations

import sys
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from type1.sets.T1MF_Discretized import T1MF_Discretized
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from typing import List

class GenT2MF_Union(GenT2MF_Prototype):
    """
    Class GenT2MF_Union
    A union instance of the General Type 2 Membership functions

    Parameters: 
        name : Name of function
        numberOfZLevels : Int of z levels
        slices_zValues : Array of slices values
        zSlices: array of slices

    Functions:
        clone
        getFS
       
    """

    def __init__(self, name: str,numberOfzLevels: int,slices_zValues: List[float],zSlices: List[IntervalT2MF_Interface]) -> None:
        super().__init__(name)
        self.numberOfzLevels = numberOfzLevels
        self.slices_zValues = slices_zValues.copy()
        self.zSlices = zSlices
        self.support = Tuple(zSlices[0].getSupport().getLeft(),zSlices[0].getSupport().getRight())
    
    def clone(self) -> GenT2MF_Union:
        """Clone the class"""
        return GenT2MF_Union(self.name,self.numberOfzLevels,self.slices_zValues,self.zSlices)
    
    def getFS(self, x: float) -> T1MF_Discretized:
        """Return the firing strength"""
        slice_ = T1MF_Discretized("VSlice")

        for i in range(len(self.zSlices)):
            temp = self.getZSlice(i).getFS(x)
            if temp.getRight()==0:
                if i==0:
                    slice_ = None
                break
            else:
                slice_.addPoint(Tuple(self.getZValue(i),temp.getLeft()))
                slice_.addPoint(Tuple(self.getZValue(i),temp.getRight()))
        return slice_
    
    def isLeftShoulder(self) -> bool:
        """Not implemented"""
        print("Shoulder methods not implemented")
        return False
    
    def isRightShoulder(self) -> bool:
        """Not implemented"""
        print("Shoulder methods not implemented")
        return False
    
    def getLeftShoulderStart(self) -> float:
        """Not implemented"""
        print("Shoulder methods not implemented")
        return float("nan")
    
    def getRightShoulderStart(self) -> float:
        """Not implemented"""
        print("Shoulder methods not implemented")
        return float("nan")




