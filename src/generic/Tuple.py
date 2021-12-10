
"""
Tuple.py
Created 10/12/2021
"""
from __future__ import annotations

class Tuple:
    """
    Class Tuple: 
    Creates an object of two values related in some way, such as range.
    The left and right values are placed into a list

    Parameters:
        l = The left value in (float) (Optional)
        r = The right value in (float) (Optional)
    
    Functions: 
        clone
        setLeft 
        setRight 
        setEqual 
        getLeft 
        getRight 
        getAverage 
        contains 
        getSize 
        toString 
        add 
        compareTo 
    """

    def __init__(self,l = None,r = None) -> None:
        self.tuple = [0.0,0.0]
        if l != None and r != None:
            self.tuple[0] = l
            self.tuple[1] = r

    def clone(self) -> Tuple:
        """Creates a duplicate copy of the tuple object"""
        return Tuple(self.getLeft(),self.getRight())
    
    def setLeft(self,l) -> None:
        """Set the left value"""
        self.tuple[0] = l
    
    def setRight(self,r) -> None:
        """Set the right value"""
        self.tuple[1] = r
    
    def setEqual(self,t) -> None:
        """Copy a tuple into the current object"""
        self.tuple[0] = t.getLeft()
        self.tuple[1] = t.getRight()
    
    def getLeft(self) -> float:
        """Return the left value"""
        return self.tuple[0]

    def getRight(self) -> float:
        """Return the right value"""
        return self.tuple[1]
    
    def getAverage(self) -> float:
        """Return the average of left and right"""
        return (sum(self.tuple))/2.0
    
    def contains(self,x) -> bool:
        """Returns true if the parameter falls within the interval defined by the Tuple"""
        return (x >= self.getLeft() and x <= self.getRight())

    def getSize(self) -> float:
        """Returns the difference of the right vs left values"""
        return self.getRight() - self.getLeft()
    
    def toString(self) -> str:
        """Returns a string of the current tuple"""
        return "left = "+str(self.getLeft())+" and right = "+str(self.getRight())
    
    def add(self,x) -> Tuple:
        """Add the values of another tuple onto the current one"""
        return Tuple(self.getLeft()+x.getLeft(),self.getRight()+x.getRight())
    
    def compareTo(self,o) -> int:
        """Compare tuple values of another object and return an int"""
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



