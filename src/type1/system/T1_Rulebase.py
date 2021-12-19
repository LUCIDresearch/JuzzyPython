
"""
T1_Rulebase.py
Created 19/12/2021
"""

from generic.Input import Input
from type1.sets.T1MF_Singleton import T1MF_Singleton
from typing import List
from collections import OrderedDict

from type1.system.T1_Antecedent import T1_Antecedent
from type1.system.T1_Consequent import T1_Consequent
from type1.system.T1_Rule import T1_Rule

class T1_Rulebase:
    """
    Class T1_Rulebase: 

    Parameters:
        
    Functions: 
      
    """

    def __init__(self) -> None:
        self.inferenceMethod = 1
        self.implicationMethod = 1
        self.PRODUCT = 0
        self.MINIMUM = 1
        self.DEBUG = False
        self.rules = []
        self.outputSetBuffers = OrderedDict()
        self.outputBuffers = OrderedDict()
    
    def addRule(self,r) -> None:
        self.rules.append(r)
        for c in r.getConsequents():
            if not c.getOutput() in self.outputSetBuffers.keys():
                self.outputSetBuffers[c.getOutput()] = [0.0] * c.getOutput().getDiscretisationLevel()
                self.outputBuffers[c.getOutput()] = None
            
    def getNumberOfOutputs(self) -> int:
        return len(self.outputBuffers)
    
    def getNumberOfRules(self) -> int:
        return len(self.rules)
    
    def getInferenceMethod(self) -> str:
        if self.inferenceMethod == self.PRODUCT:
            return "product"
        else:
            return "minimum"
    
    def setInferenceMethod(self,inferenceMethod) -> None:
        if inferenceMethod == self.PRODUCT:
            self.inferenceMethod = self.PRODUCT
        elif inferenceMethod == self.MINIMUM:
            self.inferenceMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) inference is currently supported.")

    def getImplicationMethod(self) -> str:
        if self.implicationMethod == self.PRODUCT:
            return "product"
        else:
            return "minimum"
    
    def setImplicationMethod(self,implicationMethod) -> None:
        if implicationMethod == self.PRODUCT:
            self.implicationMethod = self.PRODUCT
        elif implicationMethod == self.MINIMUM:
            self.implicationMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) implication is currently supported.")
    
    def getRule(self,r) -> T1_Rule:
        return self.rules[r]
    
    def getInputs(self) -> List[Input]:
        return self.rules[0].getInputs()
    
    def getOutputSetBuffers(self) -> dict:
        return self.outputSetBuffers
    
    def evaluate(self,defuzzType) -> dict:
        if defuzzType == 0:
            return self.heightDefuzzification()
        elif defuzzType == 1:
            return self.centroidDefuzzification()
        else:
            raise Exception("The T1 evaluate() method only supports height defuzzification (0) and centroid defuzzification (1).")
    
    def centroidDefuzzification(self) -> dict:
        for output in self.outputSetBuffers.keys():
            self.outputSetBuffers[output] = [0.0] * output.getDiscretisationLevel()
            
        
        fStrengths = []
        for i in range(len(self.rules)):
            fStrengths.append(self.rules[i].getFStrength(self.implicationMethod))
            if self.DEBUG:
                print(" fStrength of rule "+str(i)+" is: "+str(fStrengths[i]))
        
        for r in range(len(self.rules)):
            if self.DEBUG:
                print("Rule: " + str(r) + "\n" + self.rules[r] )
            
            consequentRule = self.rules[r].getConsequents()
            for c in consequentRule:
                o = c.getOutput()
                for i in range(o.getDiscretisationLevel()):
                    if self.inferenceMethod == self.PRODUCT:
                        if self.DEBUG:
                            print("output = "+o.getName() + "  outputSetBuffers.get(o)[i]= "+str(self.outputSetBuffers[o][i])+
                            "  fStrengths[r]="+str(fStrengths[r])+"   c.getMF().getFS(o.getDisc[i])="+str(c.getMF().getFS(o.getDiscretisations()[i]))+
                            "  o.getDisc[i]="+str(o.getDiscretisations()[i])+"     result: "+str(fStrengths[r] * c.getMF().getFS(o.getDiscretisations()[i])))
                        self.outputSetBuffers[o][i] = max(self.outputSetBuffers[o][i], fStrengths[r] * c.getMF().getFS(o.getDiscretisations()[i]))
                    else:
                        self.outputSetBuffers[o][i] = max(self.outputSetBuffers[o][i], min(fStrengths[r] , c.getMF().getFS(o.getDiscretisations()[i])))

        
        for o in self.outputBuffers.keys():
            numerator = 0.0
            denominator = 0.0
            for i in range(o.getDiscretisationLevel()):
                numerator += o.getDiscretisations()[i] * self.outputSetBuffers[o][i]
                denominator += self.outputSetBuffers[o][i]
            self.outputBuffers[o] = numerator/denominator
        
        return self.outputBuffers
    
    def heightDefuzzification(self) -> dict:
        for o in self.outputSetBuffers.keys():
            self.outputSetBuffers[o] == [0.0] *2
      
        fStrengths = []
        for i in range(len(self.rules)):
            fStrengths.append(self.rules[i].getFStrength(self.implicationMethod))
            if self.DEBUG:
                print(" fStrength of rule "+str(i)+" is: "+str(fStrengths[i]))

        for r in range(len(self.rules)):
            consequentRule = self.rules[r].getConsequents()
            for c in consequentRule:
                o = c.getOutput()
                self.outputSetBuffers[0][0] = self.outputSetBuffers


    



    
    