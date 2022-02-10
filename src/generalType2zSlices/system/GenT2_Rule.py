"""
GenT2_Rule.py
Created 8/1/2022
"""
import sys
sys.path.append("..")

from generalType2zSlices.system.GenT2Engine_Intersection import GenT2Engine_Intersection
from generalType2zSlices.system.GenT2_Antecedent import GenT2_Antecedent
from generalType2zSlices.system.GenT2_Consequent import GenT2_Consequent

from generic.Input import Input
from generic.Output import Output
from generic.Tuple import Tuple
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generalType2zSlices.sets.GenT2MF_CylExtension import GenT2MF_CylExtension
from generalType2zSlices.sets.GenT2MF_Prototype import GenT2MF_Prototype
from generalType2zSlices.sets.GenT2MF_Intersection import GenT2MF_Intersection

from intervalType2.system.IT2_Rule import IT2_Rule
from intervalType2.system.IT2_Antecedent import IT2_Antecedent
from intervalType2.system.IT2_Consequent import IT2_Consequent
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface

from type1.sets.T1MF_Interface import T1MF_Interface
from type1.sets.T1MF_Meet import T1MF_Meet
from typing import List, OrderedDict

class GenT2_Rule():
    """
    Class GenT2_Rule
    Creates a new instance of GenT2_Rule with a single consequent or multiple.
    Currently only "AND" is supported as logical connective.

    Parameters: 
        antecedents
        consequent
        consequents

    Functions:
        getFS
        getInputs
        getOutput
        getRuleasIT2Rules
        getAntecedents
        getConsequents
        getNumberOfAntecedents
        getNumberOfConsequents
        equals
        toString

    """

    def __init__(self,antecedents,consequent = None, consequents = None) -> None:
        self.antecedents = antecedents
        self.consequents = {}
        self.DEBUG = False
        self.gzEI = GenT2Engine_Intersection()
        if consequent != None:
            self.consequents[consequent.getOutput()] = consequent
        else:
            for i in consequents:
                self.consequents[i.getOutput()] = i
        if self.DEBUG:
            print("Rule antecedent's inputs:")
            for i in range(len(antecedents)):
                print("input: "+antecedents[i].getInput().toString())
        
    def getFS(self) -> T1MF_Interface:
        """Return firing strength of rule"""
        if self.DEBUG:
            for i in range(len(self.antecedents)):
                print(self.antecedents[i].getInput().toString())
        if len(self.antecedents) == 1:
            return self.antecedents[0].getFS()
        else:
            fs = T1MF_Meet(self.antecedents[0].getFS(),self.antecedents[1].getFS())
            if(not fs.intersectionExists()):
                fs = None
            else:
                for i in range(2,len(self.antecedents)):
                    fs = T1MF_Meet(fs,self.antecedents[i].getFS())
            if not fs == None and fs.intersectionExists():
                return fs
            else:
                return None
            
    def getNumberOfAntecedents(self) -> int:
        """Return the number of antecedents"""
        return len(self.antecedents)
    
    def getNumberOfConsequents(self) -> int:
        """Return the number of consequents"""
        return len(self.consequents)
    
    def getAntecedents(self) -> List[GenT2_Antecedent]:
        """Return the list of antecedents"""
        return self.antecedents
    
    def getConsequents(self) -> List[GenT2_Consequent]:
        """Return the list of consequents"""
        return list(self.consequents.values())
    
    def getInputs(self) -> List[Input]:
        """Return the list of inputs"""
        inputs = []
        for i in range(self.getNumberOfAntecedents()):
            inputs.append(self.antecedents[i].getInput())
        return inputs

    def getOutput(self) -> Output:
        """Return the output of the rule"""
        return self.getConsequents()[0].getOutput()
    
    def getRawOutput(self) -> dict:
        """Return the raw output of the rule"""
        returnValue = OrderedDict()
        baseSet = self.getFS()
        for con in self.getConsequents():
            o = con.getOutput()
            if baseSet != None:
                cylExt = GenT2MF_CylExtension(baseSet,self.antecedents[0].getSet().getNumberOfSlices())
                returnValue[o] = self.gzEI.getIntersection(cylExt,con.getSet())
            else:
                returnValue[o] = self.gzEI.getIntersection(cylExt,None)
        return returnValue
    
    def getRuleasIT2Rules(self) -> List[IT2_Rule]:
        """Produces a series of interval type-2 rules where each rule represents one zLevel of the underlying zSlices rule.
        CURRENTLY ONLY ONE CONSEQUENT IS SUPPORTED!"""
        rs = [0] * self.getAntecedents()[0].getSet().getNumberOfSlices()

        for i in range(len(rs)):
            As = [0] * self.getNumberOfAntecedents()
            Cs = [0] * self.getNumberOfConsequents()
            for a in range(len(As)):
                As[a] = self.getAntecedents()[a].getAntecedentasIT2Sets()[i]
                if isinstance(self.getAntecedents()[a].getInput().getInputMF(),GenT2MF_Interface):
                    temp = As[a].getInput()
                    domain = temp.getDomain()
                    nameInput = temp.getName()
                    mf = temp.getInputMF().getZSlice(i)         	
                    As[a].setInput(Input(nameInput, domain, mf))
            c = 0
            for con in self.getConsequents:
                Cs[c] = con.getConsequentsIT2Sets()[i]
                c+=1
            rs[i] = IT2_Rule(As,Cs)
        return rs
    
    def equals(self,rule) -> bool:
        """Check if rule is equal to another"""
        if self == rule:
            return True
        if not isinstance(rule,GenT2_Rule):
            return False
        isEqual = True
        for ants in range(self.getNumberOfAntecedents()):
            temp = False
            for i in range(len(rule.getAntecedents())):
                if self.getAntecedents()[ants].equals(rule.getAntecedents()[i]):
                    temp = True
            isEqual &= temp
        for cons in range(self.getNumberOfConsequents()):
            temp = False
            for i in range(len(rule.getConsequents())):
                if self.getConsequents()[cons].equals(rule.getConsequents()[i]):
                    temp = True
            isEqual &= temp
        return isEqual
    
    def toString(self) -> str:
        """Convert antecedent to string"""
        s="IF ";
        for i in range(self.getNumberOfAntecedents()):
            s+=self.getAntecedents()[i].getName()+" "
            if((i+1)<self.getNumberOfAntecedents()):
                s+="AND "
            else:
                s+="THEN "
        for i in range(self.getNumberOfConsequents()):
            s+= self.getConsequents()[i].getName()+" "
            if((i+1)<self.getNumberOfConsequents()):
                s+="AND "
        return s;
    
        
    
