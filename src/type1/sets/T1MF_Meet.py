
"""
T1MF_Meet.py
Created 15/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from typing import List

class T1MF_Meet(T1MF_Prototype):
    """
    Class T1MF_Meet
    Meet operation for 2 Type-1 sets, mostly used while computing general Type-2 FLSs.

    Parameters: Name: Name of the membership function
    InitialSize: An int defining the size of the array

    Functions:
        getFS
        intersectionExists
        findMax
        getAlphaCut
        getPeak
        compareTo
    """

    def __init__(self,a,b) -> None:
        super().__init__("T1MF_Meet")
        self.DEBUG = False
        self.resolution = 30
        self.alphaCutDiscLevel = 10000
        self.maxResolution = 10000

        if a == None or b == None:
            self.intersectionExists = False
        else:
            self.intersectionExists = True
            name = a.getName() + " <meet> " + b.getName()
            tempA = self.findMax(a)
            tempB = self.findMax(b)

            self.support = Tuple(min(a.getSupport().getLeft(),b.getSupport().getLeft()),min(a.getSupport))

            if tempA < tempB:
                self.v1 = tempA
                self.v2 = tempB
                self.f1 = a
                self.f2 = b
            else:
                self.v1 = tempB
                self.v2 = tempA
                self.f1 = b
                self.f1 = a
            
            if self.DEBUG:
                print("v1: "+str(self.v1)+" v2:" + str(self.v2))
            
    def getFS(self, x) -> float:
        """Return the maximum FS between two sets"""
        if x < self.v1:
            return max(self.f1.getFS(x),self.f2.getFS(x))
        else:
            if x < self.v2:
                return self.f1.getFS(x)
            else:
                return min(self.f1.getFS(x),self.f2.getFS(x))
    
    def intersectionExists(self) -> bool:
        """Return if an intersection exists between the sets """
        return self.intersectionExists
    
    def findMax(self, s) -> float:
        """Find the max step """
        currentStep = s.getSupport().getLeft()
        stepSize = (s.getSupport().getRight()-s.getSupport.getLeft())/(self.maxResolution-1)
        currentMax = 0
        maxStep = 0

        for i in range(self.maxResolution):
            temp = s.getFS(currentStep)
            if temp == 1:
                return currentStep
            if temp >= currentMax:
                currentMax = temp
                maxStep = currentStep
            currentStep += stepSize
        return maxStep
    
    def getAlphaCut(self, alpha) -> Tuple:
        """Return a new tuple with the alpha cut"""
        stepSize = self.getSupport().getSize()/(self.alphaCutDiscLevel-1.0)
        left = 0.0
        right = 0.0
        
        currentStep = self.getSupport().getLeft()
        for i in range(self.alphaCutDiscLevel):
            temp = abs(self.getFS(currentStep) - alpha)
            if temp < 0.001:
                left = currentStep
                break
            currentStep += stepSize
        
        currentStep = self.getSupport().getRight()
        for i in range(self.alphaCutDiscLevel):
            temp = abs(self.getFS(currentStep) - alpha)
            if temp < 0.001:
                right = currentStep
                break
            currentStep += stepSize

        return Tuple(left,right)
    
    def getPeak(self) -> float:
        """Currently unsupported function"""
        raise Exception("Unsupported Function")

    def compareTo(o) -> int:
        """Currently unsupported function"""
        raise Exception("Unsupported Function")


        