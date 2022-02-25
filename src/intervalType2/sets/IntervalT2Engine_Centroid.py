"""
IntervalT2Engine_Centroid.py
Created 6/1/2022
"""
import sys
from typing import List

from intervalType2.sets.IntervalT2MF_Interface import IntervalT2MF_Interface
sys.path.append("..")
import math

from generic.Tuple import Tuple
import intervalType2.sets.IntervalT2MF_Intersection 
import intervalType2.sets.IntervalT2MF_Union


#TODO Classes 

class IntervalT2Engine_Centroid():
    """
    Class IntervalT2Engine_Centroid
    Implements Centroid calculation using the Karnik Mendel and Enhanced Karnik
    Mendel Iterative Procedures.

    Parameters: 
        primaryDiscretisationLevel : Int with discretisation level

    Functions:
       getPrimaryDiscretizationLevel
       setPrimaryDiscretizationLevel
       getCentroid
       getCentroidKM
       getCentroid_enhanced
       getWeightedSum
    """

    def __init__(self,primaryDiscretisationLevel: int = None) -> None:
        self.KARNIKMENDEL = 0
        self.ENHANCHEDKARNIKMENDEL = 1
        self.ENHANCHEDKARNIKMENDEL_L0 = 2.4
        self.ENHANCHEDKARNIKMENDEL_R0 = 1.7
        self.centroidAlgorithmSelector = self.KARNIKMENDEL
        self.log = False
        self.DEBUG = False
        self.primaryDiscretisationLevel = 100
        if primaryDiscretisationLevel != None:
            self.primaryDiscretisationLevel = primaryDiscretisationLevel
    
    def getPrimaryDiscretizationLevel(self) -> int:
        """Return the primaryDiscretizationLevel"""
        return self.primaryDiscretisationLevel
    
    def setPrimaryDiscretizationLevel(self,primaryDiscretisationLevel: int) -> None:
        """Set the primaryDiscretizationLevel"""
        self.primaryDiscretisationLevel = primaryDiscretisationLevel
    
    def getCentroid(self,mf: IntervalT2MF_Interface) -> Tuple:
        """Get the centroid according to the algorithm selector setting"""
        if self.centroidAlgorithmSelector == self.KARNIKMENDEL:
            return self.getCentroidKM(mf)
        elif self.centroidAlgorithmSelector == self.ENHANCHEDKARNIKMENDEL:
            return self.getCentroid_enhanced(mf,self.ENHANCHEDKARNIKMENDEL_L0,self.ENHANCHEDKARNIKMENDEL_R0)
    
    def getCentroidKM(self,mf: IntervalT2MF_Interface) -> Tuple:
        """Centroid using the Karnikmendel method"""
        if mf == None:
            return Tuple(float("nan"),float("nan"))
        if isinstance(mf,intervalType2.sets.IntervalT2MF_Intersection.IntervalT2MF_Intersection) and not mf.intersectionExists():
            return Tuple(float("nan"),float("nan"))
        y_l = 0 
        y_r = 0
        iterationCounterLeft = 0
        iterationCounterRight = 0
        if self.DEBUG:
            print("MF Name: "+mf.getName())
        if isinstance(mf,intervalType2.sets.IntervalT2MF_Union.IntervalT2MF_Union) and mf.isNull():
            return None
        if self.DEBUG:
            print("domain left point is: " + str(mf.getSupport().getLeft()) + "  and right point is: "+ str(mf.getSupport().getRight()))
        if mf.getSupport().getRight() == mf.getSupport().getLeft():
            return mf.getSupport().clone()
        #stores the size of the domain over which the function is evaluated
        domainSize = mf.getSupport().getRight() - mf.getSupport().getLeft()
        #setup arrays for primaryDiscretizationLevel
        w = [0] * self.primaryDiscretisationLevel
        x = [0] * self.primaryDiscretisationLevel
        weights = [0] * self.primaryDiscretisationLevel
        #stores various bits for efficiency purposes (avoid recalculation
        temp = domainSize / (self.primaryDiscretisationLevel-1)

        if self.DEBUG:
            print("Domainsize = " + str(domainSize) + ",  discLevel = " + str(self.primaryDiscretizationLevel) + ",  stepSize = " + str(temp))
        for i in range(self.primaryDiscretisationLevel):
            x[i] = i * temp + mf.getSupport().getLeft()
            w[i] = mf.getFS(x[i])
            weights[i] = (w[i].getLeft()+w[i].getRight())/2
            if self.DEBUG:
                print("KM x disc. number: " + str(i) + "  = " + str(x[i]) + "  y(w[i]) = " + str(w[i]) + "   weights[i] = " + str(weights[i]))
        
        for runs in range(2): #One for left , one for right
            stopFlag = False
            for i in range(self.primaryDiscretisationLevel):
                w[i] = mf.getFS(x[i])
                weights[i] = (w[i].getLeft()+w[i].getRight())/2
            y = self.getWeightedSum(x,weights)
            if self.DEBUG:
                print("y = "+str(y))
            
            while not stopFlag:
                if self.log:
                    if runs == 0:
                        iterationCounterLeft += 1
                    else:
                        iterationCounterRight += 1
                for k in range(self.primaryDiscretisationLevel-1):
                    if self.DEBUG:
                        print("k = " + str(k) + "  y = " + str(y) + "  x[k] = " + str(x[k]) + "  x[k+1] = " + str(x[k + 1]))
                    if x[k] <= y and y <= x[k+1]:
                        break
                    if k == (self.primaryDiscretisationLevel-2):
                        print("NO k WAS  FOUND FOR: "+mf.getName() + '\n' + str(mf))
                if runs == 0:
                    if self.DEBUG:
                        print("Doing left   k = " + str(k) + "   and primaryDiscretizationLevel = " + str(self.primaryDiscretizationLevel))
                    for i in range(k+1):
                        weights[i] = w[i].getRight()
                    for i in range(k+1,self.primaryDiscretisationLevel):
                        weights[i] = w[i].getLeft()
                else:
                    if self.DEBUG:
                        print("Doing right   k = " + str(k) + "   and primaryDiscretizationLevel = " + str(self.primaryDiscretizationLevel))
                    for i in range(k+1):
                        weights[i] = w[i].getLeft()
                    for i in range(k+1,self.primaryDiscretisationLevel):
                        weights[i] = w[i].getRight()
                
                yDash = self.getWeightedSum(x,weights)
                if self.DEBUG:
                    print("yDash = " + str(yDash) + "   and y = " + str(y) + "   y_l=" + str(y_l) + "  y_r=" + str(y_r))
                if math.isnan(yDash):
                    if self.DEBUG:
                        print("Is using NAN in KM the right thing to avoid divide by zero? " + str(mf))
                    step = mf.getSupport().getSize()/9
                    for i in range(10):
                        value = i*step+mf.getSupport().getLeft()
                        if self.DEBUG:
                            print("FS for set at " + str(value) + " is: " + str(mf.getFS(value)))
                    yDash = y
                
                if abs(yDash-y) < 0.001:
                    if self.DEBUG:
                        print("SUCCESS! - y = " + str(y))
                    stopFlag = True
                    if runs == 0:
                        y_l = yDash
                    else:
                        y_r = yDash
                else:
                    y = yDash

        return Tuple(y_l,y_r)

    def getCentroid_enhanced(self,mf: IntervalT2MF_Interface,divisor_left: float,divisor_right: float) -> Tuple:
        """Return the centroid tuple according to the enhanced KM"""
        yDash = 0
        y_l = 0
        y_r = 0
        aDash = 0
        bDash = 0
        s = 0
        log = True
        iterationCounterLeft = 0
        iterationCounterRight = 0
        #stores the size of the domain over which the function is evaluated
        domainSize = mf.getSupport().getRight() - mf.getSupport().getLeft()
        #setup arrays for primaryDiscretizationLevel
        w = [0] * (self.primaryDiscretisationLevel+1)
        x = [0] * (self.primaryDiscretisationLevel+1)
        #stores various bits for efficiency purposes (avoid recalculation)
        temp = domainSize / self.primaryDiscretisationLevel
        #set x and calculate weights (membership values for left/right (bottom/top)
        for i in range(self.primaryDiscretisationLevel+1):
            x[i] = i*temp+mf.getSupport().getLeft()
            w[i] = mf.getFS(x[i])

        #Left
        k = round(self.primaryDiscretisationLevel/divisor_left)
        a = 0
        b = 0
        #set to true if correct yDash is found.
        stopFlag = False
        for i in range(k+1):
            a+= x[i]*w[i].getRight()
            b+= w[i].getRight()
        for i in range(k+1,self.primaryDiscretisationLevel):
            a+= x[i]*w[i].getLeft()
            b+= w[i].getLeft()
        y = a/b

        while not stopFlag:
            if log:
                iterationCounterLeft += 1
            for kDash in range(self.primaryDiscretisationLevel):
                if x[kDash] <= y and y <= x[kDash+1]:
                    break
            print("kDash Left = " + str(kDash) + "   k = " + str(k))
            if kDash == k:
                stopFlag = True
                y_l = y
            else:
                s = kDash - k
                if s < 0:
                    s = -1
                else: 
                    s = 1
                
                for i in range(min(k,kDash)+1,max(k,kDash)+1):
                    aDash += x[i] * (w[i].getRight()-w[i].getLeft())
                    bDash += (w[i].getRight()-w[i].getLeft())

                aDash = a + s * aDash
                bDash = b + s * bDash   
                yDash = aDash/bDash
                y = yDash
                a = aDash
                b = bDash
                k = kDash
                aDash = 0
                bDash = 0

        #Right
        k = round(self.primaryDiscretisationLevel/divisor_right)
        a = 0
        b = 0
        stopFlag = False
        for i in range(k+1):
            a+= x[i]*w[i].getLeft()
            b+= w[i].getLeft()
        for i in range(k+1,self.primaryDiscretisationLevel):
            a+= x[i]*w[i].getRight()
            b+= w[i].getRight()
        y = a/b

        while not stopFlag:
            if log:
                iterationCounterRight += 1
            for kDash in range(self.primaryDiscretisationLevel):
                if x[kDash] <= y and y <= x[kDash+1]:
                    break
            print("kDash Right = " + str(kDash) + "   k = " + str(k))
            if kDash == k:
                stopFlag = True
                y_r = y
            else:
                s = kDash - k
                if s < 0:
                    s = -1
                else: 
                    s = 1
                
                for i in range(min(k,kDash)+1,max(k,kDash)+1):
                    aDash += x[i] * (w[i].getRight()-w[i].getLeft())
                    bDash += (w[i].getRight()-w[i].getLeft())

                aDash = a - s * aDash
                bDash = b - s * bDash   
                yDash = aDash/bDash
                y = yDash
                a = aDash
                b = bDash
                k = kDash
                aDash = 0
                bDash = 0

        return Tuple(y_l,y_r)

    def getWeightedSum(self,x: List[float],w: List[float]) -> float:
        """Return the weighted sum from two arrays"""
        temp = 0.0
        temp2 = 0.0
        for i in range(len(x)):
            temp+= x[i] * w[i]
            temp2 += w[i]
        if temp2 != 0:
            return temp/temp2
        else:
            return float("nan")
