"""
GenT2MF_Trapezoidal.py
Created 3/1/2022
"""
from __future__ import annotations
from typing import List
import sys

from numpy import number
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from intervalType2.sets.IntervalT2MF_Trapezoidal import IntervalT2MF_Trapezoidal
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal

class GenT2MF_Trapezoidal(GenT2MF_Prototype):
    """
    Class GenT2MF_Trapezoidal
    Creates a new instance of GenT2zMF_Trapezoidal

    Parameters: 
        primer
        primer0
        primer1
        primers
        numberOfzLevels
   
    Functions:
        getZSlice
 
    """

    def __init__(self, name: str,primer: IntervalT2MF_Trapezoidal = None,primer0: IntervalT2MF_Trapezoidal = None, primer1: IntervalT2MF_Trapezoidal = None,primers: List[IntervalT2MF_Trapezoidal] = None, numberOfzLevels = None) -> None:
        super().__init__(name)
        self.DEBUG = False
        if primer != None:
            stepsize = [0] * 4
            self.numberOfzLevels = numberOfzLevels
            self.support = primer.getSupport()
            self.primer = primer
            slices_fs = [0] * numberOfzLevels
            self.slices_zValues = [0] * numberOfzLevels

            z_stepSize = 1.0/numberOfzLevels
            self.zSlices = [0] * numberOfzLevels
            stepsize[0] = (primer.getLMF().getA() - primer.getUMF().getA())/(numberOfzLevels-1)/2.0
            stepsize[1] = (primer.getLMF().getB() - primer.getUMF().getB())/(numberOfzLevels-1)/2.0
            stepsize[2] = (primer.getUMF().getC() - primer.getLMF().getC())/(numberOfzLevels-1)/2.0
            stepsize[3] = (primer.getUMF().getD() - primer.getLMF().getD())/(numberOfzLevels-1)/2.0

            inner = primer.getLMF().getParameters().copy()
            outer = primer.getUMF().getParameters().copy()

            self.zSlices[0] = IntervalT2MF_Trapezoidal("Slice 0",primer.getUMF(),primer.getLMF())
            self.slices_zValues[0] = z_stepSize
            if self.DEBUG:
                print(self.zSlices[0].toString()+"  Z-Value = "+str(self.slices_zValues[0]))
            
            for i in range(1,numberOfzLevels):
                self.slices_zValues[i] = self.slices_zValues[i-1]+z_stepSize
                inner[0]-=stepsize[0]
                inner[1]-=stepsize[1]
                inner[2]+=stepsize[2]
                inner[3]+=stepsize[3]
                outer[0]+=stepsize[0]
                outer[1]+=stepsize[1]
                outer[2]-=stepsize[2]
                outer[3]-=stepsize[3]

                if(inner[0]<outer[0]): 
                    inner[0] = outer[0]
                if(inner[1]<outer[1]): 
                    inner[1] = outer[1]
                if(inner[2]>outer[2]): 
                    inner[2] = outer[2]
                if(inner[3]>outer[3]): 
                    inner[3] = outer[3]
                
                self.zSlices[i] = IntervalT2MF_Trapezoidal("Slice "+i, T1MF_Trapezoidal("upper_slice "+i,outer),T1MF_Trapezoidal("lower_slice "+i,inner))

                if self.DEBUG:
                    print(self.zSlices[i].toString()+"  Z-Value = "+str(self.slices_zValues[i]))
                
        elif primer0 != None and primer1 != None:
            if self.DEBUG:
                print("Number of zLevels: "+str(numberOfzLevels))
            
            self.numberOfzLevels = numberOfzLevels
            self.support = primer0.getSupport()
            slices_fs = [0] * numberOfzLevels
            self.slices_zValues = [0] * numberOfzLevels
            self.zSlices = [0] * numberOfzLevels

            self.zSlices[0] = primer0
            self.zSlices[0].setName(self.getName()+"_Slice_0")
            self.zSlices[-1] = primer1

            z_stepSize = 1.0/(numberOfzLevels)
            self.slices_zValues[0] = z_stepSize
            self.slices_zValues[-1] = 1.0

            lsu = (primer1.getUMF().getParameters()[0]-primer0.getUMF().getParameters()[0])/(numberOfzLevels-1)
            lsl = (primer0.getLMF().getParameters()[0]-primer1.getLMF().getParameters()[0])/(numberOfzLevels-1)

            rsu = (primer0.getUMF().getParameters()[3]-primer1.getUMF().getParameters()[3])/(numberOfzLevels-1)
            rsl = (primer1.getLMF().getParameters()[3]-primer0.getLMF().getParameters()[3])/(numberOfzLevels-1)

            if self.DEBUG:
                print("lsu = "+str(lsu)+"  lsl = "+str(lsl)+"  rsu = "+str(rsu)+"  rsl = "+str(rsl))
            
            inner = primer0.getLMF().getParameters().copy()
            outer = primer0.getUMF().getParameters().copy()

            for i in range(1,numberOfzLevels-1):
                self.slices_zValues[i] = self.slices_zValues[i-1]+z_stepSize
                inner[0]-=lsl
                inner[3]+=rsl
                outer[0]+=lsu
                outer[3]-=rsu

                if self.DEBUG:
                    print("Slice "+str(i)+" , inner: "+str(inner[0])+"  "+str(inner[1])+"  "+str(inner[2])+"   outer: "+str(outer[0])+"  "+str(outer[1])+"  "+str(outer[2]))
                self.zSlices[i] = IntervalT2MF_Trapezoidal(self.getName()+"_Slice_"+str(i),T1MF_Trapezoidal("upper_slice "+i,outer),T1MF_Trapezoidal("lower_slice "+i,inner))

                if self.DEBUG:
                    print(self.zSlices[i].toString()+"  Z-Value = "+str(self.slices_zValues[i]))

        elif primers != None:
            self.numberOfzLevels = len(primers)
            self.support = primers[0].getSupport()

            slices_fs = [0] * self.numberOfzLevels
            self.slices_zValues = [0] * self.numberOfzLevels
            z_stepSize = 1.0/self.numberOfzLevels
            self.slices_zValues[0] = z_stepSize
            self.zSlices = primers.copy()

            for i in range(self.numberOfzLevels):
                self.slices_zValues[i] = z_stepSize*(i+1)
                if self.DEBUG:
                    print(self.zSlices[i].toString()+"  Z-Value = "+str(self.slices_zValues[i]))


    def clone(self) -> GenT2MF_Trapezoidal:
        """Not implemented"""
        print("Not implemented")
        return None
    
    def getZSlice(self, slice_number: int) -> IntervalT2MF_Trapezoidal:
        """Return the slice number"""
        return self.zSlices[slice_number]

    def getLeftShoulderStart(self) -> float:
        """Not implemented"""
        print("Not implemented")
        return float("Nan")
    
    def getRightShoulderStart(self) -> float:
        """Not implemented"""
        print("Not implemented")
        return float("Nan")
    
