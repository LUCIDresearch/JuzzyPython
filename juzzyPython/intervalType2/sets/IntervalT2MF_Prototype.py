"""
IntervalT2MF_Prototype.py
Created 6/1/2022
"""
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.type1.sets.T1MF_Interface import T1MF_Interface
from juzzyPython.intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface

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

    def __init__(self,name,uMF: T1MF_Interface = None, lMF: T1MF_Interface = None) -> None:
        self.name = name
        self.LeftShoulder = False
        self.RightShoulder = False
        self.DEBUG = False
        self.support = None
        if uMF != None and lMF != None:
            self.uMF = uMF
            self.lMF = lMF
            self.support = Tuple(min(uMF.getSupport().getLeft(),lMF.getSupport().getLeft()),max(uMF.getSupport().getRight(),lMF.getSupport().getRight()))
            self.uMF.setSupport(self.support)
            self.lMF.setSupport(self.support)

    def getFS(self,x: float) -> Tuple:
        return Tuple(self.lMF.getFS(x),self.uMF.getFS(x))

    def getPeak(self) -> float:
        if self.uMF.getPeak() == self.lMF.getPeak():
            return self.uMF.getPeak()
        else:
            return (self.uMF.getPeak()+self.lMF.getPeak())/2.0

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getSupport(self) -> Tuple:
        return self.support

    def setSupport(self, support: Tuple) -> None:
        self.support = support

    def setLeftShoulder(self, value: bool) -> None:
        self.LeftShoulder = value

    def setRightShoulder(self, value: bool) -> None:
        self.RightShoulder = value   

    def isLeftShoulder(self) -> bool:
        return self.LeftShoulder

    def isRightShoulder(self) -> bool:
        return self.RightShoulder

    def toString(self) -> str:
        return "Interval Type-2 MF with:\nName: "+self.name+"\nlMF: "+str(self.lMF.toString())+"\nuMF: "+str(self.uMF.toString())+"\nSupport: "+str(self.support.toString())
    
    def compareTo(self,o: object) -> int:
        pass

    def getUpperBound(self,x: float) -> float:
        return self.uMF.getFS(x)
    
    def getLowerBound(self,x: float) -> float:
        return self.lMF.getFS(x)
    
    def getUMF(self) -> T1MF_Interface:
        return self.uMF
    
    def getLMF(self) -> T1MF_Interface:
        return self.lMF

    def getFSAverage(self,x: float) -> float:
        return self.getFS(x).getAverage()
    
    def getCentroid(self,primaryDiscretisationLevel: int) -> Tuple:
        import intervalType2.sets.IntervalT2Engine_Centroid
        iec = intervalType2.sets.IntervalT2Engine_Centroid.IntervalT2Engine_Centroid(primaryDiscretisationLevel)
        return iec.getCentroid(self)