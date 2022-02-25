"""
GenT2MF_Discretized.py
Created 2/1/2022
"""
import sys
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from type1.sets.T1MF_Discretized import T1MF_Discretized
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from typing import List

class GenT2MF_Discretized(GenT2MF_Prototype):
    """
    Class GenT2MF_Discretized
    Creates a new instance of GenT2Discretized by setting up a new
    two-dimensional array using the dimensions provided
    and "filling" with a discretized version of the set provided.

    Parameters: 
        gt2set : Gen 2 Interface
        primaryDiscretizationLevel: The level/number of discretisations performed on the primary/x axis.
        secondaryDiscretizationLevel:  The level/number of discretisations performed on the secondary/y axis

    Functions:
        getPrimaryDiscretizationlevel
        getSetDataAt
        getDiscX
        getDiscY
        getSecondaryDiscretizationLevel
        getPrimaryDiscretizationValues
        getSecondaryDiscretizationValues

    """

    def __init__(self,gt2set: GenT2MF_Interface,primaryDiscretizationLevel: int,secondaryDiscretizationLevel: int = None) -> None:
        super().__init__("GenT2zMF_Discretized")
        self.support = gt2set.getSupport().clone()
        self.precision = 0.000001
        self.DEBUG = False
        self.xDiscretizationValues = [0] * primaryDiscretizationLevel
        self.name = "Discretized version of "+gt2set.getName()
        if secondaryDiscretizationLevel == None:
            self.xDiscretizationLevel = primaryDiscretizationLevel
            xStep = gt2set.getSupport().getLeft()
            stepsize = (gt2set.getSupport().getRight()-gt2set.getSupport().getLeft())/(primaryDiscretizationLevel-1)
            self.vSlices = [0] * primaryDiscretizationLevel
            for i in range(primaryDiscretizationLevel):
                self.xDiscretizationValues[i] = xStep
                self.vSlices[i] = gt2set.getFS(xStep)
                if self.DEBUG:
                    if self.vSlices[i] != None:
                        print("vSlice number: "+str(i)+" = \n"+self.vSlices[i].toString())
                    else:
                        print("vSlice number: "+str(i)+" = null")
                xStep+=stepsize
        else:
            self.set = [[0]*secondaryDiscretizationLevel]*primaryDiscretizationLevel
            self.yDiscretizationValues = [0]*secondaryDiscretizationLevel
            primStepsize = (self.getSupport().getRight()-self.getSupport().getLeft())/(primaryDiscretizationLevel-1)
            secStepsize = 1.0/(secondaryDiscretizationLevel-1)
            xStep = self.getSupport().getLeft()
            yStep = 0
            for i in range(primaryDiscretizationLevel):
                yStep = 0
                self.xDiscretizationValues[i] = xStep
                if self.DEBUG:
                    print("In iteration "+str(i)+" xStep = "+str(xStep))
                t1set_temp = gt2set.getFS(xStep)
                if t1set_temp != None:
                    for j in range(secondaryDiscretizationLevel):
                        self.yDiscretizationValues[j] = yStep
                        self.set[i][j] = t1set_temp.getFS(yStep)
                        yStep += secStepsize
                xStep += primStepsize

    def getPrimaryDiscretizationLevel(self) -> int:
        """Return the primary discretization level"""
        return self.xDiscretizationLevel
    
    def getSetDataAt(self,x: int,y: int) -> float:
        """Returns third dimension membership for given array coordinates. (Use
        getDiscX() and getDiscY() to get discretization level at pointer location.)
        A filter is applied which returns 0 for any values smaller than the specified
        precision within the class (usually 0.000001)"""
        if self.set[x][y] > self.precision:
            return self.set[x][y]
        else:
            return 0

    def getDiscX(self,x: int) -> float:
        """Returns discretization value at the specified level on the x Axis."""
        return self.xDiscretizationValues[x]
    
    def getDiscY(self,y: int) -> float:
        """Returns discretization value at the specified level on the y Axis."""
        return self.yDiscretizationValues[y]
    
    def getSecondaryDiscretizationLevel(self) -> int:
        """Return the level if secondary discretization"""
        return len(self.yDiscretizationValues)
    
    def getPrimaryDiscretizationValues(self) -> List[float]:
        """Return list of primary discretization values"""
        return self.xDiscretizationValues
    
    def getSecondaryDiscretizationValues(self) -> List[float]:
        """Return list of secondary discretization values"""
        return self.yDiscretizationValues

            