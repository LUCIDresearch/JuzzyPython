"""
IntervalT2MF_Gauangle.py
Created 10/1/2022
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from type1.sets.T1MF_Gauangle import T1MF_Gauangle
class IntervalT2MF_Gauangle(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Gauangle
    Creates a new instance of the IT2 Gauangle set

    Parameters: 
        name: Name of membership function
        uMF: Upper membership function
        lMF: Lower membership function

    Functions:
        toString
        getFS
        
    """
    def __init__(self, name: str, uMF: T1MF_Gauangle, lMF: T1MF_Gauangle) -> None:
        super().__init__(name)
        self.uMF = uMF
        self.lMF = lMF
        self.support = Tuple(min(uMF.getSupport().getLeft(),lMF.getSupport().getLeft()),max(uMF.getSupport().getRight(),lMF.getSupport().getRight()))
    
    def toString(self) -> str:
        """Convert the membership function to string"""
        s = self.getName()+" - IT2 Gauangle with UMF:\n"+str(self.getUMF())+" and LMF:\n"+str(self.getLMF())
        if(self.LeftShoulder):
            s+="\n (LeftShoulder)"
        if(self.RightShoulder):
            s+="\n (RightShoulder)"
        return s;        
    
    def getFS(self, x: float) -> float:
        """Get the firing strength of the membership function"""
        l = self.lMF.getFS(x)
        u = self.uMF.getFS(x)

        if self.lMF.getPeak() == self.uMF.getPeak():
            return Tuple(min(l,u),max(l,u))
        else:
            if x <= max(self.lMF.getPeak(),self.uMF.getPeak()) and x >= min(self.lMF.getPeak(),self.uMF.getPeak()):
                return Tuple(min(l,u),1.0)
            else:
                return Tuple(min(l,u),max(l,u))
    
