"""
GenT2_Antecedent.py
Created 6/1/2022
"""
import sys

from numpy import number

from generic.Input import Input
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from type1.sets.T1MF_Interface import T1MF_Interface
from typing import List

class GenT2_Antecedent():
    """
    Class GenT2_Antecedent
    Creates a new instance of Antecedent which uses an Input object.

    Parameters: 
        name: name of antecedent
        set: the membership functions
        input: input values
    
    Functions:
        getName
        setName
        getFS
        getSet
        getAntecedentasIT2Sets
        getInput
        equals
        toString
    
    """

    def __init__(self,name: str,set: GenT2MF_Interface,input: Input) -> None:
        self.name = name
        self.input = input
        self.set = set

    def getName(self) -> str:
        """Return the name of the antecedent"""
        return self.name
    
    def setName(self,name: str) -> None:
        """set the name of the antecedent"""
        self.name = name
    
    def getFS(self) -> T1MF_Interface:
        """get the firing strength"""
        if self.set.getSupport().contains(self.input.getInput()):
            return self.set.getFS(self.input.getInput())
        else:
            return None
    
    def getSet(self) -> GenT2MF_Interface:
        """Return the set"""
        return self.set
    
    def getAntecedentasIT2Sets(self) -> List[IT2_Antecedent]:
        """Returns this antecedent as a series of antecedents (each based on a single zSlice) for interval type-2 FLSs."""
        ants = [0] * self.getSet().getNumberOfSlices()
        for i in range(len(ants)):
            ants[i] = IT2_Antecedent(self.getSet().getZSlice(i),self.getInput(),self.getName()+"_zSlices:"+str(i))
        return ants
    
    def getInput(self) -> Input:
        """Return the input"""
        return self.input
    
    def equals(self,a: object) -> bool:
        """Check if equal to class"""
        if self == a:
            return True
        if not isinstance(a,GenT2_Antecedent):
            return False
        return self.getSet() == a.getSet()
    
    def toString(self) -> str:
        """Return class as string"""
        return "Antecedent_for:"+self.getSet().getName()
    
