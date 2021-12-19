
"""
T1_Antecedent.py
Created 18/12/2021
"""

from generic.Input import Input
from type1.sets.T1MF_Gauangle import T1MF_Gauangle
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Interface import T1MF_Interface
from type1.sets.T1MF_Singleton import T1MF_Singleton
from type1.sets.T1MF_Triangular import T1MF_Triangular

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

    def __init__(self,mF,input_,name) -> None:
        if name != None:
            self.name = name
        else:
            self.name = mF.getName()
        self.mF = mF
        self.input = input_
    
    def setMF(self,mF) -> None:
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
    
    def setName(self,name) -> None:
        """Set the name of the antecedent"""
        self.name = name
    
    def getFS(self) -> float:
        """Returns the firing strength for the given antecedent using the current input supplied."""
        return self.mF.getFs(self.input.getInput())

    def getMax(self,tNorm) -> float:
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
    
    def compareTo(self,o) -> int:
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

    def toString(self) -> str:
        """Converts antecedent to string"""
        return "Antecedent (current input is:"+self.getInput().getInput()+"), with MF: "+ self.mF.toString()

