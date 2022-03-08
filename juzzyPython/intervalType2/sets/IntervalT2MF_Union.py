"""
IntervalT2MF_Union.py
Created 9/1/2022
"""

from juzzyPython.intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from juzzyPython.type1.sets.T1MF_Union import T1MF_Union
class IntervalT2MF_Union(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Union
    Union operation for interval type 2

    Parameters: 
        a
        b

    Functions:
       getSets
       isNull
       getPeak


    """
    
    def __init__(self, a: IntervalT2MF_Interface,b: IntervalT2MF_Interface) -> None:
        self.DEBUG = False
        self.isNull_ = False
        self.sets = {}

        super().__init__("Union of  ("+a.getName()+" and "+b.getName()+")")
        self.uMF = T1MF_Union(a.getUMF(),b.getUMF())
        self.lMF = T1MF_Union(a.getLMF(),b.getLMF())
        self.support = Tuple(min(a.getSupport().getLeft(),b.getSupport().getLeft()),max(a.getSupport().getRight(),b.getSupport().getRight()))
    
    def getSets(self) -> set:
        """Return sets"""
        return self.sets
    
    def isNull(self) -> bool:
        """Return if null"""
        return self.isNull_
    
    def getPeak(self) -> float:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
        
        
