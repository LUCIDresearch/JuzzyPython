
"""
T1MF_Singleton.py
Created 17/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
import type1.sets.T1MF_Triangular
import functools
@functools.total_ordering
class T1MF_Singleton(T1MF_Prototype):
    """
    Class T1MF_Singleton
    Membership Function represented by a single double value - 
    for example heavily used in TSK/Anfis for consequents.

    Parameters: 
        value: the value where the singleton exists
        name: the name of the membership function

    Functions:
        getValue
        getFS
        getPeak
        getAlphaCut
        toString
        compareTo
        
    """

    def __init__(self, value: float, name: str = None) -> None:
        self.value = value
        if name:
            super().__init__(name)
            self.support = Tuple(value,value)
        else:
            super().__init__("")
    
    def getValue(self) -> float:
        """Return the value where the singleton exists"""
        return self.value
    
    def getFS(self, x: float) -> float:
        """Return the maximum FS between two sets"""
        if x == self.value:
            return 1.0
        else:
            return 0.0
    
    def getPeak(self) -> float:
        """Get the peak of the singleton"""
        return self.getValue()
    
    def getAlphaCut(self, alpha: float = None) -> Tuple:
        """Return the alpha cut of the singleton as a tuple"""
        return Tuple(self.value,self.value)
    
    def toString(self) -> str:
        """Convert the function to a string"""
        return self.name+ " - Singleton at: "+str(self.value)

    def compareTo(self, o: object) -> int:
        """Compare to a singleton or a triangular function"""
        if type(o) is T1MF_Singleton:
            if self.getValue() == o.getValue():
                return 0
            if self.getValue() < o.getValue():
                return -1
            return 1
        elif type(o) is type1.sets.T1MF_Triangular.T1MF_Triangular:
            if self.getValue() < o.getPeak():
                return -1
            return 1
        else:
            raise Exception("A T1MF_Triangular object is expected for comparison with another T1MF_Triangular ot T1MF_Singleton object.")
    
    def __eq__(self, o: object):
        val = self.compareTo(o)
        if val == 0:
            return True
        else:
            return False

    def __lt__(self, o: object):
        val = self.compareTo(o)
        if val == -1:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.getName())
        