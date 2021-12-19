
"""
T1_Consequent.py
Created 18/12/2021
"""

from generic.Output import Output
from type1.sets.T1MF_Interface import T1MF_Interface

class T1_Consequent:
    """
    Class T1_Consequent: 
    Consequent for a fuzzy rule of a Type-1 Fuzzy System.

    Parameters:
        mF: The membership function defining the consequent
        output: The output of the consequent
        name: The name of the consequent
        
    Functions: 
        setMF
        getMF
        getOutput
        setOutput
        getName
        setName
        toString
      
    """

    def __init__(self,mF,output,name = None) -> None:
        if name != None:
            self.name = name
        else:
            self.name = mF.getName()
        self.mF = mF
        self.output = output

    def setMF(self,mF) -> None:
        """Set the membership function for the consequent"""
        self.mF = mF
    
    def getMF(self) -> T1MF_Interface:
        """Get the membership function for the consequent"""
        return self.mF
    
    def getOutput(self) -> Output:
        """Get the output for the consequent"""
        return self.output
    
    def setOutput(self,out) -> None:
        """Set the output for the consequent"""
        self.output = out
    
    def getName(self) -> str:
        """Get the name of the consequent"""
        return self.name
    
    def setName(self,name) -> None:
        """Set the name of the consequent"""
        self.name = name
    
    def toString(self) -> str:
        """Convert the consequent to a string"""
        return "Consequent with MF: "+ self.mF.toString()
    
