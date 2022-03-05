"""
FLCPlant.py
Created 19/2/2022
"""
import sys

sys.path.append("..")

from intervalType2.system.IT2_Rulebase import IT2_Rulebase
from typing import List, OrderedDict
import multiprocessing
import os
class FLCPlant():
    """
    Class FLCPlant
    Runs a single IT2 Rulebase

    Parameters:
        rulebase: Single IT2 rulebase
        results: Results dict
        positionPointer: Int
        typeReductionType: Int
        lock: Multiprocessing lock
      
    Functions:
        getTypeReductionType
        setTypeReductionType
        run
    """ 

    def __init__(self,rulebase: IT2_Rulebase,positionPointer: int,typeReductionType: int,lock) -> None:
        self.rulebase = rulebase
        self.typeReductionType = typeReductionType
        self.positionPointer = positionPointer
        self.lock = lock
    
    def getTypeReductionType(self) -> int:
        return self.typeReductionType
    
    def setTypeReductionType(self,type: int) -> None:
        self.typeReductionType = type
    
    def run(self,results: dict) -> None:
        out = self.rulebase.getOutputs()
        temp = self.rulebase.evaluateGetCentroid(self.typeReductionType)
        for o in out:
            change = results[o]
            new = temp[o][0]
            change[0][self.positionPointer]= new 
            results[o] = change

