from __future__ import annotations

class Tuple:
    """
    Created 10/12/2021

    Class Tuple: 
    Creates an object of two values related in some way, such as range.
    The left and right values are placed into a list

    Parameters:
        l = The left value in float
        r = The right value in float
    
    Functions: 
        clone = Creates a duplicate copy of the tuple object
        setLeft = Set the left value
        setRight = Set the right value 
        setEqual = Copy a tuple into the current object
        getLeft = Return the left value
        getRight = Return the right value
        getAverage = Return the average of left and right
        contains = Returns true if the parameter falls within the interval defined by the Tuple
        getSize = Returns the difference of the right vs left values
        toString = Returns a string of the current tuple
        add = Add the values of another tuple onto the current one
        compareTo = Compare tuple values of another object and return an int
    """

    def __init__(self,l = None,r = None) -> None:
        self.tuple = [0.0,0.0]
        if l != None and r != None:
            self.tuple[0] = l
            self.tuple[1] = r

    def clone(self) -> Tuple:
        return Tuple(self.getLeft(),self.getRight())
    
    def setLeft(self,l) -> None:
        self.tuple[0] = l
    
    def setRight(self,r) -> None:
        self.tuple[1] = r
    
    def setEqual(self,t) -> None:
        self.tuple[0] = t.getLeft()
        self.tuple[1] = t.getRight()
    
    def getLeft(self) -> float:
        return self.tuple[0]

    def getRight(self) -> float:
        return self.tuple[1]
    
    def getAverage(self) -> float:
        return (sum(self.tuple))/2.0
    
    def contains(self,x) -> bool:
        return (x >= self.getLeft() and x <= self.getRight())

    def getSize(self) -> float:
        return self.getRight() - self.getLeft()
    
    def toString(self) -> str:
        return "left = "+str(self.getLeft())+" and right = "+str(self.getRight())
    
    def add(self,x) -> Tuple:
        return Tuple(self.getLeft()+x.getLeft(),self.getRight()+x.getRight())
    
    def compareTo(self,o) -> int:
        if self.getRight() < o.getRight():
            return -1
        elif self.getRight() > o.getRight():
            return 1
        elif self.getLeft() < o.getLeft():
            return -1
        elif self.getLeft() > o.getLeft():
            return 1
        else:
            return 0



