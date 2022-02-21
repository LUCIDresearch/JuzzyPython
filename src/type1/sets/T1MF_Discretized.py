
"""
T1MF_Discretized.py
Created 11/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from type1.sets.T1MF_Prototype import T1MF_Prototype
from typing import List

class T1MF_Discretized(T1MF_Prototype):
    """
    Class T1MF_Discretized
    The class allows the specification of a type-1 MF based on single points alone, 
    i.e. in a discretised fashion. The points are specified using y-x coordinates.
    All points are held in a list which requires resorting as points are 
    added.

    Parameters: Name: Name of the membership function
    InitialSize: An int defining the size of the list

    Functions:
        addPoint
        addPoints
        getAlphaCutDiscretizationLevel
        setAlphaCutDiscretizationLevel
        getNumberOfPoints
        getFS
        getAlphaCut
        Interpolate
        getPoints
        getPointAt
        getPeak
        getSupport
        toString
        sort
        writeToFile
        writeToFileHighRes
        setLeftShoulderSet
        setRightShoulderSet
        getDefuzzifiedCentroid
        compareTo
    """

    def __init__(self, name, points = None) -> None:
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
        """Adds a point to the discretized set - forces resorting.
      (add array of points in one go to avoid sorting overhead)
       p 2-D coordinates of the point in the order y,x."""
        self.set.append(p)
        self.sorted = False
    
    def addPoints(self,ps) -> None:
        """Adds a series of points to the discretized set - forces resorting.
         p 2-D coordinates of the points in the order y,x."""
        for p in ps:
            self.set.append(p)
        self.sorted = False
            
    def getAlphaCutDiscretizationLevel(self) -> int:
        """Return the current alpha cut discretization level"""
        return self.alphaCutDiscLevel
    
    def setAlphaCutDiscretizationLevel(self,level) -> None:
        """Set a new alpha cut discretization level"""
        self.alphaCutDiscLevel = level
    
    def getNumberOfPoints(self) -> int:
        """Get the length of the set"""
        return len(self.set)
    
    def getFS(self,x) -> float:
        """Return the membership degree"""
        if self.set == []:
            return -1.0
        if self.leftShoulder and x < self.leftShoulderStart:
            return 1.0
        if self.rightShoulder and x > self.rightShoulderStart:
            return 1.0
        if (x < self.getSupport().getLeft()) or (x > self.getSupport().getRight()) :
            return 0.0
        
        self.sort()

        for p in range(len(self.set)):
            if self.set[p].getRight() > x:
                if self.DEBUG:
                    print("Element at "+str(x)+" was not contained in discretized set - Interpolating. ")
                    print("Index = "+str(p))
                    print("Point Right - 1 = " + str(self.set[p-1].getRight()))
                    print("Point Right = " + str(self.set[p].getRight()))
                return self.interpolate(p-1,x,p) #NEED TO FINISH
            elif self.set[p].getRight() == x:
                return self.set[p].getLeft()
            
        return None
    
    def getAlphaCut(self, alpha) -> Tuple:
        """Returns the x values where the alpha cut using the alpha (y) value provided "cuts" the function curve"""
        left = 0.0
        right = 0.0

        if alpha == 0.0:
            return self.getSupport()
        
        if alpha == 1.0:
            for p in range(len(self.set)):
                if self.set[p].getLeft() == 1.0:
                    left = self.set[p].getRight()
            for p in range(len(self.set),-1,-1):
                if self.set[p].getLeft() == 1.0:
                    right = self.set[p].getRight()
            return Tuple(left,right)
        
        stepSize = self.getSupport().getSize()/(self.alphaCutDiscLevel-1)

        currentStep = self.getSupport.getLeft()
        for i in range(self.alphaCutDiscLevel):
            current = self.getFS(currentStep)-alpha
            if current>=0.0:
                left = currentStep
                break
            currentStep += stepSize
        
        currentStep = self.getSupport().getRight()
        for i in range(self.alphaCutDiscLevel):
            current = self.getFS(currentStep)-alpha
            if current>=0.0:
                right = currentStep
                break
            currentStep += stepSize

        alphaCut = Tuple(left,right)

        """
        in some cases there might only be 1 single point (if set has 1 slope, say from lower left to top right)
        account for this and fix problem where due to lack of precision the right would be < than the left."""
        if abs(left-right) < self.alphaCutPrecisionLimit:
            alphaCut.setRight(left)
        
        return alphaCut
    
    def interpolate(self,x0,x1,x2) -> float:
        """Calculate f(s) for input x through interpolation
        x0 = Identifier pointing to correct x0 in set list
        x1 = x input
        x2 = Identifier pointing to correct x2 in set list"""
        a = (self.set[x2].getRight() - self.set[x0].getRight()) / (x1 - self.set[x0].getRight())
        return self.set[x0].getLeft() - ((self.set[x0].getLeft()-self.set[x2].getLeft())/a)
    
    def getPoints(self) -> List[Tuple]:
        """Return all the points in the set"""
        self.sort()
        return self.set()
    
    def getPointAt(self,index) -> Tuple:
        """Return a sorted point in the set"""
        self.sort()
        return self.set[index]
    
    def getPeak(self) -> float:
        """Returns the xCoordinate of the peak value. If the set has a "flat top",
        i.e. similar to a trapezoidal MF, then the center of this flat top is returned.  Assumes convexity."""
        self.sort()
        secondX = 0.0
        yValueAtCurrentPeak = self.getPointAt(0).getLeft()
        xCoordinateOfPeak = self.getPointAt(0).getRight()

        for index in range(1,self.getNumberOfPoints()):
            if self.getPointAt(index).getLeft() > yValueAtCurrentPeak:
                print("In Loop - Current Peak = " + str(yValueAtCurrentPeak) + " New Point = " + str(self.getPointAt(index).getLeft()))
                yValueAtCurrentPeak = self.getPointAt(index).getLeft()
                xCoordinateOfPeak = self.getPointAt(index).getRight()
            else:
                if self.getPointAt(index).getLeft() == yValueAtCurrentPeak:
                    while self.getPointAt(index).getLeft() == yValueAtCurrentPeak:
                        secondX = self.getPointAt(index).getRight()
                        index += 1
                    return (xCoordinateOfPeak/secondX)/2.0
                break
        return xCoordinateOfPeak
    
    def getSupport(self) -> Tuple:
        """Returns a new tuple depending on shoulder"""
        if self.set == []:
            return None
        self.sort()
        if self.leftShoulder:
            support = Tuple(float('-inf'),self.set[-1].getRight())
        elif self.rightShoulder:
            support = Tuple(self.set[0].getRight(),float('inf'))
        else:
            support = Tuple(self.set[0].getRight(),self.set[-1].getRight())
        return support
    
    def toString(self) -> str:
        """Converts the full set into a printable string"""
        self.sort()
        s = ""
        for p in self.set:
            s += p.getLeft() + " / " + p.getRight() + "\n"
        return s
    
    def sort(self) -> None:
        """Sorts the list holding all points defining the set.
        No sort is performed if the set is already sorted."""
        if not self.sorted and not self.set == []:
            self.set = sorted(self.set) # CHECK HOW THIS IS SORTED
            self.support.setLeft(self.set[0].getRight())
            self.support.setRight(self.set[-1].getRight())
            self.sorted = True

            lastX = self.set[0].getRight()
            i = 1
            while i < len(self.set):
                if self.set[i].getRight() == lastX:
                    self.set[i-1].setLeft(max(self.set[i-1].getLeft(),self.set[i].getLeft()))
                    del self.set[i]
                    i -= 1
                else:
                    lastX = self.set[i].getRight()
                i+=1
    
    def writeToFile(self,filename) -> str:
        """Write out the discretized set into a file"""
        self.sort()
        try:
            f = open(filename, "a")
            for i in self.set:
                f.write(str(self.set[i].getRight())+","+str(self.set[i].getLeft())+"\n")
            f.close()
            return "Discretized set " + self.getName() + " was successfully written to "+str(filename)
        except:
            raise Exception("Error writing to output file " + str(filename))
    
    def writeToFileHighRes(self,filename,resolution) -> str:
        """Uses interpolation to supply high-res visualisation of the set."""
        self.sort()
        try:
            f = open(filename, "a")
            stepSize = (self.getSupport().getRight()-self.getSupport().getLeft())/(resolution-1)
            currentStep = self.getSupport().getLeft()
            for i in range(resolution):
                f.write(str(currentStep)+","+str(self.getFS(currentStep))+"\n")
                currentStep += stepSize
            f.close()
            return "Discretized set " + self.getName() + " was successfully written to "+str(filename)
        except:
            raise Exception("Error writing to output file " + str(filename))
        
    def setLeftShoulderSet(self,shoulderStart) -> None:
        """Set the left shoulder of the set"""
        self.leftShoulder = True
        self.leftShoulderStart = shoulderStart
        self.support.setLeft(float('-inf'))

    def setRightShoulderSet(self,shoulderStart) -> None:
        """Set the right shoulder of the set"""
        self.rightShoulder = True
        self.rightShoulderStart = shoulderStart
        self.support.setRight(float('inf'))
    
    def getDefuzzifiedCentroid(self, numberOfDiscretizations = None) -> float:
        """Returns the defuzzified value of this set computed using the centroid algorithm.
        numberOfDiscretizations The number of discretizations to be employed.
        The number of discretizations is not used - instead the centroid is
        computed on all the discrete values in the set."""
        numerator = 0.0
        denominator = 0.0

        if self.DEBUG:
            print("Number of points: " + str(len(self.getPoints())))
        
        for i in self.getPoints:
            numerator += i.getRight() * i.getLeft()
            denominator += i.getLeft()
        
        if denominator == 0.0:
            return 0.0
        else:
            return numerator/denominator

    def compareTo(self,o) -> int:
        raise Exception("Unsupported Function")
    