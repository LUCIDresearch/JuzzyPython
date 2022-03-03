"""
FLCFactory.py
Created 19/2/2022
"""
import sys
sys.path.append("..")
from generalType2zSlices.multicore.FLCPlant import FLCPlant
from generic.Input import Input
from generic.Output import Output
from generic.Tuple import Tuple
from intervalType2.system.IT2_Rulebase import IT2_Rulebase
from typing import List, OrderedDict
import multiprocessing

class FLCFactory():
    """
    Class FLCFactory

    Parameters:
      
    Functions:

    """ 

    def __init__(self,rulebases: List[IT2_Rulebase]) -> None:
        self.manager - multiprocessing.Manager()
        self.rulebases = rulebases
        self.weight = 0.0
        self.defaultTypeReduction = 1
        self.numberOfThreads = len(rulebases)
        self.pool = multiprocessing.Pool(self.numberOfThreads)
        self.plants = [None] * self.numberOfThreads
        self.zLevels = [0.0] * self.numberOfThreads

        for i in range(self.numberOfThreads):
            self.zLevels[i] = (i+1.0) / self.numberOfThreads
            self.weight += self.zLevels[i]
        
        self.rawResults = self.manager.dict()
        out = self.rulebases[0].getOutputs()
        for o in out:
            self.rawResults[o] = [ [0]*self.numberOfThreads for i in range(2)]
        for i in self.numberOfThreads:
            self.plants[i] = FLCPlant(self.rulebases[i],self.rawResults,i,self.defaultTypeReduction)
    
    def runFactory(self, typeReductionType: int) -> dict:
        returnValue = OrderedDict()
        out = self.rulebases[0].getOutputs()
        for o in out:
            objs = self.rawResults[o]
            objs[0] = [0] * self.numberOfThreads
            objs[1] = [0] * self.numberOfThreads
        
        if not typeReductionType == self.defaultTypeReduction:
            for p in self.plants:
                p.setTypeReductionType(typeReductionType)
            self.defaultTypeReduction = typeReductionType
        
        for i in range(self.numberOfThreads):
            self.pool.apply(self.plants[i].run())

        out = self.rulebases[0].getOutputs()
        for o in out:
            returnValue[o] = 0.0
        
        for i in range(self.numberOfThreads):
            out = self.rulebases[0].getOutputs()
            for o in out:
                if self.rawResults[o][0][i] != None:
                    returnValue[o] = returnValue.get(o) + self.rawResults[o][0][i].getAverage()*self.zLevels[i]
        
        out = self.rulebases[0].getOutputs()
        for o in out:
            returnValue[o] = returnValue[o] / self.weight

        return returnValue

