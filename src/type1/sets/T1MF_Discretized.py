
"""
T1MF_Discretized.py
Created 11/12/2021
"""

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype

class T1MF_Discretized(T1MF_Prototype):
    """
    Class T1MF_Discretized
    The class allows the specification of a type-1 MF based on single points alone, 
    i.e. in a discretised fashion. The points are specified using y-x coordinates.
    All points are held in an ArrayList which requires resorting as points are 
    added.

    Parameters: Name: Name of the membership function
    InitialSize: An int defining the size of the array

    Functions:
    """

    def __init__(self, name, initialSize = None, points = None) -> None:
        super().__init__(name)
        self.sorted = False
        self.leftShoulder = False
        self.rightShoulder = False
        self.leftShoulderStart = 0.0
        self.rightShoulderStart = 0.0
        self.DEBUG = False
        self.alphaCutDiscLevel = 60
        self.alphaCutPrecisionLimit = 0.01
        self.support = Tuple()
        self.set = []
        if points != None:
            self.addPoints(points)
            self.sort()
        
    def addPoint(self,p) -> None:
        self.set.append(p)
        self.sorted = False
    
    def addPoints(self,ps) -> None:
        for p in ps:
            self.set.append(p)
        self.sorted = False
            
    def getAlphaCutDiscretizationLevel(self) -> int:
        return self.alphaCutDiscLevel
    
    def setAlphaCutDiscretizationLevel(self,level) -> None:
        self.alphaCutDiscLevel = level
    
    def getNumberOfPoints(self) -> int:
        return len(self.set)
    
    
    

    