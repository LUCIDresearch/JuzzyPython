
"""
JaccardSimilarity.py
Created 5/1/2022
"""
import sys

from numpy import isin, number
sys.path.append("..")

from type1.sets.T1MF_Interface import T1MF_Interface
from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
from generic.Tuple import Tuple
from typing import List

class JaccardSimilarity():
    """
    Class JaccardSimilarity
    Implementation of Jaccard Similarity for Type-1, Type-2 and zGT2 Sets

    Parameters: None
    
    Functions:
        getSimilarity
        getDiscretisationValues
    """
    
    def getSimilarity(self,setA,setB,numberOfDiscretisations) -> float:
        """Get the similarity between 2 sets across Type 1 and Type 2 sets"""
        numerator = 0.0
        denomintor = 0.0
        discValues = self.getDiscretisationValues(setA.getSupport(),setB.getSupport(),numberOfDiscretisations)
        if isinstance(setA,T1MF_Interface) and isinstance(setB,T1MF_Interface):
            for i in range(len(discValues)):
                numerator += min(setA.getFS(discValues[i]),setB.getFS(discValues[i]))
                denomintor += max(setA.getFS(discValues[i]),setB.getFS(discValues[i]))
            return numerator/denomintor
        elif isinstance(setA,IntervalT2MF_Interface) and isinstance(setB,IntervalT2MF_Interface):
            for i in range(len(discValues)):
                numerator += min(setA.getUMF().getFS(discValues[i]), setB.getUMF().getFS(discValues[i])) +min(setA.getLMF().getFS(discValues[i]), setB.getLMF().getFS(discValues[i]))
                denomintor += max(setA.getUMF().getFS(discValues[i]), setB.getUMF().getFS(discValues[i])) + max(setA.getLMF().getFS(discValues[i]), setB.getLMF().getFS(discValues[i]))
            return numerator/denomintor
        else:
            raise Exception("Incorrect setA setB types")
    
    def getDiscretisationValues(self,domainSetA,domainSetB,numberOfDiscretisations) -> List[float]:
        """Get the discretisation values across two domains"""
        domain = Tuple(min(domainSetA.getLeft(),domainSetB.getLeft()),max(domainSetA.getRight(),domainSetB.getRight()))
        discStep = domain.getSize()/(numberOfDiscretisations-1)
        discValues = []
        for i in range(numberOfDiscretisations):
            discValues.append(domain.getLeft()+i*discStep)
        return discValues