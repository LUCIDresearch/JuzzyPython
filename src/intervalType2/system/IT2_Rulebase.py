"""
IT2_Rulebase.py
Created 16/1/2022
"""
import sys

from intervalType2.system.IT2_Rule import IT2_Rule
sys.path.append("..")
from collections import OrderedDict


from generic.Tuple import Tuple
from generic.Input import Input
from type1.sets.T1MF_Interface import T1MF_Interface
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from intervalType2.system.IT2_Consequent import IT2_Consequent
from type1.sets.T1MF_Singleton import T1MF_Singleton
from typing import List

class IT2_Rulebase():
    """
    Class 

    Parameters:
      
        
    Functions: 
        
    """

    def __init__(self,initialNumberOfRule = None) -> None:
        self.rules = []
        if initialNumberOfRule != None:
            self.outputs = [0]* initialNumberOfRule
        else:
            self.outputs = []
        self.DEBUG = False
        self.CENTEROFSETS = 0
        self.CENTROID = 1
        self.implicationMethod = 1
        self.PRODUCT = 0
        self.MINIMUM = 1
    
    def getInputs(self) -> List[Input]:
        return self.rules[0].getInputs()
    
    def getFuzzyLogicType(self) -> int:
        return 1

    def addRule(self,r) -> None:
        self.rules.append(r)
        it = r.getConsequents()
        for i in it:
            o = i.getOutput()
            if not o in self.outputs:
                self.outputs.append(o)
    
    def addRules(self,r) -> None:
        for i in range(len(r)):
            self.addRule(i)
    
    def getRules(self) -> List[IT2_Rule]:
        return self.rules
    
    def getNumberOfRules(self) -> int:
        return len(self.rules)
    
    def evaluateGetCentroid(self,typeReductionType) -> dict:
        returnValue = OrderedDict()
        
        if typeReductionType == self.CENTEROFSETS:
            typeReductionOutput = self.doCOSTypeReduction()
        elif typeReductionType == self.CENTROID:
            typeReductionOutput = self.doReductionCentroid()
        
        for o in self.outputs:
            if not o in typeReductionOutput.keys():
                returnValue[o] = {None,1.0}
            else:
                returnValue[o] = {typeReductionOutput[o],1.0}

        return returnValue

    def evaluate(self,typeReductionType) -> dict:
        returnValue = OrderedDict()

        if typeReductionType == self.CENTEROFSETS:
            typeReductionOutput = self.doCOSTypeReduction()
        elif typeReductionType == self.CENTROID:
            typeReductionOutput = self.doReductionCentroid()
        
        for o in self.outputs:
            if not o in typeReductionOutput.keys():
                returnValue[o] = 0.0
            else:
                returnValue[o] = typeReductionOutput[o].getAverage()

        return returnValue
    
    def doCOSTypeReduction(self) -> dict:
        returnValue = OrderedDict()
        data = self.getFiringIntervalsForCOS_TR()

        oIt = data.keys()
        oIt = sorted(oIt)
        
        if data == {} or len(data[oIt[0]][0]) == 0:
            for i in oIt:
                returnValue[i] == None
            return returnValue
        else:
            for o in oIt:
                currentOutputData = data[o]
                leftData = currentOutputData[0].copy()
                rightData = currentOutputData[1].copy()
                leftData = sorted(leftData)
                rightData = sorted(rightData)

                






    