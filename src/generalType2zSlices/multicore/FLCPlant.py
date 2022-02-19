"""
FLCPlant.py
Created 19/2/2022
"""
import sys

sys.path.append("..")

from generic.Input import Input
from generic.Output import Output
from generic.Tuple import Tuple
from intervalType2.system.IT2_Rulebase import IT2_Rulebase
from typing import List, OrderedDict

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

    def __init__(self,rulebase,results,positionPointer,typeReductionType,lock) -> None:
        self.rulebase = rulebase
        self.results = results
        self.typeReductionType = typeReductionType
        self.positionPointer = positionPointer
        self.lock = lock
    
    def getTypeReductionType(self) -> int:
        return self.typeReductionType
    
    def setTypeReductionType(self,type) -> None:
        self.typeReductionType = type
    
    def run(self) -> None:
        out = self.rulebase.getOutputs()
        temp = self.rulebase.evaluateGetCentroid(self.typeReductionType)
        for o in out:
            self.lock.acquire()
            self.results[o][0][self.positionPointer] = temp[o][0]
            self.lock.release()