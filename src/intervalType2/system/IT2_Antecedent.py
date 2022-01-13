"""
IT2_Antecedent.py
Created 13/1/2022
"""
import sys
from generic.Input import Input
from generic.Output import Output
sys.path.append("..")

from generic.Tuple import Tuple
from intervalType2.sets.IntervalT2MF_Gauangle import IntervalT2MF_Gauangle
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Interface import T1MF_Interface


class IT2_Antecedent():
    """
    Class IT2_Antecedent

    Parameters: 

    Functions:

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
        return self.mF
    
    def getFS(self) -> Tuple:
        if self.DEBUG:
            print("Input = "+str(self.input.getInput()))
            print("MF is:  "+str(self.mF.getName()))
            print("Result is: "+self.mF.getFS(input.getInput()).toString())
        return self.mF.getFS(input.getInput())
    
    def setInput(self,input_) -> None:
        self.input = input_
    
    def getInput(self) -> Input:
        return self.input
    
    def getSet(self) -> IntervalT2MF_Interface:
        return self.mF
    
    def getName(self) -> str:
        return self.name
    
    def setName(self,name) -> None:
        self.name = name

    def getMax(self,tNorm) -> Tuple:
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