"""
IT2_COSInferenceData.py
Created 13/1/2022
"""
from juzzyPython.generic.Tuple import Tuple
import functools

@functools.total_ordering
class IT2_COSInferenceData():
    """
    Class IT2_COSInferenceData
    Stores Consequent Data in IT2 systems - supports sorting.

    Parameters: 
        f = The firing strength
        c = the centroid value

    Functions:
        getFStrength
        getSelectedCentroidEndpoint
        compareTo
        toString
        __eq__
        __lt__
    """

    def __init__(self,f: Tuple,c: float) -> None:
        self.firingStrength = f
        self.centroidValue = c
    
    def getFStrength(self) -> Tuple:
        """Return the firing strength"""
        return self.firingStrength
    
    def getSelectedCentroidEndpoint(self) -> float:
        """Return the centroid value"""
        return self.centroidValue
    
    def compareTo(self,o: object) -> int:
        """Compare to another COS inference data class"""
        if self.getSelectedCentroidEndpoint() < o.getSelectedCentroidEndpoint():
            return -1
        elif self.getSelectedCentroidEndpoint() > o.getSelectedCentroidEndpoint():
            return 1
        else:
            return 0
    
    def __str__(self) -> str:
        """Return class as string"""
        return "FiringStrength = ["+str(self.firingStrength.getLeft())+","+str(self.firingStrength.getRight())+"   centroidValue = "+str(self.centroidValue)
    
    #Comparable methods
    
    def __eq__(self,other: object):
        return isinstance(other,IT2_COSInferenceData) and self.getSelectedCentroidEndpoint() == other.getSelectedCentroidEndpoint()

    def __lt__(self,other: object):
        return isinstance(other,IT2_COSInferenceData) and self.getSelectedCentroidEndpoint() < other.getSelectedCentroidEndpoint()