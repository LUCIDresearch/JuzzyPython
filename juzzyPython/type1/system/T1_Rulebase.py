
"""
T1_Rulebase.py
Created 19/12/2021
"""

from juzzyPython.generic.Input import Input
from typing import List
from collections import OrderedDict
from juzzyPython.type1.system.T1_Rule import T1_Rule
from numpy import float64 as f

class T1_Rulebase:
    """
    Class T1_Rulebase: 
    Class Capturing an entire Type-1 FLS through its rules.

    Parameters:None
        
    Functions: 
        addRule
        getNumberOfOutputs
        getNumberOfRules
        getInferenceMethod
        setInferenceMethod
        getImplicationMethod
        setImplicationMethod
        getRule
        getInputs
        getOutputSetBuffers
        evaluate
        centroidDefuzzification
        heightDefuzzification
        getRules
        changeRule
        removeRule
        toString
      
    """

    def __init__(self) -> None:
        self.inferenceMethod = 1
        self.implicationMethod = 1
        self.PRODUCT = 0
        self.MINIMUM = 1
        self.DEBUG = False
        self.rules = []
        self.outputSetBuffers = OrderedDict() #a buffer for the discretised output sets (yLevels) of each output
        self.outputBuffers = OrderedDict() #buffers the actual outputs of the rulebase (one per output)
    
    def addRule(self,r: T1_Rule) -> None:
        """add a rule to the set and buffers"""
        self.rules.append(r)
        for c in r.getConsequents():
            if not c.getOutput() in self.outputSetBuffers.keys():
                self.outputSetBuffers[c.getOutput()] = [0.0] * c.getOutput().getDiscretisationLevel()
                self.outputBuffers[c.getOutput()] = None
            
    def getNumberOfOutputs(self) -> int:
        """Get the number of output buffers"""
        return len(self.outputBuffers)
    
    def getNumberOfRules(self) -> int:
        """Get the number of rules"""
        return len(self.rules)
    
    def getInferenceMethod(self) -> str:
        """Returns the current Inference Method as used for all rules."""
        if self.inferenceMethod == self.PRODUCT:
            return "product"
        else:
            return "minimum"
    
    def setInferenceMethod(self,inferenceMethod: int) -> None:
        """Sets the inference method, where by inference, we mean the implementation
        of applying the rule's firing strength to the consequent.
        The desired inference method is applied for all rules."""
        if inferenceMethod == self.PRODUCT:
            self.inferenceMethod = self.PRODUCT
        elif inferenceMethod == self.MINIMUM:
            self.inferenceMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) inference is currently supported.")

    def getImplicationMethod(self) -> str:
        """Returns the current Implication Method as used for all rules."""
        if self.implicationMethod == self.PRODUCT:
            return "product"
        else:
            return "minimum"
    
    def setImplicationMethod(self,implicationMethod: int) -> None:
        """Sets the implication method, where by implication, we mean the implementation
        of the AND logical connective between parts of the antecedent.
        The desired implication method is applied for all rules."""
        if implicationMethod == self.PRODUCT:
            self.implicationMethod = self.PRODUCT
        elif implicationMethod == self.MINIMUM:
            self.implicationMethod = self.MINIMUM
        else:
            raise Exception("Only product (0) and minimum (1) implication is currently supported.")
    
    def getRule(self,r: T1_Rule) -> T1_Rule:
        """Return a specific rule"""
        return self.rules[r]
    
    def getInputs(self) -> List[Input]:
        """This method assumes all rules use the same (and all) inputs. 
        The first rule is queried to identify the inputs and return them.
        return a list of the inputs used in the rulebase (retrieved from the 
        antecedents of the first rule in the rulebase!)."""
        return self.rules[0].getInputs()
    
    def getOutputSetBuffers(self) -> dict:
        """Returns the outputSetBuffers"""
        return self.outputSetBuffers
    
    def evaluate(self,defuzzType: int) -> dict:
        """ Returns defuzzified result of evaluating all rules in the rulebase.
        param defuzzificationType The type of defuzzifier to be used: 0-Height 
        Defuzzification, 1-Centroid Defuzzification.
        param discretizationLevel The discretization level to be employed (only
        applies to centroid defuzzification)"""
        if defuzzType == 0:
            return self.heightDefuzzification()
        elif defuzzType == 1:
            return self.centroidDefuzzification()
        else:
            raise Exception("The T1 evaluate() method only supports height defuzzification (0) and centroid defuzzification (1).")
    
    def centroidDefuzzification(self) -> dict:
        """Inference and Centroid Defuzzification"""
        for output in self.outputSetBuffers.keys():
            self.outputSetBuffers[output] = [0.0] * output.getDiscretisationLevel()
            
        
        fStrengths = []
        for i in range(len(self.rules)):
            fStrengths.append(self.rules[i].getFStrength(self.implicationMethod))
            if self.DEBUG:
                print(" fStrength of rule "+str(i)+" is: "+str(fStrengths[i]))
        
        for r in range(len(self.rules)):
            if self.DEBUG:
                print("Rule: " + str(r) + "\n" + self.rules[r].toString() )
            
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
                        self.outputSetBuffers[o][i] = max(self.outputSetBuffers[o][i], 
                        min(fStrengths[r] ,
                        c.getMF().getFS(o.getDiscretisations()[i])))

        
        for o in self.outputBuffers.keys():
            numerator = 0.0
            denominator = 0.0
            for i in range(o.getDiscretisationLevel()):
                numerator += o.getDiscretisations()[i] * self.outputSetBuffers[o][i]
                denominator += self.outputSetBuffers[o][i]
            if denominator == 0:
                self.outputBuffers[o] = float("nan")
            else:
                self.outputBuffers[o] = f(numerator)/denominator
        
        return self.outputBuffers
    
    def heightDefuzzification(self) -> dict:
        """Inference and Height  Defuzzification"""
        for o in self.outputSetBuffers.keys():
            self.outputSetBuffers[o] = [0.0] *2
      
        fStrengths = []
        for i in range(len(self.rules)):
            fStrengths.append(self.rules[i].getFStrength(self.implicationMethod))
            if self.DEBUG:
                print(" fStrength of rule "+str(i)+" is: "+str(fStrengths[i]))

        for r in range(len(self.rules)):
            consequentRule = self.rules[r].getConsequents()
            for c in consequentRule:
                o = c.getOutput()
                if self.DEBUG:
                    print(c.getMF().getPeak())
                
                self.outputSetBuffers[o][0] = self.outputSetBuffers[o][0] + fStrengths[r] * c.getMF().getPeak()
                self.outputSetBuffers[o][1] = self.outputSetBuffers[o][1] + fStrengths[r]
        
        
        for o in self.outputBuffers.keys():
            if self.outputSetBuffers[o][1] == 0:
                self.outputBuffers[o] = float("nan")
            else:
                self.outputBuffers[o] = f(self.outputSetBuffers[o][0])/self.outputSetBuffers[o][1]
        
        return self.outputBuffers
    
    def getRules(self) -> List[T1_Rule]:
        """Get the list of rules"""
        return self.rules
    
    def changeRule(self,ruleNum: int,newRule: T1_Rule) -> None:
        """Change a current rule"""
        self.rules[ruleNum] = newRule
    
    def removeRule(self,ruleNum: int) -> None:
        """Remove a rule from the set"""
        del self.rules[ruleNum]
    
    def toString(self) -> str:
        """Convert all the rules to string"""
        s="Type-1 Fuzzy Logic System with "+str(self.getNumberOfRules())+" rules:\n"
        for i in range(self.getNumberOfRules()):
            s+= str(self.rules[i].toString()) + "\n"
        return s

    
    



    
    