"""
FLCFactory.py
Created 19/2/2022
"""
import sys

from numpy import zeros_like

sys.path.append("..")

from generic.Input import Input
from generic.Output import Output
from generic.Tuple import Tuple
from intervalType2.system.IT2_Rulebase import IT2_Rulebase
from typing import List, OrderedDict

class FLCFactory():
    """
    Class FLCFactory

    Parameters:
      
    Functions:

    """ 

    def __init__(self,rulebases) -> None:
        self.rulebases = rulebases
        self.weight = 0.0
        self.defaultTypeReduction = 1
        self.numberOfThreads = len(rulebases)
        self.plants = [None] * self.numberOfThreads
        self.zLevels = [0.0] * self.numberOfThreads

        for i in range(self.numberOfThreads):
            self.zLevels[i] = (i+1.0) / self.numberOfThreads
            self.weight += self.zLevels[i]
        
        self.rawReseults = OrderedDict()
        out = self.rulebases[0].getOutputs()
        for o in out:
            
