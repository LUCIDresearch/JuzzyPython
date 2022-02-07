"""
GenT2Engine_Intersection.py
Created 7/1/2022
"""
import sys

from generic.Output import Output
from generic.Tuple import Tuple
sys.path.append("..")

from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generalType2zSlices.sets.GenT2MF_Intersection import GenT2MF_Intersection
from intervalType2.sets.IntervalT2MF_Intersection import IntervalT2MF_Intersection

from typing import List

class GenT2Engine_Intersection():
    """
    Class GenT2Engine_Intersection

    Parameters: 
        None

    Functions:
        getIntersection
       
    """

    def __init__(self) -> None:
        self.TRADITIONAL = 0
        self.GEOMETRIC = 1
        self.intersection_method = self.TRADITIONAL
    
    def getIntersection(self,a,b) -> GenT2MF_Interface:
        """Return the intersection of two sets"""
        if a == None or b == None:
            return None
        
        if a.getNumberOfSlices() != b.getNumberOfSlices():
            raise Exception("Both sets need to have the same number of slices to calculate their Intersection!")
        
        if self.intersection_method == self.TRADITIONAL:
            zSlices = [0] * a.getNumberOfSlices()
            for i in range(a.getNumberOfSlices()):
                zSlices[i] = IntervalT2MF_Intersection(a.getZSlice(i),b.getZSlice(i))
                if not zSlices[i].intersectionExists():
                    zSlices[i] = None
            intersection = GenT2MF_Intersection("Intersection of "+a.getName()+" and "+b.getName(),a.getNumberOfSlices(),a.getZValues(),zSlices)
        else:
            print("Geometric not defined")

        return intersection