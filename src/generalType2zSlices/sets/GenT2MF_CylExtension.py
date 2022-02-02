"""
GenT2MF_CylExtension.py
Created 2/1/2022
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Cylinder import IntervalT2MF_Cylinder
from type1.sets.T1MF_Discretized import T1MF_Discretized
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from typing import List

class GenT2MF_CylExtension(GenT2MF_Prototype):
    """
    Class GenT2MF_CylExtension
    The cylinder extension Gen class

    Parameters: 
        baseSet: T1 interface
        zDiscLevel = The discretization Level

    Functions:
        clone

    """

    def __init__(self, baseSet,zDiscLevel) -> None:
        super().__init__("GenT2zCyl-ext-of-"+baseSet.getName())
        self.baseSet = baseSet
        self.zDiscretizationLevel = zDiscLevel
        self.zSpacing = 1.0/zDiscLevel
        self.DEBUG = False
        self.zSlices = [0] * zDiscLevel
        self.support = Tuple(float("-inf"),float("inf"))
        self.slices_zValues = [0] * zDiscLevel

        if self.DEBUG:
            print("Cylindric extension baseset:")
            print(baseSet.toString())
        
        for i in range(zDiscLevel):
            self.slices_zValues[i] = (i+1)*self.zSpacing
            self.zSlices[i] = IntervalT2MF_Cylinder("Cyl-ext-at-"+self.slices_zValues[i],baseSet.getAlphaCut(self.slices_zValues[i]))
        self.getNumberOfzLevels = self.zDiscretizationLevel
    
    def clone(self) -> GenT2MF_CylExtension:
        """Clone the class"""
        return GenT2MF_CylExtension(self.baseSet,self.zDiscretizationLevel)
