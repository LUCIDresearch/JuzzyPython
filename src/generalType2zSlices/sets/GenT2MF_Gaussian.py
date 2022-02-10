"""
GenT2MF_Gaussian.py
Created 3/1/2022
"""
from __future__ import annotations

import sys

from numpy import number
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Gaussian import IntervalT2MF_Gaussian
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from typing import List

class GenT2MF_Gaussian(GenT2MF_Prototype):
    """
    Class GenT2MF_Gaussian
    Creates a new instance of GenT2zMF_Gaussian by accepting an Interval Type-2
    Fuzzy Set as primer. The specified number of zLevels are created evenly
    with the Footprint of Uncertainty of the original IT2 set.
    Note that the actual primer will be the first zSlice (at zLevel 
    (1.0 / numberOfzLevels)) and that there will be no zSlice at zLevel 0.

    Parameters: 
        name
        primer
        numberOfzLevels
        primers

    Functions:
        clone
        getZSlice
        setSupport
        
    """

    def __init__(self, name, primer = None,numberOfzLevels = None,primers = None) -> None:
        super().__init__(name)
        self.DEBUG = False
        if primer != None and numberOfzLevels != None:
            self.numberOfzLevels = numberOfzLevels
            self.primer = primer
            self.support = Tuple(primer.getSupport().getLeft(),primer.getSupport().getRight())
            slices_fs = [0] * numberOfzLevels
            slices_zValues = [0] * numberOfzLevels
            z_stepSize = 1.0/numberOfzLevels
            self.zSlices = [0] * numberOfzLevels

            stepsize_spread = ((primer.getUMF().getSpread()-primer.getLMF().getSpread())/(numberOfzLevels-1))/2.0
            stepsize_mean = ((primer.getUMF().getMean()-primer.getLMF().getMean())/(numberOfzLevels-1))/2.0

            inner = [0,0]
            outer = [0,0]
            inner[0] = primer.getLMF().getMean()
            inner[1] = primer.getLMF().getSpread()
            outer[0] = primer.getUMF().getMean()
            outer[1] = primer.getUMF().getSpread()
            self.zSlices[0] = IntervalT2MF_Gaussian(primer.getName()+"_zSlice_0",T1MF_Gaussian(primer.getName()+"_zSlice_0"+"_UMF", outer[0], outer[1]), T1MF_Gaussian(primer.getName()+"_zSlice_0"+"_LMF", inner[0], inner[1]))

            if primer.isLeftShoulder():
                self.zSlices[0].setLeftShoulder(True)
            if primer.isRightShoulder():
                self.zSlices[0].setRightShoulder(True)
            slices_zValues[0] = z_stepSize

            if self.DEBUG:
                print(self.zSlices[0].toString()+"  Z-Value = "+str(slices_zValues[0]))
            
            for i in range(1,numberOfzLevels):
                slices_zValues[i] = (i+1)*z_stepSize
                inner[0] += stepsize_mean
                outer[0] -= stepsize_mean
                inner[1] += stepsize_spread
                outer[1] -= stepsize_spread

                if outer[1]<inner[1]:
                    inner[1] = outer[1]
                if outer[0]<inner[0]:
                    inner[0] = outer[0]
                self.zSlices[i] = IntervalT2MF_Gaussian(primer.getName()+"_zSlice_"+str(i),T1MF_Gaussian(primer.getName()+"_zSlice_"+str(i)+"_UMF", outer[0], outer[1]), T1MF_Gaussian(primer.getName()+"_zSlice_"+str(i)+"_LMF", inner[0], inner[1]))

                if primer.isLeftShoulder():
                    self.zSlices[i].setLeftShoulder(True)
                if primer.isRightShoulder():
                    self.zSlices[i].setRightShoulder(True)
                
                if self.DEBUG:
                    print("zSlice "+i+" is: "+self.zSlices[i].getName()+" its domain is: "+ str(self.zSlices[i].getSupport()))
                    print(self.zSlices[i].toString()+"  zValue = "+str(slices_zValues[i]))
                self.zSlices[i].setSupport(primer.getSupport())
        else:
            self.numberOfzLevels = len(primers)
            self.support = primers[0].getSupport()
            slices_fs = [0] * numberOfzLevels
            slices_zValues = [0] * numberOfzLevels

            self.zSlices = [0] * numberOfzLevels
            z_stepSize = 1.0/numberOfzLevels
            slices_zValues[0] = z_stepSize

            self.zSlices = primers.copy()

            for i in range(numberOfzLevels):
                slices_zValues[i] = z_stepSize*(i+1)
                if self.DEBUG:
                    print(self.zSlices[i].toString()+"  Z-Value = "+str(slices_zValues[i]))
    
    def clone(self) -> GenT2MF_Gaussian:
        """Return a copy of the class"""
        return GenT2MF_Gaussian(self.name,self.primer,self.numberOfzLevels)
    
    def getZSlice(self, slice_number) -> IntervalT2MF_Gaussian:
        """Get the z slice at slice number"""
        return self.zSlices[slice_number]
    
    def setSupport(self, support) -> None:
        """Forces new support over which MF is evaluated"""
        self.support = support
        for i in range(1,self.numberOfzLevels):
            self.zSlices[i].setSupport(self.getSupport())




                



            