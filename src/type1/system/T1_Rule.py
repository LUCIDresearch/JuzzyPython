
"""
T1_Rule.py
Created 19/12/2021
"""

from generic.Input import Input
from type1.sets.T1MF_Singleton import T1MF_Singleton
from typing import List

from type1.system.T1_Antecedent import T1_Antecedent
from type1.system.T1_Consequent import T1_Consequent

class T1_Rule:
    """
    Class T1_Rule: 
    Rule for a Type-1 Fuzzy System.

    Parameters:
        Antecedents:The array of antecedents
        Consequent:The consequent (only a single consequent is supported here)
        Consequents:The array of consequents 
        
    Functions: 
        getNumberOfAntecedents
        getNumberOfConsequents
        getAntecedents
        getConsequents
        getInputs
        compareBasedOnAntecedents
        getFStrength
        toString
      
    """

    def __init__(self,antecedents,consequent = None, consequents = None) -> None:
        self.DEBUG = False
        self.PRODUCT = 0
        self.MINIMUM = 1
        self.antecedents = antecedents
        self.consequents = {}
        if consequent != None:
            self.consequents[consequent.getOutput()] = consequent
        else:
            for i in consequents:
                self.consequents[i.getOutput()] = i
    
    def getNumberOfAntecedents(self) -> int:
        """Return the number of antecedents"""
        return len(self.antecedents)
    
    def getNumberOfConsequents(self) -> int:
        """Return the number of consequents"""
        return len(self.consequents)
    
    def getAntecedents(self) -> List[T1_Antecedent]:
        """Return the list of antecedents"""
        return self.antecedents
    
    def getConsequents(self) -> List[T1_Consequent]:
        """Return the list of consequents"""
        return self.consequents.values()
    
    def getInputs(self) -> List[Input]:
        """Return the list of inputs"""
        inputs = []
        for i in range(self.getNumberOfAntecedents()):
            inputs.append(self.antecedents[i].getInput())
        return inputs
    
    def compareBasedOnAntecedents(self,r) -> bool:
        """Performs a comparison operation by comparing the rule objects solely based 
        on their antecedents. The method returns true of the antecedents of both
        rules are the same."""
        if self.getNumberOfAntecedents() == r.getNumberOfAntecedents():
            for i in range(self.getNumberOfAntecedents):
                if self.antecedents[i].compareTo(r.getAntecedents()[i]) != 0:
                    return False
                return True
        return False

    def getFStrength(self,tNorm) -> float:
        """Returns the rule's firing strength. The method relies on the transparent 
        updating of the inputs of the fuzzy system through the Input classes 
        attached to the antecedents."""
        fStrength = 1.0
        if tNorm == self.PRODUCT:
            for i in range(self.getNumberOfAntecedents()):
                if isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Singleton):
                    if self.DEBUG:
                        print("Antecedent "+str(i)+" gives a FS of: "+str(self.antecedents[i].getFS())
                        +" with an input of: "+str(self.antecedents[i].getInput().getInput()))
                    fStrength *= self.antecedents[i].getFS()
                else:
                    xmax = self.antecedents[i].getMax(0)
                    fStrength *= self.antecedents[i].getInput().getInputMF().getFS(xmax)*self.antecedents[i].getMF().getFS(xmax)
        else:
            for i in range(self.getNumberOfAntecedents()):
                if isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Singleton):
                    if self.DEBUG:
                        print("Antecedent "+str(i)+" gives a FS of: "+str(self.antecedents[i].getFS())
                        +" with an input of: "+str(self.antecedents[i].getInput().getInput()))
                    fStrength = min(fStrength,self.antecedents[i].getFS())
                else:
                    xmax = self.antecedents[i].getMax(1)
                    fStrength = min(fStrength,min(self.antecedents[i].getInput().getInputMF().getFS(xmax),self.antecedents[i].getMF().getFS(xmax)))
        return fStrength

    def toString(self) -> str:
        """Convert antecedent to string"""
        s="IF ";
        for i in range(self.getNumberOfAntecedents()):
            s+=self.getAntecedents()[i].getName()+" "
            if((i+1)<self.getNumberOfAntecedents()):
                s+="AND "
            else:
                s+="THEN "
        for i in range(self.getNumberOfConsequents()):
            s+= self.getConsequents()[i].getName()+" "
            if((i+1)<self.getNumberOfConsequents()):
                s+="AND "
        return s;
    
