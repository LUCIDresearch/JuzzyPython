"""
GenT2MF_Triangular.py
Created 3/1/2022
"""
import sys
from typing import List
from numpy import number
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from type1.sets.T1MF_Triangular import T1MF_Triangular

class GenT2MF_Triangular(GenT2MF_Prototype):
    """
    Class GenT2MF_Triangular
    Creates a new instance of GenT2zMF_Triangular

    Parameters: 
        primer:
        Creates a new instance of GenT2MFz_Triangular by accepting an Interval Type-2
        Fuzzy Set as primer. The specified number of zLevels are created evenly
        with the Footprint of Uncertainty of the original IT2 set.
        Note that the actual primer will be the first zSlice (at zLevel 
        (1.0 / numberOfzLevels)) and that there will be no zSlice at zLevel 0.
        primer0 primer1:
        Creates a new instance of GenT2MFz_Triangular by taking two interval 
        type-2 sets as first and last slice as inputs. Depending on the numberOfzLevels
        specified, additional zSlices will be created between both initial zSlices.
        primers:
        Creates a new instance of GenT2MFz_Triangular by taking an array of
        interval type-2 triangular membership functions as input.
        The number of zLevels is specified by the length of the primers array.

    Functions:
        None
    
    """

    def __init__(self, name: str,primer: IntervalT2MF_Triangular = None,primer0: IntervalT2MF_Triangular = None, primer1: IntervalT2MF_Triangular = None,primers: List[IntervalT2MF_Triangular] = None, numberOfzLevels: int = None) -> None:
        super().__init__(name)
        self.DEBUG = False
        if primer != None:
            self.numberOfzLevels = numberOfzLevels
            self.support = primer.getSupport()
            self.primer = primer
            slices_fs = [0] * numberOfzLevels
            self.slices_zValues = [0] * numberOfzLevels
            z_stepSize = 1.0/numberOfzLevels
            self.zSlices = [0] * numberOfzLevels
            left_stepsize = ((primer.getLMF().getStart()-primer.getUMF().getStart())/(numberOfzLevels-1))/2.0
            right_stepsize = ((primer.getUMF().getEnd()-primer.getLMF().getEnd())/(numberOfzLevels-1))/2.0

            self.zSlices[0] = IntervalT2MF_Triangular("Slice 0",primer.getUMF(),primer.getLMF())
            inner = [primer.getLMF().getStart(), primer.getLMF().getPeak(), primer.getLMF().getEnd()]
            outer = [primer.getUMF().getStart(), primer.getUMF().getPeak(), primer.getUMF().getEnd()]

            self.slices_zValues[0] = z_stepSize
            if self.DEBUG:
                print(self.zSlices[0].toString()+"  zValue = "+str(self.slices_zValues[0]))
            
            for i in range(1,numberOfzLevels):
                self.slices_zValues[i] = (i+1)*z_stepSize
                inner[0]-=left_stepsize
                inner[2]+=right_stepsize
                outer[0]+=left_stepsize
                outer[2]-=right_stepsize
                if(abs(inner[0]-outer[0])<0.000001):
                    outer[0] = inner[0]
                if(abs(inner[2]-outer[2])<0.000001):
                    outer[2] = inner[2]
                
                self.zSlices[i] = IntervalT2MF_Triangular("Slice_"+str(i),T1MF_Triangular("Slice_"+str(i)+"_UMF", outer[0], outer[1], outer[2]),T1MF_Triangular("Slice_"+str(i)+"_LMF", inner[0], inner[1], inner[2]))

                if self.DEBUG:
                     print(self.zSlices[i].toString()+"  zValue = "+str(self.slices_zValues[i]))

        elif primer0 != None and primer1 != None:
            self.numberOfzLevels = numberOfzLevels
            self.support = primer0.getSupport()
            slices_fs = [0] * numberOfzLevels
            self.slices_zValues = [0] * numberOfzLevels
            z_stepSize = 1.0/numberOfzLevels
            self.zSlices = [0] * numberOfzLevels
            self.zSlices[0] = primer0
            self.slices_zValues[0] = z_stepSize
            self.zSlices[-1] = primer1
            self.slices_zValues[-1] = 1.0
            self.zSlices[-1].setSupport(self.zSlices[0].getSupport())

            lsu = ((primer1.getUMF().getStart()-primer0.getUMF().getStart())/(numberOfzLevels-1.0))
            lsl = ((primer0.getLMF().getStart()-primer1.getLMF().getStart())/(numberOfzLevels-1.0))
            rsu = ((primer0.getUMF().getEnd()-primer1.getUMF().getEnd())/(numberOfzLevels-1.0))
            rsl = ((primer1.getLMF().getEnd()-primer0.getLMF().getEnd())/(numberOfzLevels-1.0))

            inner = [primer0.getLMF().getStart(), primer0.getLMF().getPeak(), primer0.getLMF().getEnd()]
            outer = [primer0.getUMF().getStart(), primer0.getUMF().getPeak(), primer0.getUMF().getEnd()]
            for i in range(1,numberOfzLevels-1):
                self.slices_zValues[i] = (i+1)*z_stepSize
                inner[0]-=lsl
                inner[2]+=rsl
                outer[0]+=lsu
                outer[2]-=rsu
                if self.DEBUG:
                    print(self.getName()+"_zSlice "+str(i)+" , inner: "+str(inner[0])+"  "+str(inner[1])+"  "+str(inner[2])+"   outer: "+str(outer[0])+"  "+str(outer[1])+"  "+str(outer[2]))
                self.zSlices[i] = IntervalT2MF_Triangular(self.getName()+"_zSlice_"+str(i), T1MF_Triangular(self.getName()+"_zSlice_"+str(i)+"_UMF", outer[0], outer[1], outer[2]),T1MF_Triangular(self.getName()+"_zSlice_"+str(i)+"_LMF", inner[0], inner[1], inner[2]))
                self.zSlices[i].setSupport(self.zSlices[0].getSupport())
        elif primers != None:
            self.numberOfzLevels = len(primers)
            self.support = primer[0].getSupport()
            slices_fs = [0] * numberOfzLevels
            self.slices_zValues = [0] * numberOfzLevels
            z_stepSize = 1.0/numberOfzLevels
            self.zSlices = [0] * numberOfzLevels
            self.zSlices = primers.copy()
            for i in range(numberOfzLevels):
                self.slices_zValues[i] = z_stepSize*(i+1)
                self.zSlices[i].setSupport(primers[0].getSupport())

        else:
            raise Exception("Incorrect parameters")