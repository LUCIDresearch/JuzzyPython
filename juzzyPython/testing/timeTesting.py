"""
Time testing across the variety of different functions we use to run FLS systems.


1. Rulebases

    T1 Rulebase
        evaluate Height
        evaluate Centroid
    IT2 Rulebase
        evaluate COS + getCentroid
        evaluate Centroid + getCentroid
    GT2 Rulebase
        evaluate COS + getCentroid
        evaluate Centroid + getCentroid
    GT2 Multicore evaluate
    
2. Graphs

    plotControlSurface
    plotMF2
    plotMF
    plotMFasLines
    plotMFasSurface

3. Examples

    All examples in folder

"""

import math
import time
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.generic.Plot import Plot
from juzzyPython.generalType2zSlices.system.GenT2_Antecedent import GenT2_Antecedent
from juzzyPython.intervalType2.system.IT2_Antecedent import IT2_Antecedent
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.generalType2zSlices.system.GenT2_Rule import GenT2_Rule
from juzzyPython.intervalType2.system.IT2_Rule import IT2_Rule
from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.generalType2zSlices.system.GenT2_Consequent import GenT2_Consequent
from juzzyPython.intervalType2.system.IT2_Consequent import IT2_Consequent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.generalType2zSlices.system.GenT2_Rulebase import GenT2_Rulebase
from juzzyPython.intervalType2.system.IT2_Rulebase import IT2_Rulebase
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase
from juzzyPython.type1.sets.T1MF_Gaussian import T1MF_Gaussian
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.intervalType2.sets.IntervalT2MF_Gaussian import IntervalT2MF_Gaussian
from juzzyPython.intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from juzzyPython.generalType2zSlices.sets.GenT2MF_Gaussian import GenT2MF_Gaussian
from juzzyPython.generalType2zSlices.sets.GenT2MF_Triangular import GenT2MF_Triangular
from juzzyPython.generalType2zSlices.multicore.FLCFactory import FLCFactory
from juzzyPython.testing.timeRecorder import timeDecorator

class TimeTester():

    def __init__(self) -> None:
        self.count = 30
        self.serviceIn = 5
        self.foodIn = 5
        self.numberOfzLevels = 4
        self.typeReduction = 0
        self.xDiscs = 50
        self.yDiscs = 10

    def setup(self):
        #Inputs to the FLS
        self.food = Input("Food Quality",Tuple(0,10)) #Rating from 0-10
        self.service = Input("Service Level",Tuple(0,10)) #Rating from 0-10
        #Output
        self.tip = Output(("Tip"),Tuple(0,30)) #Tip from 0-30%
        self.plot = Plot()
        #Set up the membership functions (MFs) for each input and output
        
        self.badFoodUMF = T1MF_Triangular("Upper MF for bad food",0.0,0.0,10.0)
        badFoodLMF = T1MF_Triangular("Lower MF for bad food",0.0,0.0,8.0)
        self.badFoodIT2MF = IntervalT2MF_Triangular("IT2MF for bad food",self.badFoodUMF,badFoodLMF)
        self.badFoodMF = GenT2MF_Triangular("zGT2MF for bad food", primer = self.badFoodIT2MF, numberOfzLevels = self.numberOfzLevels)
        
        self.greatFoodUMF = T1MF_Triangular("Upper MF for great food",0.0,10.0,10.0)
        greatFoodLMF = T1MF_Triangular("Lower MF for great food",2.0,10.0,10.0)
        self.greatFoodIT2MF = IntervalT2MF_Triangular("IT2MF for great food",self.greatFoodUMF,greatFoodLMF)
        self.greatFoodMF = GenT2MF_Triangular("zGT2MF for great food", primer = self.greatFoodIT2MF, numberOfzLevels = self.numberOfzLevels)


        self.unfriendlyServiceUMF = T1MF_Triangular("Upper MF for unfriendly service",0.0,0.0,8.0)
        unfriendlyServiceLMF = T1MF_Triangular("Lower MF for unfriendly service",0.0,0.0,6.0)
        self.unfriendlyServiceIT2MF = IntervalT2MF_Triangular("IT2MF for unfriendly service",self.unfriendlyServiceUMF,unfriendlyServiceLMF)
        self.unfriendlyServiceMF = GenT2MF_Triangular("zGT2MF for unfriendly service", primer = self.unfriendlyServiceIT2MF, numberOfzLevels = self.numberOfzLevels)

        self.friendlyServiceUMF = T1MF_Triangular("Upper MF for friendly service",2.0,10.0,10.0)
        friendlyServiceLMF = T1MF_Triangular("Lower MF for friendly service",4.0,10.0,10.0)
        self.friendlyServiceIT2MF = IntervalT2MF_Triangular("IT2MF for friendly service",self.friendlyServiceUMF,friendlyServiceLMF)
        self.friendlyServiceMF = GenT2MF_Triangular("zGT2MF for friendly service", primer = self.friendlyServiceIT2MF, numberOfzLevels = self.numberOfzLevels)

        self.lowTipUMF = T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0)
        lowTipLMF = T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0)
        self.lowTipIT2MF = IntervalT2MF_Gaussian("IT2MF for Low Tip",self.lowTipUMF,lowTipLMF)
        self.lowTipMF = GenT2MF_Gaussian("zGT2MF for Low tip", self.lowTipIT2MF, self.numberOfzLevels)

        self.mediumTipUMF = T1MF_Gaussian("Upper MF medium tip", 15.0, 6.0)
        mediumTipLMF = T1MF_Gaussian("Lower MF medium tip", 15.0, 4.0)
        self.mediumTipIT2MF = IntervalT2MF_Gaussian("IT2MF for medium Tip",self.mediumTipUMF,mediumTipLMF)
        self.mediumTipMF = GenT2MF_Gaussian("zGT2MF for medium tip", self.mediumTipIT2MF, self.numberOfzLevels)

        self.highTipUMF = T1MF_Gaussian("Upper MF high tip", 30.0, 6.0)
        highTipLMF = T1MF_Gaussian("Lower MF high tip", 30.0, 4.0)
        self.highTipIT2MF = IntervalT2MF_Gaussian("IT2MF for high Tip",self.highTipUMF,highTipLMF) 
        self.highTipMF = GenT2MF_Gaussian("zGT2MF for high tip", self.highTipIT2MF, self.numberOfzLevels)


        #Set up the antecedents and consequents
        # T1
        badFoodT1 = T1_Antecedent(self.badFoodUMF, self.food,"BadFood")
        greatFoodT1 = T1_Antecedent(self.greatFoodUMF, self.food,"GreatFood")

        unfriendlyServiceT1 =  T1_Antecedent(self.unfriendlyServiceUMF, self.service,"UnfriendlyService")
        friendlyServiceT1 =  T1_Antecedent(self.friendlyServiceUMF, self.service,"FriendlyService")

        lowTipT1 =  T1_Consequent( self.lowTipUMF, self.tip, "LowTip" )
        mediumTipT1 =  T1_Consequent( self.mediumTipUMF, self.tip,"MediumTip" )
        highTipT1 =  T1_Consequent(self.highTipUMF, self.tip,"HighTip" )

        self.rulebaseT1 = T1_Rulebase()
        self.rulebaseT1.addRule(T1_Rule([badFoodT1, unfriendlyServiceT1], consequent = lowTipT1))
        self.rulebaseT1.addRule(T1_Rule([badFoodT1, friendlyServiceT1],consequent = mediumTipT1))
        self.rulebaseT1.addRule(T1_Rule([greatFoodT1, unfriendlyServiceT1], consequent =lowTipT1))
        self.rulebaseT1.addRule(T1_Rule([greatFoodT1, friendlyServiceT1], consequent =highTipT1))

        # IT2
        badFoodIT2 = IT2_Antecedent(self.badFoodIT2MF, self.food, "BadFood")
        greatFoodIT2 = IT2_Antecedent(self.greatFoodIT2MF, self.food, "GreatFood")

        unfriendlyServiceIT2 =  IT2_Antecedent(self.unfriendlyServiceIT2MF, self.service,"UnfriendlyService")
        friendlyServiceIT2 =  IT2_Antecedent(self.friendlyServiceIT2MF, self.service,"FriendlyService")

        lowTipIT2 =  IT2_Consequent(self.lowTipIT2MF, self.tip, "LowTip" )
        mediumTipIT2 =  IT2_Consequent(self.mediumTipIT2MF, self.tip,"MediumTip" )
        highTipIT2 =  IT2_Consequent(self.highTipIT2MF, self.tip,"HighTip" )

        self.rulebaseIT2 = IT2_Rulebase()
        self.rulebaseIT2.addRule(IT2_Rule([badFoodIT2, unfriendlyServiceIT2], consequent = lowTipIT2))
        self.rulebaseIT2.addRule(IT2_Rule([badFoodIT2, friendlyServiceIT2],consequent = mediumTipIT2))
        self.rulebaseIT2.addRule(IT2_Rule([greatFoodIT2, unfriendlyServiceIT2], consequent =lowTipIT2))
        self.rulebaseIT2.addRule(IT2_Rule([greatFoodIT2, friendlyServiceIT2], consequent =highTipIT2))

        # GT2
        badFoodGT2 = GenT2_Antecedent("BadFood",self.badFoodMF, self.food)
        greatFoodGT2 = GenT2_Antecedent("GreatFood",self.greatFoodMF, self.food)

        unfriendlyServiceGT2 =  GenT2_Antecedent("UnfriendlyService",self.unfriendlyServiceMF, self.service)
        friendlyServiceGT2 =  GenT2_Antecedent("FriendlyService",self.friendlyServiceMF, self.service)

        lowTipGT2 =  GenT2_Consequent(  "LowTip",self.lowTipMF, self.tip )
        mediumTipGT2 =  GenT2_Consequent( "MediumTip",self.mediumTipMF, self.tip )
        highTipGT2 =  GenT2_Consequent("HighTip",self.highTipMF, self.tip )

        self.rulebaseGT2 = GenT2_Rulebase()
        self.rulebaseGT2.addRule(GenT2_Rule([badFoodGT2, unfriendlyServiceGT2], consequent = lowTipGT2))
        self.rulebaseGT2.addRule(GenT2_Rule([badFoodGT2, friendlyServiceGT2],consequent = mediumTipGT2))
        self.rulebaseGT2.addRule(GenT2_Rule([greatFoodGT2, unfriendlyServiceGT2], consequent =lowTipGT2))
        self.rulebaseGT2.addRule(GenT2_Rule([greatFoodGT2, friendlyServiceGT2], consequent =highTipGT2))

    def getRulebaseGT2MulticoreTimes(self):
        FLC = FLCFactory(self.rulebaseGT2.getIT2Rulebases())
        self.food.setInput(self.foodIn)
        self.service.setInput(self.serviceIn)
        timecount = 0
        for i in range(self.count):
            start = time.time()
            FLC.runFactory(0)[self.tip]
            timecount += time.time() - start
        print("GT2 average evaluate COS time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            FLC.runFactory(1)[self.tip]
            timecount += time.time() - start
        print("GT2 average evaluate Centroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            FLC.runFactoryGetCentroid(0)
            timecount += time.time() - start
        print("GT2 average evaluate COS getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            FLC.runFactoryGetCentroid(1)
            timecount += time.time() - start
        print("GT2 average evaluate Centroid getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))

    def getRulebaseGT2Times(self):
        self.food.setInput(self.foodIn)
        self.service.setInput(self.serviceIn)
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseGT2.evaluate(0)[self.tip]
            timecount += time.time() - start
        print("GT2 average evaluate COS time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseGT2.evaluate(1)[self.tip]
            timecount += time.time() - start
        print("GT2 average evaluate Centroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseGT2.evaluateGetCentroid(0)
            timecount += time.time() - start
        print("GT2 average evaluate COS getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseGT2.evaluateGetCentroid(1)
            timecount += time.time() - start
        print("GT2 average evaluate Centroid getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
    
    def getRulebaseIT2Times(self):
        self.food.setInput(self.foodIn)
        self.service.setInput(self.serviceIn)
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseIT2.evaluate(0)[self.tip]
            timecount += time.time() - start
        print("IT2 average evaluate COS time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseIT2.evaluate(1)[self.tip]
            timecount += time.time() - start
        print("IT2 average evaluate Centroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseIT2.evaluateGetCentroid(0)
            timecount += time.time() - start
        print("IT2 average evaluate COS getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseIT2.evaluateGetCentroid(1)
            timecount += time.time() - start
        print("IT2 average evaluate Centroid getCentroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
    
    def getRulebaseT1Times(self):
        self.food.setInput(self.foodIn)
        self.service.setInput(self.serviceIn)
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseT1.evaluate(0)[self.tip]
            timecount += time.time() - start
        print("T1 average evaluate Height time over " + str(self.count) + " iterations is "+str(timecount/self.count))
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.rulebaseT1.evaluate(1)[self.tip]
            timecount += time.time() - start
        print("T1 average evaluate Centroid time over " + str(self.count) + " iterations is "+str(timecount/self.count))
            
    def getPlotTimes(self):
        timecount = 0
        for i in range(self.count):
            start = time.time()
            self.plotMFT1("Test",[self.badFoodUMF, self.greatFoodUMF], self.food.getDomain(), 100)
            timecount += time.time() - start
        self.plot.closeAllFigures()
        print("plotMF (T1) average time over " + str(self.count) + " iterations is "+str(timecount/self.count))
    
    def plotMFT1(self,name,sets,xAxisRange,discretizationLevel):
        """Plot the lines for each membership function of the sets"""
        self.plot.figure()
        self.plot.title(name)
        for i in range(len(sets)):
            self.plot.plotMF(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,xAxisRange,Tuple(0.0,1.0),False)
        self.plot.legend()
    
    def plotMFIT2(self,name,sets,xAxisRange,discretizationLevel):
        """Plot the lines for each membership function of the sets"""
        self.plot.figure()
        self.plot.title(name)
        for i in range(len(sets)):
            self.plot.plotMF2(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,True)
        self.plot.legend()
    
    def plotMFGT2(self,name,sets,xAxisRange,discretizationLevel,plotAsLines,plotAsSurface):
        """Plot the lines for each membership function of the sets"""
        if plotAsLines:
            self.plot.figure3d()
            self.plot.title(name)
            for i in range(len(sets)):
                self.plot.plotMFasLines(sets[i],discretizationLevel)
        if plotAsSurface:
            self.plot.figure3d()
            self.plot.title(name)
            for i in range(len(sets)):
                self.plot.plotMFasSurface(sets[i].getName(),sets[i],xAxisRange,discretizationLevel,False)

if __name__ == "__main__":
    t = TimeTester()
    t.setup()
    print("-------- GT2 Multicore --------")
    #t.getRulebaseGT2MulticoreTimes()
    print("------------- GT2 -------------")
    #t.getRulebaseGT2Times()
    print("------------- IT2 -------------")
    #t.getRulebaseIT2Times()
    print("------------- T1 --------------")
    #t.getRulebaseT1Times()
    print("------------ Plot -------------")
    t.getPlotTimes()

