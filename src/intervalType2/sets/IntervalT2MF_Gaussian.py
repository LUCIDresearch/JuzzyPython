"""
IntervalT2MF_Gaussian.py
Created 10/1/2022
"""
import sys
sys.path.append("..")
import math

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
class IntervalT2MF_Gaussian(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Gaussian
    Interval Type-2 Gaussian Membership Function. Note that uncertain mean is
    supported, however, the mean of the upper MF should be larger than that 
    of the lower MF (otherwise the LMF and UMF will be swapped internally).

    Parameters: 
        uMF = Upper membership function
        lMF = Lower membership function
        
    Functions:
        getUMF
        getLMF
        getFS
        toString
        
    """

    def __init__(self, name, uMF=None, lMF=None) -> None:
        if uMF == None and lMF == None:
            super().__init__(name)
        else:
            super().__init__(name, uMF=uMF, lMF=lMF)
            if uMF.getMean() < lMF.getMean():
                raise Exception("By convention, the mean of the upper membership function should be larger than the mean of the lower membership function.")
            if uMF.getSpread() < lMF.getSpread():
                raise Exception("By convention, the st. dev. (spread) of the upper membership function should be larger than the st. dev. of the lower membership function.")
            self.support = uMF.getSupport()
    
    def getUMF(self) -> T1MF_Gaussian:
        """Return the upper membership function"""
        return self.uMF
    
    def getLMF(self) -> T1MF_Gaussian:
        """Return the lower membership function"""
        return self.lMF
    
    def getFS(self, x) -> float:
        """Return the firing strength of the function """
        if x < self.support.getLeft():
            return Tuple(0.0,0.0)
        if x > self.support.getRight():
            return Tuple(0.0,0.0)
        
        #If means are same
        if self.lMF.getMean() == self.uMF.getMean():
            return Tuple(math.exp(-0.5*math.pow((x-self.lMF.getMean())/self.lMF.getSpread(),2))
            ,math.exp((x-self.uMF.getMean())/self.uMF.getSpread(),2))
        else:
            #with uncertain mean things are a bit more complicated...rely on innerMean being <= outerMean!
            #UPPER
            if x < self.lMF.getMean():
                temp = math.exp(-0.5*math.pow((x-self.lMF.getMean())/self.lMF.getSpread(),2))
            elif x > self.uMF.getMean():
                temp = math.exp(-0.5*math.pow((x-self.uMF.getMean())/self.uMF.getSpread(),2))
            else:
                temp = 1.0
            #LOWER
            if x < (self.lMF.getMean() + self.uMF.getMean())/2:
                temp2 = math.exp(-0.5*math.pow((x-self.uMF.getMean())/self.uMF.getSpread(),2))
            else:
                temp2 = math.exp(-0.5*math.pow((x-self.lMF.getMean())/self.lMF.getSpread(),2))
            
            return Tuple(min(temp,temp2),max(temp,temp2))
    
    def toString(self) -> str:
        """Return the function as a string"""
        return ("Gaussian Interval Type-2 MF: "+self.name+"\nUMF: "+str(self.uMF)+
                "\nLMF: "+str(self.lMF));