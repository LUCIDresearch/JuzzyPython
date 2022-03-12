"""
FLCPlant.py
Created 19/2/2022
"""
from juzzyPython.intervalType2.system.IT2_Rulebase import IT2_Rulebase

class FLCPlant():
    """
    Class FLCPlant
    Runs a single IT2 Rulebase

    Parameters:
        rulebase: Single IT2 rulebase
        results: Results dict
        positionPointer: Int
        typeReductionType: Int
        lock: Multiprocessing lock
      
    Functions:
        getTypeReductionType
        setTypeReductionType
        run
    """ 

    def __init__(self,rulebase: IT2_Rulebase,positionPointer: int,typeReductionType: int,lock) -> None:
        self.rulebase = rulebase
        self.typeReductionType = typeReductionType
        self.positionPointer = positionPointer
        self.lock = lock #Currently unused... may come into effect.
    
    def getTypeReductionType(self) -> int:
        """Return the type reduction type"""
        return self.typeReductionType
    
    def setTypeReductionType(self,type: int) -> None:
        """Set the type reduction type"""
        self.typeReductionType = type
    
    def run(self,results: dict) -> None:
        """Run an IT2 rulebase"""
        out = self.rulebase.getOutputs()
        temp = self.rulebase.evaluateGetCentroid(self.typeReductionType)
        for o in out:
            #This variable exchange seems redundant, however is required for the dict proxy to update
            change = results[o]
            new = temp[o][0]
            change[0][self.positionPointer]= new 
            results[o] = change

