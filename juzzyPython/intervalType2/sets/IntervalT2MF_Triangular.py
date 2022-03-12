"""
IntervalT2MF_Triangular.py
Created 8/1/2022
"""
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular

class IntervalT2MF_Triangular(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Triangular

    Parameters: 
        upper: Upper membership function
        lower: Lower membership function

    Functions:
        getLMF
        getUMF
        getFS

    """
    
    def __init__(self, name: str, upper: T1MF_Triangular = None, lower: T1MF_Triangular = None) -> None:
        if upper == None and lower == None:
            super().__init__(name)
        else:
            super().__init__(name,upper,lower)
            if upper.getStart()>lower.getStart() or upper.getEnd()<lower.getEnd():
                raise Exception("The upper membership function needs to be higher than the lower membership function.")
    
    def getLMF(self) -> T1MF_Triangular:
        """Return the lower membership function"""
        return self.lMF
    
    def getUMF(self) -> T1MF_Triangular:
        """Return the upper membership function"""
        return self.uMF
    
    def getFS(self,x: float) -> Tuple:
        """Get the firing strength"""
        l = self.lMF.getFS(x)
        u = self.uMF.getFS(x)

        if self.lMF.getPeak() == self.uMF.getPeak():
            return Tuple(min(l,u),max(l,u))
        else:
            if x <= max(self.lMF.getPeak(),self.uMF.getPeak()) and x >= min(self.lMF.getPeak(),self.uMF.getPeak()):
                return Tuple(min(l,u),1.0)
            else:
                return Tuple(min(l,u),max(l,u))
