"""
GenT2Engine_Defuzzification.py
Created 7/1/2022
"""
from calendar import c
import sys

from generic.Output import Output
from generic.Tuple import Tuple
from type1.sets.T1MF_Discretized import T1MF_Discretized
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generalType2zSlices.sets.GenT2MF_Discretized import GenT2MF_Discretized
from intervalType2.sets.IntervalT2Engine_Centroid import IntervalT2Engine_Centroid

from typing import List

class GenT2Engine_Defuzzification():
    """
    Class GenT2Engine_Defuzzification
    Creates a new instance of GenT2zEngine_Defuzzification 

    Parameters: 
        primaryDiscretizationLevel

    Functions:
        typeReduce
        typeReduce_standard
        printSlices
       
    """

    def __init__(self,primaryDiscretizationLevel) -> None:
        self.MINIMUM = 0
        self.PRODUCT = 1
        self.tnorm = self.MINIMUM
        self.DEBUG = False
        self.DEBUG_S = False
        self.IEC = IntervalT2Engine_Centroid(primaryDiscretizationLevel)
    
    def typeReduce(self,s: GenT2MF_Interface) -> Tuple:
        """Returns a tuple of the type reduced set"""
        if s == None:
            if self.DEBUG:
                print("Set is null at defuzzification stage")
            return None

        dividend_left = 0.0
        divisor_left = 0.0
        dividend_right = 0.0
        divisor_right = 0.0

        for i in range(s.getNumberOfSlices()):
            if s.getZSlice(i) == None:
                if self.DEBUG:
                    print("Slice "+str(i) +" is null")
            else:
                if self.DEBUG:
                    print("Computing centroid "+str(i)+" of "+str(s.getNumberOfSlices()))
                centroid = self.IEC.getCentroid(s.getZSlice(i))
                if self.DEBUG:
                    print("Centroid calculated: "+centroid.toString())

                if centroid != None:
                    dividend_left += centroid.getLeft() * s.getZValue(i)
                    dividend_right += centroid.getRight() * s.getZValue(i)

                    divisor_left += s.getZValue(i)
                    divisor_right += s.getZValue(i)
        
        return Tuple(dividend_left/divisor_left,dividend_right/divisor_right)
    
    def typeReduce_standard(self,s: GenT2MF_Interface,xRes: int,yRes: int) -> float:
        """Returns a typereduced and defuzzified set using the standard general type-2 wavy slice centroid method.
        param set The Type 2 set to type reduce.
        param xResolution Determines how fine the type 2 set should be discretised along the x-axis.
        param yResolution Determines how fine the type 2 set should be discretised along the y-axis."""
        self.dset = GenT2MF_Discretized(s,xRes,yRes)
        self.dPoints_real = [None] * xRes

        temp = [0] * yRes
        for i in range(xRes):
            counter = 0
            for j in range(yRes):
                if self.dset.getSetDataAt(i,j)>0:
                    temp[counter] = Tuple(self.dset.getSetDataAt(i,j),self.dset.getDiscY(j))
                    counter+= 1
            self.dPoints_real[i] = temp[:counter].copy()
        
        if self.DEBUG_S:
            print("No. of vertical slices: "+str(len(self.dPoints_real)))
            print("Vertical slice positions on x axis")
            for i in range(xRes):
                print("Slice "+str(i)+" is at x = "+str(self.dset.getPrimaryDiscretizationValues()[i]))
            print("Actual slices:")
            self.printSlices(self.dPoints_real)
        
        numberOfRows = 0.0
        for i in range(len(self.dPoints_real)):
            if len(self.dPoints_real[i]) != 0:
                if numberOfRows == 0.0:
                    numberOfRows = len(self.dPoints_real[i])
                else:
                    numberOfRows *= len(self.dPoints_real[i])
        
        if self.DEBUG_S:
            print("Final array float is "+str(numberOfRows))
            print("Final array int is "+str(int(numberOfRows)))
        
        if numberOfRows != int(numberOfRows):
            print("precision too great, integer overflow - array length not supported!")
        
        wavySlices = [ [0]*xRes for i in range(int(numberOfRows))]

        for i in range(xRes):
            counter = 0
            for k in range(len(wavySlices)):
                if len(self.dPoints_real[i]) != 0:
                    wavySlices[k][i] = self.dPoints_real[i][counter]
                else:
                    print("Setting wavy slice none")
                    wavySlices[k][i] = None
                
                counter += 1
                if counter == len(self.dPoints_real[i]):
                    counter = 0
        
        if self.DEBUG_S:
            print("Wavy slices:")
            self.printSlices(wavySlices)

        wavycentroids = [0] * int(numberOfRows)
        for i in range(numberOfRows):
            dividend = 0
            divisor = 0
            for j in range(xRes):
                if wavySlices[i][j] == None:
                    if self.DEBUG_S:
                        print("Skip wavy slice, at "+str(i)+" as it is not defined at "+str(j))
                else:
                    dividend += (self.dset.getPrimaryDiscretizationValues()[j]*wavySlices[i][j].getRight())
                    divisor += wavySlices[i][j].getRight()
            if self.DEBUG_S:
                print("wavySlices - Dividend: "+str(dividend)+"  Divisior: "+str(divisor))
            wavycentroids[i] = dividend/divisor
            if self.DEBUG_S:
                print("Centroid of wavyslice "+str(i)+" is: "+str(wavycentroids[i]))
        
        if self.DEBUG_S:
            print("Final type-reduced tuples:")
        min_ = 1.0
        reduced = [0] * int(numberOfRows)

        for i in range(numberOfRows):
            if self.tnorm == self.MINIMUM:
                min_ = 1.0
                for j in range(xRes):
                    if wavySlices[i][j] != None:
                        min_ = min(min_,wavySlices[i][j].getLeft())
            elif self.tnorm == self.PRODUCT:
                min_ = 1.0
                for j in range(xRes):
                    if wavySlices[i][j] != None:
                        min_ *= wavySlices[i][j].getLeft()
            reduced[i] = Tuple(min_,wavycentroids[i])
            if self.DEBUG_S:
                print(reduced[i].toString())
            print(str(reduced[i].getRight())+","+str(reduced[i].getLeft()))
        
        tRset = T1MF_Discretized("output")
        tRset.addPoints(reduced)
        dividend = 0
        divisor = 0

        for i in range(len(reduced)):
            dividend += reduced[i].getLeft()*reduced[i].getRight()
            divisor += reduced[i].getLeft()
        
        if self.DEBUG_S:
            print("Dividend: "+str(dividend)+"  Divisior: "+str(divisor))
        self.crisp_output = dividend/divisor

        return self.crisp_output
    
    def printSlices(self,o: List[object]) -> None:
        """Print the slices in the set"""
        for i in range(len(o)):
            print("Slice "+str(i)+" with length "+str(len(o[i])))
            for j in range(len(o[i])):
                if o[i][j] != None:
                    print("Point "+str(j)+": "+str(o[i][j].getLeft())+"/"+str(o[i][j].getRight())+" ")
                else:
                    print("None")

