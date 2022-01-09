"""
IntervalT2MF_Union.py
Created 9/1/2022
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from type1.sets.T1MF_Union import T1MF_Union
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
    
    def __init__(self, a,b) -> None:
        self.DEBUG = False
        self.isNull = False
        self.sets = {}

        super.__init__("Union of  ("+a.getName()+" and "+b.getName()+")")
        self.uMF = T1MF_Union(a.getUMF(),b.getUMF())
        self.lMF = T1MF_Union(a.getLMF(),b.getLMF())
        self.support = Tuple(min(a.getSupport().getLeft(),b.getSupport.getLeft()),max(a.getSupport().getRight(),b.getSupport().getRight()))
    
    def getSets(self) -> set:
        """Return sets"""
        return self.sets
    
    def isNull(self) -> bool:
        """Return if null"""
        return self.isNull
    
    def getPeak(self) -> float:
        """Unsupported Function"""
        raise Exception("Unsupported Function")
        
        
