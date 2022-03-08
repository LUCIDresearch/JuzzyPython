
"""
T1_Antecedent.py
Created 18/12/2021
"""

from juzzyPython.generic.Input import Input
from juzzyPython.type1.sets.T1MF_Gauangle import T1MF_Gauangle
from juzzyPython.type1.sets.T1MF_Gaussian import T1MF_Gaussian
from juzzyPython.type1.sets.T1MF_Interface import T1MF_Interface
from juzzyPython.type1.sets.T1MF_Singleton import T1MF_Singleton
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
import functools

@functools.total_ordering
class T1_Antecedent:
    """
    Class T1_Antecedent: 
    Antecedent for a fuzzy rule of a Type-1 Fuzzy System.

    Parameters:
        mF:The actual membership function to associated with this antecedent.
        input_:The input to associate with this antecedent.
        name:Name of the antecedent
        
    Functions: 
        setMF
        getMF
        getInput
        getName
        setName
        getFS
        getMax
        compareTo
        toString
      
    """

    def __init__(self,mF: T1MF_Interface,input_: Input,name: str) -> None:
        if name != None:
            self.name = name
        else:
            self.name = mF.getName()
        self.mF = mF
        self.input = input_
    
    def setMF(self,mF: T1MF_Interface) -> None:
        """Allows changing the membership function defining the antecedent"""
        self.mF = mF
    
    def getMF(self) -> T1MF_Interface:
        """Get the membership function defining the antecedent"""
        return self.mF
    
    def getInput(self) -> Input:
        """Get the input of the antecedent"""
        return self.input
    
    def getName(self) -> str:
        """Get the name of the antecedent"""
        return self.name
    
    def setName(self,name: str) -> None:
        """Set the name of the antecedent"""
        self.name = name
    
    def getFS(self) -> float:
        """Returns the firing strength for the given antecedent using the current input supplied."""
        return self.mF.getFS(self.input.getInput())

    def getMax(self,tNorm: int) -> float:
        """Returns the arg sup of the t-norm between the membership function of the antecedent and the 
        membership function of the input (in case of NSF)"""
        xmax = 0.0
        if isinstance(self.input.getInputMF(),T1MF_Gaussian) and isinstance(self.getMF(),T1MF_Gaussian):
            gaussian = self.input.getInputMF()
            sigmaX = gaussian.getSpread()
            meanX = gaussian.getMean()
            antecedentMF = self.mF
            sigmaF = antecedentMF.getSpread()
            meanF = antecedentMF.getMean()
            if tNorm == 0:
                xmax = (sigmaX*sigmaX*meanF + sigmaF*sigmaF*meanX)/(sigmaX*sigmaX + sigmaF*sigmaF)
            else:
                xmax = (sigmaX*meanF + sigmaF*meanX)/(sigmaX + sigmaF)
        else:
            valxmax = 0
            domain = self.input.getDomain().getRight() - self.input.getDomain().getLeft()
            incr = domain/(domain*50)
            x = 0
            for i in range((domain*50)+1):
                if tNorm == 0:
                    temp = self.input.getInputMF().getFS(x)*self.getMF().getFS(x)
                else:
                    temp = min(self.input.getInputMF().getFS(x),self.getMF().getFS(x))
                
                if temp >= valxmax:
                    valxmax = temp
                    xmax = x
                x += incr
        return xmax
    
    def compareTo(self,o: object) -> int:
        """Allows the comparison of two antecedents, based on their membership functions."""
        if not isinstance(o.getMF(),T1MF_Interface):
            raise Exception("A Membership function (inplementing T1MF_Interface) object is expected.")
        
        if isinstance(self.mF,T1MF_Triangular) and isinstance(o.getMF(),T1MF_Triangular):
            return self.mF.compareTo(o.getMF())
        elif isinstance(self.mF,T1MF_Gauangle) and isinstance(o.getMF(),T1MF_Gauangle):
            return self.mF.compareTo(o.getMF())
        elif isinstance(self.mF,T1MF_Singleton) and isinstance(o.getMF(),T1MF_Singleton):
            return self.mF.compareTo(o.getMF())
        elif isinstance(self.mF,T1MF_Singleton) and isinstance(o.getMF(),T1MF_Triangular):
            return self.mF.compareTo(o.getMF())
        elif isinstance(self.mF,T1MF_Triangular) and isinstance(o.getMF(),T1MF_Singleton):
            return self.mF.compareTo(o.getMF())
        else:
            raise Exception("Antecedent - compareTo has only not been implemented for the provided combination of sets.")

    def __eq__(self, o: object):
        val = self.compareTo(o)
        if val == 0:
            return True
        else:
            return False

    def __lt__(self, o: object):
        val = self.compareTo(o)
        if val == -1:
            return True
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.getName())

    def toString(self) -> str:
        """Converts antecedent to string"""
        return "Antecedent (current input is:"+self.getInput().getInput()+"), with MF: "+ self.mF.toString()

