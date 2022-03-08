"""
IT2_Rule.py
Created 14/1/2022
"""
from __future__ import annotations
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from generic.Input import Input
from type1.sets.T1MF_Interface import T1MF_Interface
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from intervalType2.system.IT2_Consequent import IT2_Consequent
from type1.sets.T1MF_Singleton import T1MF_Singleton
from typing import List

class IT2_Rule():
    """
    Class IT2_Rule
    Rule class for Interval Type-2 FLSs. Note that currently only a single
    consequent per rule is supported.

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
        getConsequentCentroid
    """

    def __init__(self,antecedents: List[IT2_Antecedent],consequent: IT2_Consequent = None, consequents: List[IT2_Consequent] = None) -> None:
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
    
    def getAntecedents(self) -> List[IT2_Antecedent]:
        """Return the list of antecedents"""
        return self.antecedents
    
    def getConsequents(self) -> List[IT2_Consequent]:
        """Return the list of consequents"""
        return list(self.consequents.values())
    
    def getInputs(self) -> List[Input]:
        """Return the list of inputs"""
        inputs = []
        for i in range(self.getNumberOfAntecedents()):
            inputs.append(self.antecedents[i].getInput())
        return inputs
    
    def compareBasedOnAntecedents(self,r: IT2_Rule) -> bool:
        """Performs a comparison operation by comparing the rule objects solely based 
        on their antecedents. The method returns true of the antecedents of both
        rules are the same."""
        if self.getNumberOfAntecedents() == r.getNumberOfAntecedents():
            for i in range(self.getNumberOfAntecedents):
                if self.antecedents[i].compareTo(r.getAntecedents()[i]) != 0:
                    return False
                return True
        return False
    
    def getConsequentCentroid(self,o: object) -> Tuple:
        """Return the consequent centroid of the ouput"""
        return self.consequents[o].getCentroid()

    def getFStrength(self,tNorm: int) -> float:
        """Returns the rule's firing strength. The method relies on the transparent 
        updating of the inputs of the fuzzy system through the Input classes 
        attached to the antecedents."""
        fStrength = Tuple(1.0,1.0)
        if tNorm == self.PRODUCT:
            for i in range(self.getNumberOfAntecedents()):
                if isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Singleton):
                    fStrength.setLeft(fStrength.getLeft()*self.antecedents[i].getFS().getLeft())
                    fStrength.setRight(fStrength.getRight()*self.antecedents[i].getFS().getRight())
                elif isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Interface):
                    xmax = self.antecedents[i].getMax(self.PRODUCT)
                    fStrength.setLeft(fStrength.getLeft()*self.antecedents[i].getMF().getLMF().getFS(xmax.getLeft())*self.antecedents[i].getInput().getInputMF().getFS(xmax.getLeft()))
                    fStrength.setRight(fStrength.getRight()*self.antecedents[i].getMF().getUMF().getFS(xmax.getRight())*self.antecedents[i].getInput().getInputMF().getFS(xmax.getRight()))
                else:
                    xmax = self.antecedents[i].getMax(self.PRODUCT)
                    fStrength.setLeft(fStrength.getLeft()*self.antecedents[i].getMF().getLMF().getFS(xmax.getLeft())*self.antecedents[i].getInput().getInputMF().getLMF().getFS(xmax.getLeft()))
                    fStrength.setRight(fStrength.getRight()*self.antecedents[i].getMF().getUMF().getFS(xmax.getRight())*self.antecedents[i].getInput().getInputMF().getUMF().getFS(xmax.getRight()))
        else:
            for i in range(self.getNumberOfAntecedents()):
                
                if isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Singleton):
                    fStrength.setLeft(min(fStrength.getLeft(),self.antecedents[i].getFS().getLeft()))
                    fStrength.setRight(min(fStrength.getRight(),self.antecedents[i].getFS().getRight()))

                elif isinstance(self.antecedents[i].getInput().getInputMF(),T1MF_Interface):
                    xmax = self.antecedents[i].getMax(self.MINIMUM)
                    fStrength.setLeft(min(fStrength.getLeft(),min(self.antecedents[i].getMF().getLMF().getFS(xmax.getLeft()),self.antecedents[i].getInput().getInputMF().getFS(xmax.getLeft()))))
                    fStrength.setRight(min(fStrength.getRight(),min(self.antecedents[i].getMF().getUMF().getFS(xmax.getRight()),self.antecedents[i].getInput().getInputMF().getFS(xmax.getRight()))))

                else:
                    xmax = self.antecedents[i].getMax(self.MINIMUM)
                    fStrength.setLeft(min(fStrength.getLeft(),min(self.antecedents[i].getMF().getLMF().getFS(xmax.getLeft()),self.antecedents[i].getInput().getInputMF().getLMF().getFS(xmax.getLeft()))))
                    fStrength.setRight(min(fStrength.getRight(),min(self.antecedents[i].getMF().getUMF().getFS(xmax.getRight()),self.antecedents[i].getInput().getInputMF().getUMF().getFS(xmax.getRight()))))

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
    