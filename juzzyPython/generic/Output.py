
"""
Output.py
Created 10/12/2021
"""
from juzzyPython.generic.Tuple import Tuple
from typing import List
import functools

@functools.total_ordering
class Output: 
    """
    Class Output: 
    Enables the labeling of an output and captures the allowable domain for a given output.

    Parameters:
        name = name of output (String)
        domain = (Tuple)
        discretisationLevel = (Int) (Optional)

    Functions: 
        getName
        setName
        getDiscretisationLevel
        setDiscretisationLevel
        getDomain
        setDomain
        getDiscretisations
    """

    def __init__(self,name: str,domain: Tuple,discretisationLevel: int = None) -> None:
        self.discretisationLevel = 100
        self.name = name
        self.domain = domain
        self.discretisedDomain = None
        if discretisationLevel != None:
            self.discretisationLevel = discretisationLevel
    
    def getName(self) -> str:
        """Return the name of the output"""
        return self.name
    
    def setName(self,name: str) -> None:
        """Set the name of the output"""
        self.name = name
    
    def getDiscretisationLevel(self) -> int:
        """Get the current discretisation level"""
        return self.discretisationLevel
    
    def setDiscretisationLevel(self,level: int) -> None:
        """Set a new discretisation level"""
        self.discretisationLevel = level
    
    def getDomain(self) -> Tuple:
        """Get the current domain tuple"""
        return self.domain
    
    def setDomain(self,domain: Tuple):
        """Set a new domain"""
        self.domain = domain
    
    def getDiscretisations(self) -> List[float]:
        """Returns an array with discrete values over the domain of this output. This 
        discrete array is buffered in the Output object, i.e. if the same discretisation 
        is kept, it is efficient to use the array from the output object (e.g. in rule-based
        inference)."""
        if self.discretisedDomain == None or len(self.discretisedDomain) != self.discretisationLevel:
            self.discretisedDomain = [0] * self.discretisationLevel
            stepsize = self.domain.getSize()/(self.discretisationLevel-1.0)
            self.discretisedDomain[0] = self.domain.getLeft()
            self.discretisedDomain[self.discretisationLevel-1] = self.domain.getRight()
            for i in range(1,self.discretisationLevel-1):
                self.discretisedDomain[i] = self.domain.getLeft()+i*stepsize
            return self.discretisedDomain
        else:
            return self.discretisedDomain
    
    def __eq__(self, o: object):
        return isinstance(o,Output) and self.getName() == o.getName()

    def __lt__(self, o: object):
        return isinstance(o,Output) and self.getName() < o.getName()

    def __hash__(self) -> int:
        return hash(self.getName())
