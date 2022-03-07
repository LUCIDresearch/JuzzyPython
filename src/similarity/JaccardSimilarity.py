
"""
JaccardSimilarity.py
Created 5/1/2022
"""
import sys
from generalType2zSlices.sets.GenT2MF_Interface import GenT2MF_Interface
from generic.MF_Interface import MF_Interface

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
    
    def getSimilarity(self,setA: MF_Interface,setB: MF_Interface,numberOfDiscretisations: int) -> float:
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
        elif isinstance(setA,GenT2MF_Interface) and isinstance(setB,GenT2MF_Interface):
            numeratorArray = [0] * setA.getNumberOfSlices()
            denominatorArray = [0] * setA.getNumberOfSlices()
            for i in range(len(discValues)):
                for z in range(setA.getNumberOfSlices()):
                    numeratorArray[z] += min(setA.getZSlice(z).getUMF().getFS(discValues[i]), setB.getZSlice(z).getUMF().getFS(discValues[i])) + min(setA.getZSlice(z).getLMF().getFS(discValues[i]), setB.getZSlice(z).getLMF().getFS(discValues[i]))
                    denominatorArray[z] += max(setA.getZSlice(z).getUMF().getFS(discValues[i]), setB.getZSlice(z).getUMF().getFS(discValues[i])) + max(setA.getZSlice(z).getLMF().getFS(discValues[i]), setB.getZSlice(z).getLMF().getFS(discValues[i]))   
            for z in range(setA.getNumberOfSlices()):
                numerator += numeratorArray[z] * setA.getZValue(z)
                denominator += denominatorArray[z] * setA.getZValue(z)
            return numerator/denominator
        else:
            raise Exception("Incorrect setA setB types")
    
    def getDiscretisationValues(self,domainSetA: Tuple,domainSetB: Tuple,numberOfDiscretisations: int) -> List[float]:
        """Get the discretisation values across two domains"""
        domain = Tuple(min(domainSetA.getLeft(),domainSetB.getLeft()),max(domainSetA.getRight(),domainSetB.getRight()))
        discStep = domain.getSize()/(numberOfDiscretisations-1)
        discValues = []
        for i in range(numberOfDiscretisations):
            discValues.append(domain.getLeft()+i*discStep)
        return discValues