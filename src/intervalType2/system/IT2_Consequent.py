"""
IT2_Consequent.py
Created 13/1/2022
"""
import sys
from generic.Output import Output
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2Engine_Centroid import IntervalT2Engine_Centroid

class IT2_Consequent():
    """
    Class IT2_Consequent
    Consequent class for type 2 intervals

    Parameters: 
        m = the membership function
        output = the output 
        name = name of consequent
        centroid = replace mF with centroid

    Functions:
        getName
        getOutput
        setOutput
        setName
        getMembershipFunction
        getCentroid
        toString
    
    """

    def __init__(self,m: IntervalT2MF_Interface,output: Output,name: str = None,centroid: Tuple = None) -> None:
        if centroid != None:
            self.centroid = centroid
        else:
            self.mF = m
            if name != None:
                self.name = name
            else:
                self.name = self.mF.getName()
            self.output = output
            self.DEBUG = False
            self.mF.setSupport(Tuple(max(self.mF.getSupport().getLeft(),self.output.getDomain().getLeft()),
            min(self.mF.getSupport().getRight(),self.output.getDomain().getRight())))
            self.IEC = IntervalT2Engine_Centroid()
            self.centroid = self.IEC.getCentroid(m)
            if self.DEBUG:
                print("Centroid values of interval consequent "+self.mF.getName()+" are: "+self.centroid.toString())
    
    def getName(self) -> str:
        return self.name
    
    def getOutput(self) -> Output:
        return self.output
    
    def setName(self,name: str) -> None:
        self.name = name
    
    def getMembershipFunction(self) -> IntervalT2MF_Interface:
        return self.mF
    
    def getCentroid(self) -> Tuple:
        return self.centroid
    
    def toString(self) -> str:
        return "Consequent with MF: "+ self.mF.toString()