"""
GenT2Engine_Defuzzification.py
Created 7/1/2022
"""
import sys

from generic.Output import Output
from generic.Tuple import Tuple
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generalType2zSlices.sets.GenT2MF_Discretized import GenT2MF_Discretized
from intervalType2.sets.IntervalT2Engine_Centroid import IntervalT2Engine_Centroid

from typing import List

class GenT2Engine_Defuzzification():
    """
    Class GenT2Engine_Defuzzification

    Parameters: 
        None

    Functions:
       
    """

    def __init__(self,primaryDiscretizationLevel) -> None:
        self.MINIMUM = 0
        self.PRODUCT = 1
        self.tnorm = self.MINIMUM
        self.DEBUG = False
        self.DEBUG_S = False
        self.IEC = IntervalT2Engine_Centroid(primaryDiscretizationLevel)
    
    def typeReduce(self,s) -> Tuple:
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
    
    def typeReduce_standard(self,s,xRes,yRes) -> float:
        self.dset = GenT2MF_Discretized(s,xRes,yRes)
        self.dPoints_real = [0] * xRes

        temp = [0] * yRes
        for i in range(xRes):
            counter = 0
            for j in range(yRes):
                if self.dset.getSetDataAt(i,j)>0:
                    temp[counter] = Tuple(self.dset.getSetDataAt(i,j),self.dset.getDiscY(j))
                    counter+= 1
            self.dPoints_real[i] = temp.copy()
        
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
        
        wavySlices = [[0]*xRes]*int(numberOfRows)

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

            