"""
IntervalT2MF_Intersection.py
Created 12/1/2022
"""
import sys
sys.path.append("..")
from intervalType2.sets.IntervalT2MF_Cylinder import IntervalT2MF_Cylinder
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from generic.Tuple import Tuple
from type1.sets.T1MF_Intersection import T1MF_Intersection

class IntervalT2MF_Intersection(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Intersection
    Class that manages the intersection of two interval type-2 MFs.
    The class supports the intersection of other intersections.

    Parameters:
        a = Membership Function T2
        b = Membership Function T2

    Functions:
        getSets
        containsSet
        getFS
        intersectionExists
      
    """

    def __init__(self,a: IntervalT2MF_Interface,b: IntervalT2MF_Interface) -> None:
        #Intersection a and b
        super().__init__("dummy-intersect")#Updated at the end
        self.intersectionExists_ = False # if false, no intersection
        self.sets = set()

        if isinstance(a,IntervalT2MF_Cylinder) or isinstance(b,IntervalT2MF_Cylinder):
            if not (isinstance(a,IntervalT2MF_Cylinder) and a.getUpperBound(0)==0.0) and not(isinstance(b,IntervalT2MF_Cylinder) and b.getUpperBound(0) == 0.0):
                self.intersectionExists_ = True
        elif a.getSupport().getLeft() == b.getSupport().getLeft():
            self.intersectionExists_ = True
        elif a.getSupport().getLeft() < b.getSupport().getLeft():
            if a.getSupport().getRight() >= b.getSupport().getLeft():
                self.intersectionExists_ = True
        elif a.getSupport().getLeft() <= b.getSupport().getRight():
            self.intersectionExists_ = True
        
        if self.intersectionExists_:
            if isinstance(a,IntervalT2MF_Intersection):
                self.sets.update(a.getSets())
            else:
                self.sets.add(a)
            if isinstance(b,IntervalT2MF_Intersection):
                self.sets.update(b.getSets())
            else:
                self.sets.add(b)
            
            self.uMF = T1MF_Intersection("uMF of Intersection of ("+a.getName()+","+b.getName()+")", a.getUMF(),b.getUMF())
            self.lMF = T1MF_Intersection("lMF of Intersection of ("+a.getName()+","+b.getName()+")", a.getLMF(),b.getLMF())
            first = True
            for s in self.sets:
                if first:
                    if s.getSupport() != None and not isinstance(s,IntervalT2MF_Cylinder):
                        self.support = Tuple(s.getSupport().getLeft(),s.getSupport().getRight())
                    name = "Intersection of (" + s.getName()
                    first = False
                else:
                    if not isinstance(s,IntervalT2MF_Cylinder):
                        if self.support == None:
                            self.support = s.getSupport()
                        else:
                            self.support.setLeft(min(self.support.getLeft(),s.getSupport().getLeft()))
                            self.support.setRight(max(self.support.getRight(),s.getSupport().getRight()))
                    name += " and " + s.getName()
            name += ")"
            self.setName(name)
        else:
            self.support = None

    def getSets(self) -> set:
        """Returns the intersection's constituting sets, i.e. all sets which are
        intersected to give rise to this set."""
        return self.sets
    
    def containsSet(self,s: IntervalT2MF_Interface) -> bool:
        """Returns true if the set specified is part of this intersection set."""
        if s in self.sets:
            return True
        else:
            return False
    
    def getFS(self, x: float) -> float:
        """Get the firing strength if there is an intersection"""
        if not self.intersectionExists_:
            return None
        else:
            returnValue = Tuple(1.0,1.0)
            for s in self.sets:
                setFS = s.getFS(x)
                returnValue.setLeft(min(returnValue.getLeft(),setFS.getLeft()))
                returnValue.setRight(min(returnValue.getRight(),setFS.getRight()))
            return returnValue
    
    def intersectionExists(self) -> bool:
        """Return if an intersection exists"""
        return self.intersectionExists_