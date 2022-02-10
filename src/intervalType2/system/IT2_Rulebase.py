"""
IT2_Rulebase.py
Created 16/1/2022
"""
import sys
from turtle import right
from intervalType2.sets.IntervalT2Engine_Centroid import IntervalT2Engine_Centroid
from intervalType2.sets.IntervalT2MF_Intersection import IntervalT2MF_Intersection

from intervalType2.system.IT2_Rule import IT2_Rule
sys.path.append("..")
from collections import OrderedDict

import math
from generic.Tuple import Tuple
from generic.Input import Input
from intervalType2.system.IT2_COSInferenceData import IT2_COSInferenceData
from intervalType2.sets.IntervalT2MF_Cylinder import IntervalT2MF_Cylinder
from intervalType2.sets.IntervalT2MF_Union import IntervalT2MF_Union
from typing import List

class IT2_Rulebase():
    """
    Class IT2_Rulebase
    Keeps track of rules and generates results

    Parameters:
        initialNumberOfRules = Starting rules for the logic set
      
    Functions: 
        getInputs
        getFuzzyLogicType
        addRule
        addRules
        getRules
        getNumberOfRules
        getOutputIterator
        evaluateGetCentroid
        evaluate
        doCOSTypeReduction
        getFiringIntervalsForCOS_TR
        doReductionCentroid
        weightedSigma
        removeRule
        setImplicationMethod
        getImplicationMethod
        toString
        
    """

    def __init__(self) -> None:
        self.rules = []
        self.outputs = []
        self.DEBUG = False
        self.CENTEROFSETS = 0
        self.CENTROID = 1
        self.implicationMethod = 1
        self.PRODUCT = 0
        self.MINIMUM = 1
    
    def getInputs(self) -> List[Input]:
        """This method assumes all rules use the same (and all) inputs. The first rule is queried to identify the inputs and return them.
        return An array of the inputs used in the rulebase (retrieved from the actecedents of the firts rule in the rulebase!)"""
        return self.rules[0].getInputs()
    
    def getFuzzyLogicType(self) -> int:
        """Returns the type of fuzzy logic that is employed.
        return 0: type-1, 1: interval type-2, 2: zSlices based general type-2"""
        return 1

    def addRule(self,r) -> None:
        """Add a new rule to the rule set"""
        self.rules.append(r)
        it = r.getConsequents()
        for i in it:
            o = i.getOutput()
            if not o in self.outputs:
                self.outputs.append(o)
    
    def addRules(self,r) -> None:
        """Add multiple new rules to the rule set"""
        for i in range(len(r)):
            self.addRule(i)
    
    def getRules(self) -> List[IT2_Rule]:
        """Return all the rules in the set"""
        return self.rules
    
    def getNumberOfRules(self) -> int:
        """Get the number of rules in the set"""
        return len(self.rules)
    
    def evaluateGetCentroid(self,typeReductionType) -> dict:
        """Returns the output of the FLS after type-reduction, i.e. the centroid.
        return A TreeMap where Output is used as key and the value is an Object[]
        where Object[0] is a Tuple (the centroid) and Object[1] is a Double holding
        the associated yValue for the centroid. If not rule fired for the given input(s),
        then null is returned as an Object[]."""
        returnValue = OrderedDict()
        
        if typeReductionType == self.CENTEROFSETS:
            typeReductionOutput = self.doCOSTypeReduction()
        elif typeReductionType == self.CENTROID:
            typeReductionOutput = self.doReductionCentroid()
        
        for o in self.outputs:
            if not o in typeReductionOutput.keys():
                returnValue[o] = [None,1.0]
            else:
                returnValue[o] = [typeReductionOutput[o],1.0]

        return returnValue

    def evaluate(self,typeReductionType) -> dict:
        """Returns typereduced & defuzzified result of evaluating all rules in the rulebase.
        typeReductionType: The type of type reducer to be used: 0-Center-Of-Sets, 
        1-Centroid.
        discretizationLevel: The discretization level to be employed (only applies to centroid type reducer)
        return The type-reduced and defuzzified output."""
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
        """Reduce based on center of sets reduction type"""
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
                        fir[i] = rightData[i].getFStrength().getLeft()
                    for i in range(R+1,len(fir)):
                        fir[i] = rightData[i].getFStrength().getRight()

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
                    fir[i] = leftData[i].getFStrength().getAverage()
                
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
                        fir[i] = leftData[i].getFStrength().getRight()
                    for i in range(L+1,len(fir)):
                        fir[i] = leftData[i].getFStrength().getLeft()
                    
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
                returnValue[o]=Tuple(yl,yr)
        return returnValue
    
    def getFiringIntervalsForCOS_TR(self) -> dict:
        """Get the firing intervals for cos type reduction"""
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
                        returnValue[cons.getOutput()]=[],[]
                    returnValue[cons.getOutput()][0].append(IT2_COSInferenceData(firingStrength,r.getConsequentCentroid(cons.getOutput()).getLeft()))
                    returnValue[cons.getOutput()][1].append(IT2_COSInferenceData(firingStrength,r.getConsequentCentroid(cons.getOutput()).getRight()))
            ruleCounter += 1
        return returnValue
        
    def doReductionCentroid(self) -> dict:
        """Do reduction based on the centroid type"""
        overallOutputSet = OrderedDict()
        firstFiredForOutput = OrderedDict()
        for o in self.outputs:
            firstFiredForOutput[o]= True
        
        for r in self.rules:
            fStrength = r.getFStrength(self.implicationMethod)
            #print(fStrength.toString())
            if fStrength.getRight()>0.0:
                for c in r.getConsequents():
                    o = c.getOutput()
                    if firstFiredForOutput[o]:
                        overallOutputSet[o] = IntervalT2MF_Intersection(IntervalT2MF_Cylinder("FiringInterval",fStrength),c.getMembershipFunction())
                        if not overallOutputSet[o].intersectionExists():
                            print("PUTTING NONE")
                            overallOutputSet[o] = None
                        firstFiredForOutput[o] = False
                    else:
                        if overallOutputSet[o] == None:
                            overallOutputSet[o] = IntervalT2MF_Intersection(IntervalT2MF_Cylinder("FiringInterval",fStrength),c.getMembershipFunction())
                            if not overallOutputSet[o].intersectionExists():
                                print("PUTTING NONE")
                                overallOutputSet[o] = None
                        else:
                            overallOutputSet[o] = IntervalT2MF_Union(IntervalT2MF_Intersection(
                            IntervalT2MF_Cylinder("FiringInterval",fStrength),
                            c.getMembershipFunction()),overallOutputSet[o])
            else:
                #print(r.toString())
                pass
    
        iT2EC = IntervalT2Engine_Centroid()
        returnValue = OrderedDict()
        for o in self.outputs:
            iT2EC.setPrimaryDiscretizationLevel(o.getDiscretisationLevel())
        
            try:
                current = iT2EC.getCentroid(overallOutputSet[o])
            except:
                current = Tuple(float("nan"),float("nan"))
            
            returnValue[o] = current
        return returnValue

    def weightedSigma(self,w,y) -> float:
        """Return the sigma based on COS inference data"""
        numerator = 0.0
        denominator = 0.0

        for i in range(len(w)):
            numerator += (w[i]*y[i].getSelectedCentroidEndpoint())
            denominator += w[i]
        
        if denominator == 0.0:
            return 0.0
        else:
            return numerator/denominator
    
    def removeRule(self,ruleNumber) -> None:
        """Remove a rule based on its index"""
        del self.rules[ruleNumber]
    
    def getImplicationMethod(self) -> str:
        """Return if the implication is product or minimum"""
        if self.implicationMethod == self.PRODUCT:
            return "product"
        else:
            return "minimum"
    
    def setImplicationMethod(self,implicationMethod) -> None:
        """Set the product or minimum implication method"""
        if implicationMethod == self.PRODUCT:
            self.implicationMethod = self.PRODUCT
        elif implicationMethod == self.MINIMUM:
            self.implicationMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) implication is currently supported.")
    
    def toString(self) -> str:
        """Convert the class to string"""
        s = "Interval Type-2 Fuzzy Logic System with "+str(self.getNumberOfRules())+" rules:\n"
        for i in range(self.getNumberOfRules()):
            s += str(self.rules[i].toString())+"\n"
        return s




                    






                






    