"""
GenT2MF_Intersection.py
Created 3/1/2022
"""
from __future__ import annotations
from typing import List
import sys

from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
sys.path.append("..")
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype

class GenT2MF_Intersection(GenT2MF_Prototype):
    """
    Class GenT2MF_Intersections
    General Type 2 Intersection class

    Parameters: 
        name
        numberOfzLevels
        slices_zValues
        zSlices

    Functions:
        clone
 
    """

    def __init__(self, name: str,numberOfzLevels: int,slices_zValues: List[float],zSlices: List[IntervalT2MF_Interface]) -> None:
        super().__init__(name)
        self.getNumberOfzLevels = numberOfzLevels
        self.slices_zValues = slices_zValues
        self.zSlices = zSlices
        self.support = zSlices[0].getSupport().clone()

        if self.DEBUG:
            print("GenT2zMF_Intersection:")
            for i in range(8):
                print("For x = "+str(i*10)+" :  "+str(zSlices[0].getFS(i*10)))
    
    def clone(self) -> GenT2MF_Intersection:
        """Clone the class"""
        return GenT2MF_Intersection(self.name,self.getNumberOfzLevels,self.slices_zValues,self.zSlices)