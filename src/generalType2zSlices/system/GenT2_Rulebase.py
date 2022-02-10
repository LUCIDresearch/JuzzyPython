"""
GenT2_Rulebase.py
Created 9/1/2022
"""
import sys

sys.path.append("..")

from generic.Input import Input
from generic.Output import Output
from generic.Tuple import Tuple

from generalType2zSlices.system.GenT2Engine_Intersection import GenT2Engine_Intersection
from generalType2zSlices.system.GenT2Engine_Union import GenT2Engine_Union
from generalType2zSlices.system.GenT2_Rule import GenT2_Rule

from generalType2zSlices.system.GenT2_Antecedent import GenT2_Antecedent
from generalType2zSlices.system.GenT2_Consequent import GenT2_Consequent
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generalType2zSlices.sets.GenT2MF_CylExtension import GenT2MF_CylExtension
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from generalType2zSlices.sets.GenT2MF_Intersection import GenT2MF_Intersection

from intervalType2.system.IT2_Rulebase import IT2_Rulebase
from intervalType2.system.IT2_Rule import IT2_Rule
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from intervalType2.system.IT2_Consequent import IT2_Consequent
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface

from type1.sets.T1MF_Interface import T1MF_Interface
from type1.sets.T1MF_Meet import T1MF_Meet
from typing import List, OrderedDict

class GenT2_Rulebase():
    """
    Class GenT2_Rulebase
    Keeps track of rules and generates results
  
    Parameters: 
        None

    Functions:
        addRule
        addRules
        getRules
        getFuzzyLogicType
        get_GenT2zEngine_Intersection
        get_GenT2zEngineUnion
        getOverallOutput
        evaluateGetCentroid
        evaluate
        getIT2Rulebases
        getRule
        changeRule
        removeRule
        getNumberOfRules
        containsRule
        getRulesWithAntecedents
        getImplicationMethod
        setImplicationMethod
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
        self.gzEU = GenT2Engine_Union()
        self.gzEI = GenT2Engine_Intersection()
    
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
    
    def getRules(self) -> List[GenT2_Rule]:
        """Return all the rules in the set"""
        return self.rules
    
    def getRule(self,ruleNum) -> GenT2_Rule:
        """Return a specific rule"""
        return self.rules[ruleNum]
    
    def getNumberOfRules(self) -> int:
        """Get the number of rules in the set"""
        return len(self.rules)
    
    def getFuzzyLogicType(self) -> int:
        """Returns the type of fuzzy logic that is employed.
        return 0: type-1, 1: interval type-2, 2: zSlices based general type-2"""
        return 2
    
    def containsRule(self,rule) -> bool:
        """Check if a rule in the ruleset"""
        return rule in self.rules
    
    def getGenT2zEngineIntersection(self) -> GenT2Engine_Intersection:
        """Return the intersection engine"""
        return self.gzEI
    
    def getGenT2zEngineUnion(self) -> GenT2Engine_Union:
        """Return the union engine"""
        return self.gzEU
    
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
        """Sets the implication method, where by implication, we mean the implementation
        of the AND logical connective between parts of the antecedent.
        The desired implication method is applied for all rules."""
        if implicationMethod == self.PRODUCT:
            self.implicationMethod = self.PRODUCT
        elif implicationMethod == self.MINIMUM:
            self.implicationMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) implication is currently supported.")
    
    def toString(self) -> str:
        """Convert the class to string"""
        s = "General Type-2 Fuzzy Logic System with "+str(self.getNumberOfRules())+" rules:\n"
        for i in range(self.getNumberOfRules()):
            s += str(self.rules[i].toString())+"\n"
        return s
    
    def getOverallOutput(self) -> dict:
        """Return the overall output of the rules"""
        returnValue = OrderedDict()
        for r in range(len(self.rules)):
            temp = self.rules[r].getRawOutput()
            for o in self.outputs:
                if r == 0:
                    returnValue[o] = temp[o]
                else:
                    returnValue[o] = self.gzEU.getUnion(returnValue.get(o),temp.get(o))
        return returnValue
    
    def evaluateGetCentroid(self,typeReductionType) -> dict:
        """Returns the output of the FLS after type-reduction, i.e. the centroid.
        param: typeReductionType
        return: A TreeMap where Output is used as key and the value is an Object[]
        where Object[0] is a Tuple[] (the centroids, one per zLevel) and Object[1] is a Double holding the associated yValues for the centroids. If not rule fired for the given input(s),
        then null is returned as an Object[]."""
        returnValue = OrderedDict()
        rbsIT2 = self.getIT2Rulebases()
        zValues = self.rules.get(0).getAntecedents()[0].getSet().getZValues()

        for i in range(len(rbsIT2)):
            temp = rbsIT2[i].evaluateGetCentroid(typeReductionType)
            for o in temp.keys():
                if i == 0:
                    returnValue[o] = [[],[]]
                returnValue[o][0].append(temp[o][0])
                returnValue[o][1].append(zValues[i])
        return returnValue
    
    def evaluate(self,typeReductionType) -> dict:
        """The current evaluate function is functional but inefficient. It creates an IT2
        version of all the rules in the rulebase and computes each IT2 rule separately...
        param typeReductionType: 0: Center Of Sets, 1: Centroid
        param discretizationLevel: The discretization level on the xAxis"""
        returnValue = OrderedDict()
        rbsIT2 = self.getIT2Rulebases()
        rawOutputValues = []

        for i in range(len(rbsIT2)):
            rawOutputValues.append(rbsIT2[i].evaluate(typeReductionType))
        zValues = self.rules[0].getAntecedents()[0].getSet().getZValues()

        for o in self.outputs:
            i=0
            numerator = 0.0
            denominator = 0.0

            for outputValue in rawOutputValues:
                numerator += outputValue[o] * zValues[i]
                denominator += zValues[i]
                i+= 1
            returnValue[o] = numerator/denominator
        return returnValue
    
    def getIT2Rulebases(self) -> List[IT2_Rulebase]:
        """Returns the whole zSlices based rulebase as a series of interval type-2
        rule bases (one per zLevel) which can then be computed in parallel.
        param typeReductionMethod: The type-reduction method to be used at the IT2 level 
        0: Center Of Sets,  1: Centroid.
        param discretizationLevelXAxis: The number of discretizations to be used at the IT2 level."""
        rbs = [0] * self.rules[0].getAntecedents()[0].getSet().getNumberOfSlices()
        for i in range(len(rbs)):
            rbs[i] = IT2_Rulebase(self.getNumberOfRules())
            for currentRule in range(self.getNumberOfRules()):
                rbs[i].addRule(self.rules[currentRule].getRuleasIT2Rules()[i])
            rbs[i].setImplicationMethod(self.implicationMethod)
        return rbs
    
    def getRulesWithAntecedents(self,antecedents) -> List[GenT2_Rule]:
        """ Returns all rules with a matching (i.e. equal) set of antecedents."""
        matches = []
        for i in range(len(self.rules)):
            if self.rules[i].getAntecedents()==antecedents:
                matches.append(self.rules[i])
        return matches
    

    
