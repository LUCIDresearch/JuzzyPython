"""
GenT2Engine_Union.py
Created 7/1/2022
"""
from juzzyPython.generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from juzzyPython.generalType2zSlices.sets.GenT2MF_Union import GenT2MF_Union
from juzzyPython.intervalType2.sets.IntervalT2MF_Union import IntervalT2MF_Union

class GenT2Engine_Union():
    """
    Class GenT2Engine_Union

    Parameters: 
        None

    Functions:
        getUnion
       
    """

    def __init__(self) -> None:
        self.TRADITIONAL = 0
        self.GEOMETRIC = 1
        self.union_method = self.TRADITIONAL
    
    def getUnion(self,a: GenT2MF_Interface,b: GenT2MF_Interface) -> GenT2MF_Interface:
        """Return the union of two sets"""
        if a == None:
            return b
        if b == None:
            return a
        
        if a.getNumberOfSlices() != b.getNumberOfSlices():
            raise Exception("Both sets need to have the same number of slices to calculate their union!")
        
        if self.union_method == self.TRADITIONAL:
            zSlices = [0] * a.getNumberOfSlices()
            for i in range(a.getNumberOfSlices()):
                zSlices[i] = IntervalT2MF_Union(a.getZSlice(i),b.getZSlice(i))
            union = GenT2MF_Union("Union of "+a.getName()+" and "+b.getName(),a.getNumberOfSlices(),a.getZValues(),zSlices)
        else:
            print("Geometric not defined")

        return union