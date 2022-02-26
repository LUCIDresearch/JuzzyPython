"""
GenT2MF_Prototype.py
Created 31/1/2022
"""
import sys
sys.path.append("..")

from generic.MF_Interface import MF_Interface
from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from type1.sets.T1MF_Discretized import T1MF_Discretized
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from typing import List

class GenT2MF_Prototype(GenT2MF_Interface):
    """
    Class GenT2MF_Prototype
    Prototype class for zSlices based general type-2 fuzzy sets. This class should
    not be instantiated directly but extended by the specific fuzzy set classes
    such as triangular, Gaussian, etc.

    Parameters: None

    Functions:
        getName
        setName
        getNumberOfSlices
        getFS
        getZSlice
        setZSlice
        getZValue
        getSupport
        setSupport
        getFSWeightedAverage
        isLeftShoulder
        isRightShoulder
        getZValues
        getCentroid
        getPeak
        toString
        setZValues
  
       
    """

    def __init__(self,name: str) -> None:
        self.name = name
        self.isLeftShoulder_ = False
        self.isRightShoulder_ = False
        self.DEBUG = False

    def setLeftShoulder(self,isLeftShoulder: bool):
        """Set the left shoulder"""
        self.isLeftShoulder_ = isLeftShoulder
    
    def setRightShoulder(self,isRightShoulder: bool):
        """Set the right shoulder"""
        self.isRightShoulder_ = isRightShoulder

    def getFS(self,x: float) -> T1MF_Discretized:
        """Return the firing strength"""
        slice_ = T1MF_Discretized("VerticalSlice_at"+str(x)+"_of_"+self.getName())

        for i in range(self.numberOfzLevels):
            temp = self.getZSlice(i).getFS(x)
            if self.DEBUG:
                print("On slice "+i+" with x = "+x+", getFS() returns: "+temp)
                print("Adding Tuple: "+Tuple(self.getZValue(i),temp.getLeft()).toString())
                print("Adding Tuple: "+Tuple(self.getZValue(i),temp.getRight()).toString())
            slice_.addPoint(Tuple(self.getZValue(i),temp.getLeft()))
            slice_.addPoint(Tuple(self.getZValue(i),temp.getRight()))
        if slice_.getNumberOfPoints()>0:
            return slice_
        return None

    def getPeak(self) -> float:
        """Average of the peaks of each slice"""
        average = 0
        for i in range(self.getNumberOfSlices()):
            average += self.getZSlice(i).getPeak()
        average = average/self.getNumberOfSlices()
        return average

    def getName(self) -> str:
        """Return the name"""
        return self.name

    def setName(self, name: str) -> None:
        """Set the name"""
        self.name = name

    def getSupport(self) -> Tuple:
        """Get the support Tuple"""
        return self.support

    def setSupport(self, support: Tuple) -> None:
        """Set the support tuple"""
        self.support = support

    def isLeftShoulder(self) -> bool:
        """Check left shoulder"""
        return self.isLeftShoulder_

    def isRightShoulder(self) -> bool:
        """Check right shoulder"""
        return self.isRightShoulder_

    def toString(self) -> str:
        """Convert class to string"""
        s = "zMF(noSlices:"+str(self.getNumberOfSlices())+"):["
        for i in range (self.getNumberOfSlices()):
            s+= str(self.getZSlice(i))
        s+="]\n"
        return s
    
    def getFSWeightedAverage(self,x: float) -> float:
        """Returns the weighted average of the firing strength of the zSlices of this
        set. Employed for example in order to compare the firing strength for a
        given input of mutliple zSlices based general type-2 fuzzy sets."""
        numerator = 0.0
        denominator = 0.0
        for i in range(self.getNumberOfSlices()):
            numerator += self.getZSlice(i).getFSAverage(x)*self.getZValue(i)
            denominator += self.getZValue(i)
        return numerator/denominator
    
    def getCentroid(self,primaryDiscretisationLevel: int) -> T1MF_Discretized:
        """Get the discretized T1 MF function"""
        slice_ = T1MF_Discretized("Centroid of"+self.getName(), self.numberOfzLevels)

        for i in range(self.numberOfzLevels):
            temp = self.getZSlice(i).getCentroid(primaryDiscretisationLevel)
            if self.DEBUG:
                print("On slice number"+i+" ("+self.getZSlice(i).getName()+") with primaryDiscretizationLevel = "+ str(primaryDiscretisationLevel)+" getCentroid() returns: "+temp)
            slice_.addPoint(Tuple(self.getZValue(i),temp.getLeft()))
            slice_.addPoint(Tuple(self.getZValue(i),temp.getRight()))
        if slice_.getNumberOfPoints()>0:
            return slice_
        return None
    
    def getZValues(self) -> List[float]:
        """Get all z values"""
        try:
            return self.slices_zValues
        except:
            self.setZValues()
            return self.slices_zValues

    def setZValues(self):
        """Set new z values"""
        stepSize = 1.0/self.getNumberOfSlices()
        firstStep = stepSize
        self.slices_zValues = [0.0] * self.getNumberOfSlices()
        for i in range(len(self.slices_zValues)):
            self.slices_zValues[i] = firstStep+i*stepSize
    
    def getZValue(self,slice_number: int) -> float:
        """Return a specific slice """
        if slice_number >= self.getNumberOfSlices():
            raise Exception("The zSlice reference "+str(slice_number)+" is invalid as the set has only "+str(self.getNumberOfSlices())+" zSlices.")
        try:
            return self.slices_zValues[slice_number] 
        except:
            self.setZValues()
            return self.slices_zValues[slice_number] 

    def setZSlice(self,zSlice: IntervalT2MF_Interface,zLevel: int) -> None:
        """Method to set or swap a specific zSlice. The method replaces a specific 
        zSlice with the given zSlice respectively IT2 set. Note that currently
        NO checks whether a 
        provided zSlices results in the violation of the general type-2 fuzzy set
        restrictions are done - no exceptions are thrown!"""
        self.zSlices[zLevel] = zSlice

    def getZSlice(self,slice_number: int) -> IntervalT2MF_Interface:
        """Get a specific z slice"""
        if slice_number >= self.getNumberOfSlices():
            raise Exception("The zSlice reference "+str(slice_number)+" is invalid as the set has only "+str(self.getNumberOfSlices())+" zSlices.")
        return self.zSlices[slice_number]

    def getNumberOfSlices(self) -> int:
        """Total number of slices"""
        return self.numberOfzLevels

    