
"""
T1MF_Trapezoidal.py
Created 17/12/2021
"""

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype

class T1MF_Trapezoidal(T1MF_Prototype):
    """
    Class T1MF_Trapezoidal

    Parameters: None

    Functions:
        
    """

    def __init__(self, name,parameters, yLevels = None) -> None:
        super().__init__(name)
        self.lS = None
        self.rS = None
        self.lI = None
        self.rI = None
        self.peak = None
        self.yLevels = [1.0,1.0]
        self.a = parameters[0]
        self.b = parameters[1]
        self.c = parameters[2]
        self.d = parameters[3]
        self.support = Tuple(self.a,self.d)
        if yLevels != None:
            self.yLevels = [yLevels[0],yLevels[1]]
        
    def getFS(self, x) -> float:
        if (self.isLeftShoulder and x <= self.c) or (self.isRightShoulder and x >= self.b):
            return 1.0
        
        if x<self.b and x>self.a:
            out = self.yLevels[0] * (x-self.a)/(self.b-self.a)
        elif x>=self.b and x<=self.c:
            if self.yLevels[0] == self.yLevels[1]:
                out = self.yLevels[0]
            elif self.yLevels[0] < self.yLevels[1]:     
                out = (self.yLevels[1]*x-self.yLevels[0]*x-self.yLevels[1]*self.b+self.yLevels[0]*self.b)/(self.c-self.b)+self.yLevels[0]
            else:
                out = (self.yLevels[1]*x-self.yLevels[0]*x-self.yLevels[1]*self.b+self.yLevels[0]*self.b)/(self.c-self.b)+self.yLevels[0]
            if out<0:
                out = 0
        elif