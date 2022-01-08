"""
IntervalT2MF_Prototype.py
Created 6/1/2022
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Interface import T1MF_Interface
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2Engine_Centroid import IntervalT2Engine_Centroid

class IntervalT2MF_Prototype(IntervalT2MF_Interface):
    """
    Class IntervalT2MF_Prototype

    Parameters: None

    Functions:
        getFS
        getPeak
        getName
        setName
        getSupport
        setSupport
        setLeftShoulder
        setRightShoulder
        isLeftShoulder
        isRightShoulder
        toString
        compareTo
        getLowerBound
        getUpperBound
        getCentroid
        getUMF
        getLMF
        getFSAverage
       
    """

    def __init__(self,name,uMF = None, lMF = None) -> None:
        self.name = name
        self.LeftShoulder = False
        self.RightShoulder = False
        self.DEBUG = False
        if uMF != None and lMF != None:
            self.uMF = uMF
            self.lMF = lMF
            self.support = Tuple(min(uMF.getSupport().getLeft(),lMF.getSupport().getLeft()),max(uMF.getSupport().getRight(),lMF.getSupport().getRight()))
            self.uMF.setSupport(self.support)
            self.lMF.setSupport(self.support)

    def getFS(self,x) -> float:
        return Tuple(self.lMF.getFS(x),self.uMF.getFS(x))

    def getPeak(self) -> float:
        if self.uMF.getPeak() == self.lMF.getPeak():
            return self.uMF.getPeak()
        else:
            return (self.uMF.getPeak()+self.lMF.getPeak())/2.0

    def getName(self) -> str:
        return self.name

    def setName(self, name) -> None:
        self.name = name

    def getSupport(self) -> Tuple:
        return self.support

    def setSupport(self, support) -> None:
        self.support = support

    def setLeftShoulder(self, value) -> None:
        self.LeftShoulder = value

    def setRightShoulder(self, value) -> None:
        self.RightShoulder = value   

    def isLeftShoulder(self) -> bool:
        return self.LeftShoulder

    def isRightShoulder(self) -> bool:
        return self.RightShoulder

    def toString(self) -> str:
        return "Interval Type-2 MF with:\nName: "+self.name+"\nlMF: "+str(self.lMF)+"\nuMF: "+str(self.uMF)+"\nSupport: "+str(self.support)
    
    def compareTo(self,o) -> int:
        pass

    def getUpperBound(self,x) -> float:
        return self.uMF.getFS(x)
    
    def getLowerBound(self,x) -> float:
        return self.lMF.getFS(x)
    
    def getUMF(self) -> T1MF_Interface:
        return self.uMF
    
    def getLMF(self) -> T1MF_Interface:
        return self.lMF

    def getFSAverage(self,x) -> float:
        return self.getFS(x).getAverage()
    
    def getCentroid(self,primaryDiscretisationLevel) -> Tuple:
        iec = IntervalT2Engine_Centroid(primaryDiscretisationLevel)
        return iec.getCentroid(self)