"""
IT2_Antecedent.py
Created 13/1/2022
"""
import sys
from generic.Input import Input
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Gauangle import IntervalT2MF_Gauangle
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from type1.sets.T1MF_Interface import T1MF_Interface


class IT2_Antecedent():
    """
    Class IT2_Antecedent
    Antecedent class for Interval Type-2 FLSs

    Parameters: 
        m = The membership function
        i = The input
        name = Name of antecedent

    Functions:
        getMF
        getFS
        setInput
        getInput
        getSet
        getName
        setName
        getMax
        toString
        compareTo

    """
    
    def __init__(self,m,i,name = None) -> None:
        self.DEBUG = False
        self.mF = m
        self.input = i
        if name != None:
            self.name = name
        else:
            self.name = self.mF.getName()
    
    def getMF(self) -> IntervalT2MF_Interface:
        """Return the membership function"""
        return self.mF
    
    def getFS(self) -> Tuple:
        """Get the firing strength"""
        if self.DEBUG:
            print("Input = "+str(self.input.getInput()))
            print("MF is:  "+str(self.mF.getName()))
            print("Result is: "+self.mF.getFS(input.getInput()).toString())
        return self.mF.getFS(input.getInput())
    
    def setInput(self,input_) -> None:
        """Set the input"""
        self.input = input_
    
    def getInput(self) -> Input:
        """Get the current input"""
        return self.input
    
    def getSet(self) -> IntervalT2MF_Interface:
        """Return the membership function set"""
        return self.mF
    
    def getName(self) -> str:
        """Return the name of the antecedent"""
        return self.name
    
    def setName(self,name) -> None:
        """Set the name of the antecedent"""
        self.name = name

    def getMax(self,tNorm) -> Tuple:
        """Returns the arg sup of the t-norm between the membership function of the antecedent and the 
        membership function of the input (in case of NSF)"""
        xmax = Tuple(0.0,0.0)
        valxmaxl = 0
        valxmaxu = 0
        domain = self.input.getDomain().getRight() - self.input.getDomain().getLeft()
        incr = 1.0/50.0
        x = 0
        templ = 0
        tempu = 0
        if isinstance(self.input.getInputMF(),T1MF_Interface):
            for i in range((domain*50)+1):
                if tNorm == 0:
                    templ = self.input.getInputMF().getFS(x)*self.getMF().getLMF().getFS(x)
                    tempu = self.input.getInputMF().getFS(x)*self.getMF().getUMF().getFS(x)
                else:
                    templ = min(self.input.getInputMF().getFS(x),self.getMF().getLMF().getFS(x))
                    tempu = min(self.input.getInputMF().getFS(x),self.getMF().getUMF().getFS(x))
                if templ >= valxmaxl:
                    valxmaxl = templ
                    xmax.setLeft(x)
                if tempu >= valxmaxu:
                    valxmaxu = tempu
                    xmax.setRight(x)
                x = x + incr
        elif isinstance(self.input.getInputMF(),IntervalT2MF_Interface):
            for i in range((domain*50)+1):
                if tNorm == 0:
                    templ = self.input.getInputMF().getFS(x).getLeft()*self.getMF().getFS(x).getLeft()
                    tempu = self.input.getInputMF().getFS(x).getRight()*self.getMF().getFS(x).getRight()
                else:
                    templ = min(self.input.getInputMF().getFS(x).getLeft(),self.getMF().getFS(x).getLeft())
                    tempu = min(self.input.getInputMF().getFS(x).getRight(),self.getMF().getFS(x).getRight())
                if templ >= valxmaxl:
                    valxmaxl = templ
                    xmax.setLeft(x)
                if tempu >= valxmaxu:
                    valxmaxu = tempu
                    xmax.setRight(x)
                x = x + incr
        return xmax
    
    def toString(self) -> str:
        """Convert the antecedent to string"""
        return "IT2 Antecedent (current input is:"+str(self.getInput().getInput())+"), with MF: "+ str(self.mF)
    
    def compareTo(self,o) -> int:
        """Compare the antecededent mF to another of the same type"""
        if not isinstance(o.getMF(),IntervalT2MF_Interface):
            raise Exception("A Membership function (inplementing T1MF_Interface) object is expected.")
        if isinstance(self.mF,IntervalT2MF_Triangular) and isinstance(o.getMF(),IntervalT2MF_Triangular):
            return self.mF.compareTo(o.getMF())
        elif isinstance(self.mF,IntervalT2MF_Gauangle) and isinstance(o.getMF(),IntervalT2MF_Gauangle):
            return self.mF.compareTo(o.getMF())
        else:
            raise Exception("Antecedent - compareTo has only been implemented for two T1MF_Triangular and T1MF_Gauangle sets.")