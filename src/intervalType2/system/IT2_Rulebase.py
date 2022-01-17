"""
IT2_Rulebase.py
Created 16/1/2022
"""
import sys
from intervalType2.sets.IntervalT2MF_Intersection import IntervalT2MF_Intersection

from intervalType2.system.IT2_Rule import IT2_Rule
sys.path.append("..")
from collections import OrderedDict

import math
from generic.Tuple import Tuple
from generic.Input import Input
from type1.sets.T1MF_Interface import T1MF_Interface
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from intervalType2.system.IT2_COSInferenceData import IT2_COSInferenceData
from intervalType2.sets.IntervalT2MF_Cylinder import IntervalT2MF_Cylinder
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
                fir = [0.0] * len(leftData) 
                yDashDash = 0.0
                stopFlag = False
                R = 0
                L = 0

                for i in range(len(fir)):
                    fir[i] = rightData[i].getFStrength().getAverage()
                
                yr = self.weightedSigma(fir,rightData)
                yDash = yr

                while not stopFlag:
                    for i in range(len(fir)-1):
                        if rightData[i].getSelectedCentroidEndpoint()<=yDash and yDash <= rightData[i+1].getSelectedCentroidEndpoint():
                            R = i
                            break
                    
                    for i in range(R+1):
                        fir[i] = rightData[i].getFStrength.getLeft()
                    for i in range(R+1,len(fir)):
                        fir[i] = rightData[i].getFStrength.getRight()

                    if len(fir) == 1 and fir[0] == 0:
                        fir[0] = 0.00001
                    
                    yr = self.weightedSigma(fir,rightData)
                    yDashDash = yr

                    if abs(yDash-yDashDash)<0.000000001:
                        stopFlag = True
                        yDashDash = yr
                    else:
                        yDash = yDashDash
                
                stopFlag = False
                for i in range(len(fir)):
                    fir[i] = leftData[i].getFStrength.getAverage()
                
                yl = self.weightedSigma(fir,leftData)
                yDash = yl
                if self.DEBUG:
                    print("Initial yDash for left = "+str(yDash))
                
                while not stopFlag:
                    for i in range(len(fir)-1):
                        if leftData[i].getSelectedCentroidEndpoint()<=yDash and yDash <= leftData[i+1].getSelectedCentroidEndpoint():
                            L = i
                            break
                    
                    for i in range(L+1):
                        fir[i] = leftData[i].getFStrength.getRight()
                    for i in range(L+1,len(fir)):
                        fir[i] = leftData[i].getFStrength.getLeft()
                    
                    yl = self.weightedSigma(fir,leftData)

                    if math.isnan(yl):
                        yl = 0
                        break

                    yDashDash = yl

                    if self.DEBUG:
                        print("yDash = "+str(yDash)+" and yDashDash = "+yDashDash)
                    
                    if abs(yDash)-abs(yDashDash)<0.000000001:
                        stopFlag = True
                        yDashDash = yl
                    else:
                        yDash = yDashDash
            
                if self.DEBUG:
                    print("returning yl = "+str(yl)+" and yr = "+str(yr))
                returnValue.put(o,Tuple(yl,yr))
        return returnValue
    
    def getFiringIntervalsForCOS_TR(self):
        returnValue = OrderedDict()
        if self.DEBUG:
            print("Number of rules in rulebase: "+str(len(self.rules)))
    
        ruleCounter = 0
        for r in self.rules:
            ruleCons = r.getConsequents()
            firingStrength = r.getFStrength(self.implicationMethod)
            if firingStrength.getRight()>0.0:
                for cons in ruleCons:
                    if not cons.getOutput() in returnValue.keys():
                        returnValue.put(cons.getOutput(),[None,None])
                    returnValue[cons.getOutput()][0]=IT2_COSInferenceData(firingStrength,r.getConsequentCentroid(cons.getOutput()).getLeft())
                    returnValue[cons.getOutput()][1]=IT2_COSInferenceData(firingStrength,r.getConsequentCentroid(cons.getOutput()).getRight())
            ruleCounter += 1
        return returnValue
        
    def doReductionCentroid(self):
        overallOutputSet = OrderedDict()
        firstFiredForOutput = OrderedDict()
        for o in self.outputs:
            firstFiredForOutput[o]= True
        
        for r in self.rules:
            fStrength = r.getFStrength(self.implicationMethod)
            if fStrength.getRight()>0.0:
                for c in r.getConsequents():
                    o = c.getOutput()
                    if firstFiredForOutput[o]:
                        overallOutputSet[o] = IntervalT2MF_Intersection(IntervalT2MF_Cylinder("FiringInterval",fStrength),c.getMembershipFunction())




                    






                






    