
"""
Input.py
Created 18/12/2021
"""

from typing import List
from generic.MF_Interface import MF_Interface
from type1.sets.T1MF_Interface import T1MF_Interface
from type1.sets.T1MF_Singleton import T1MF_Singleton
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Gauangle import T1MF_Gauangle
from type1.sets.T1MF_Triangular import T1MF_Triangular
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
import Tuple

class Input: 
    """
    Class Input: 
    The Input class allows the management and updating of one input, for example
    as part of fuzzy membership functions.

    Parameters:
        name: The name of the input
        domain: the range of the input
        x: Current input value
        inputMF: the input membership object

    Functions: 
        getName
        setName
        getInput
        getDomain
        setDomain
        setInput
        setInputMF
        getInputMF
        toString
      
    """

    def __init__(self,name,domain,x=None,inputMF=None) -> None:
        self.name = name
        self.domain = domain
        if inputMF == None:
            if x != None:
                self.x = x
            else: 
                self.x = 0
            self.inputMF = T1MF_Singleton(x)
        else:
            self.inputMF = inputMF
            self.x = inputMF.getPeak()
        
    def getName(self) -> str:
        return self.name
    
    def setName(self,name) -> None:
        self.name = name
    
    def getInput(self) -> float:
        return self.x
    
    def getDomain(self) -> Tuple:
        return self.domain
    
    def setDomain(self,domain) -> None:
        self.domain = domain
    
    def setInput(self,x) -> None:
        """Set the numeric input value x for this input and change its membership function"""
        if self.domain.contains(x):
            self.x = x
            inMF = self.inputMF
            nameMF = inMF.getName()
            if isinstance(inMF,T1MF_Interface):
                if isinstance(inMF,T1MF_Singleton):
                    self.inputMF = T1MF_Singleton(x)
                elif isinstance(inMF,T1MF_Gaussian):
                    spread = inMF.getSpread()
                    self.inputMF = T1MF_Gaussian(nameMF,x,spread)
                elif isinstance(inMF,T1MF_Gauangle):
                    start = inMF.getStart()
                    end = inMF.getEnd()
                    mean = inMF.getMean()
                    self.inputMF = T1MF_Gauangle(nameMF,start+(x-mean),x,end+(x-mean))
                elif isinstance(inMF,T1MF_Triangular):
                    start = inMF.getStart()
                    end = inMF.getEnd()
                    mean = inMF.getPeak()
                    self.inputMF = T1MF_Triangular(nameMF,start+(x-mean),x,end+(x-mean))
                elif isinstance(inMF,T1MF_Trapezoidal):
                    params = []
                    params.append(inMF.getA())
                    params.append(inMF.getB())
                    params.append(inMF.getC())
                    params.append(inMF.getD())
                    mid = (params[1] + params[2])/2
                    d = x-mid
                    for i in params:
                        i += d
                    self.inputMF = T1MF_Trapezoidal(nameMF,params)
        else:
            raise Exception("The input value "+str(x)+" was rejected "
                    + "as it is outside of the domain for this input: "
                    + "["+str(self.domain.getLeft())+", "+str(self.domain.getRight())+"].")

    def getInputMF(self) -> MF_Interface:
        """Return the input membership function"""
        return self.inputMF
    
    def setInputMF(self,inputMF) -> None:
        """Set a new input membership function"""
        if isinstance(inputMF,T1MF_Interface):
            if self.domain.contains(inputMF.getPeak()):
                self.x = inputMF.getPeak()
                self.inputMF = inputMF
            else:
                raise Exception("The inputMF was rejected "
                    + "as it is outside of the domain for this input: "
                    + "["+str(self.domain.getLeft())+", "+str(self.domain.getRight())+"].")
        else:
            raise Exception("Unsupported InputMF")
        
    def toString(self) -> str:
        """Convert the input to string"""
        return "Input: '"+self.name+"' with value: "+str(self.x)








            
        


