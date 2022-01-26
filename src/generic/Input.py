
"""
Input.py
Created 18/12/2021
"""
import sys

from numpy import isin
sys.path.append("..")

from generic.MF_Interface import MF_Interface
from type1.sets.T1MF_Interface import T1MF_Interface
from type1.sets.T1MF_Singleton import T1MF_Singleton
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Gauangle import T1MF_Gauangle
from type1.sets.T1MF_Triangular import T1MF_Triangular
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from intervalType2.sets.IntervalT2MF_Gauangle import IntervalT2MF_Gauangle
from intervalType2.sets.IntervalT2MF_Gaussian import IntervalT2MF_Gaussian
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from intervalType2.sets.IntervalT2MF_Trapezoidal import IntervalT2MF_Trapezoidal
from generic.Tuple import Tuple

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
        """Return the name of the Input"""
        return self.name
    
    def setName(self,name) -> None:
        """Set the name of the input"""
        self.name = name
    
    def getInput(self) -> float:
        """Get the value of the input"""
        return self.x
    
    def getDomain(self) -> Tuple:
        """Get the range of the input"""
        return self.domain
    
    def setDomain(self,domain) -> None:
        """Set the range of the input"""
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
            elif isinstance(inMF,IntervalT2MF_Interface):
                if isinstance(inMF,IntervalT2MF_Gaussian):
                    lmf = inMF.getLMF()
                    namel = lmf.getName()
                    spreadl = lmf.getSpread()
                    umf = inMF.getUMF()
                    nameu = umf.getName()
                    spreadu = umf.getSpread()
                    self.inputMF = IntervalT2MF_Gaussian(nameMF,T1MF_Gaussian(nameu,x,spreadu),T1MF_Gaussian(namel,x,spreadl))
                elif isinstance(inMF,IntervalT2MF_Gauangle):
                    lmf = inMF.getLMF()
                    namel = lmf.getName()
                    startl = lmf.getStart()
                    endl = lmf.getEnd()
                    meanl = lmf.getMean()
                    umf = inMF.getUMF()
                    nameu = umf.getName()
                    startu = umf.getStart()
                    endu = umf.getEnd()
                    meanu = umf.getMean()
                    self.inputMF = IntervalT2MF_Gauangle(nameMF,T1MF_Gauangle(nameu,startu+(x-meanu),x,endu+(x-meanu)),T1MF_Gauangle(namel,startl+(x-meanl),x,endl+(x-meanl)))
                elif isinstance(inMF,IntervalT2MF_Triangular):
                    lmf = inMF.getLMF()
                    namel = lmf.getName()
                    startl = lmf.getStart()
                    endl = lmf.getEnd()
                    meanl = lmf.getPeak()
                    umf = inMF.getUMF()
                    nameu = umf.getName()
                    startu = umf.getStart()
                    endu = umf.getEnd()
                    meanu = umf.getPeak()
                    self.inputMF = IntervalT2MF_Triangular(nameMF,T1MF_Triangular(nameu,startu+(x-meanu),x,endu+(x-meanu)),T1MF_Triangular(namel,startl+(x-meanl),x,endl+(x-meanl)))
                elif isinstance(inMF,IntervalT2MF_Trapezoidal):
                    params = [0] * 4
                    lmf = inMF.getLMF()
                    params[0] = lmf.getA()
                    params[1] = lmf.getB()
                    params[2] = lmf.getC()
                    params[3] = lmf.getD()
                    mid = (params[1]+params[2])/2
                    d = x-mid
                    params[0] = params[0] + d
                    params[1] = params[1] + d
                    params[2] = params[2] + d
                    params[3] = params[3] + d
                    LMF = T1MF_Trapezoidal(lmf.getName(),params)
                    umf = inMF.getUMF()
                    params[0] = umf.getA()
                    params[1] = umf.getB()
                    params[2] = umf.getC() 
                    params[3] = umf.getD()
                    mid = (params[1]+params[2])/2
                    d = x-mid
                    params[0] = params[0] + d
                    params[1] = params[1] + d
                    params[2] = params[2] + d
                    params[3] = params[3] + d
                    UMF = T1MF_Trapezoidal(umf.getName(),params)
                    self.inputMF = IntervalT2MF_Trapezoidal(nameMF,UMF,LMF)

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








            
        


