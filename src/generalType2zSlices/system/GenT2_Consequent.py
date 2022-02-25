"""
GenT2_Consequent.py
Created 6/1/2022
"""
import sys

from generic.Output import Output
from generic.Tuple import Tuple
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from intervalType2.system.IT2_Consequent import IT2_Consequent
from typing import List

class GenT2_Consequent():
    """
    Class GenT2_Consequent
    Creates a new instance of Consequent    

    Parameters: 
       name
       set
       output

    Functions:
        getSet
        getName
        setName
        getOutput
        setOutput
        getConseuqnetsIT2Sets
        equals
        toString
       
    """

    def __init__(self,name: str,set_: GenT2MF_Interface,output: Output) -> None:
        self.set = set_
        self.name = name
        self.output = output
        self.set.setSupport(Tuple(max(self.set.getSupport().getLeft(), self.output.getDomain().getLeft()),min(self.set.getSupport().getRight(), self.output.getDomain().getRight())))

    def getSet(self) -> GenT2MF_Interface:
        """Return the set of the consequent"""
        return self.set
    
    def getName(self) -> str:
        """Return the name of the consequent"""
        return self.name
    
    def setName(self,name: str) -> None:
        """Set the name of the consequent"""
        self.name = name
    
    def getOutput(self) -> Output:
        """Get the output of the consequent"""
        return self.output
    
    def setOutput(self,o: Output) -> None:
        """Set the output of the consequent"""
        self.output = o
    
    def getConsequentsIT2Sets(self) -> List[IT2_Consequent]:
        """Returns this antecedent as a series of consequents (each based on a single zSlice) for interval type-2 FLSs."""
        cons = [0] * self.getSet().getNumberOfSlices()
        for i in range(len(cons)):
            cons[i] = IT2_Consequent(self.getSet().getZSlice(i),self.getOutput(),self.getName()+"_zSlices:"+str(i))
        return cons
    
    def equals(self,a: object) -> bool:
        """Check if equal to class"""
        if self == a:
            return True
        if not isinstance(a,GenT2_Consequent):
            return False
        return self.getSet() == a.getSet()
    
    def toString(self) -> str:
        """Return class as string"""
        return self.getSet().getName()
    

