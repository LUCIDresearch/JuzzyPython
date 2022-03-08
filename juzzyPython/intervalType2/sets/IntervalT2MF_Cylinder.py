"""
IntervalT2MF_Cylinder.py
Created 9/1/2022
"""
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.intervalType2.sets.IntervalT2MF_Prototype import IntervalT2MF_Prototype
from juzzyPython.type1.sets.T1MF_Cylinder import T1MF_Cylinder

class IntervalT2MF_Cylinder(IntervalT2MF_Prototype):
    """
    Class IntervalT2MF_Cylinder
    The class IntervalT2MF_Cylinder represents a membership function which is 
    defined by a single Tuple and can be seen as a cylinder from left to right.
    It does not vary in height/firing strength but its getFS() method will return
    the same FS for all x. (In the literature referred to as cylindrical extension
    of a FS).

    Parameters: 
        primer : Tuple for creating T1MF cylinder MF
        uMF : Upper membership function
        lMF : Lower membership function

    Functions:
        toString
    """
    
    def __init__(self, name: str,primer: Tuple = None,uMF: T1MF_Cylinder = None,lMF: T1MF_Cylinder = None) -> None:
        if uMF != None and lMF != None:
            super().__init__(name,uMF,lMF)
        else:
            super().__init__(name)
            if primer == None:
                raise Exception("IntervalT2MF_Cylinder primer is NONE!")
            if primer.getLeft() > primer.getRight():
                if primer.getLeft()-primer.getRight() < 0.000001:
                    primer.setLeft(primer.getRight())
                else:
                    raise Exception("Lower firing strength ("+primer.getLeft()+") should not be higher than Upper firing strength ("+primer.getRight()+").")
            self.uMF = T1MF_Cylinder(name+"_uMF", primer.getRight())
            self.lMF = T1MF_Cylinder(name+"_lMF", primer.getLeft())
            self.support = Tuple(float("-inf"),float("inf"))

    def toString(self) -> str:
        """Return membership function as string"""
        return "Interval Type-2 Cylindrical Extension of FS: ["+str(self.lMF.getFS(0))+","+str(self.uMF.getFS(0))+"]"