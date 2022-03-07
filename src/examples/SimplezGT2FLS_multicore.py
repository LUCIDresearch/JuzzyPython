"""
SimplezGT2FLS_multicore.py
Created 5/3/2022
"""
import sys
sys.path.append("..")
import math
import time
from generic.Tuple import Tuple
from generic.Output import Output
from generic.Input import Input
from generic.Plot import Plot
from generalType2zSlices.system.GenT2_Antecedent import GenT2_Antecedent
from generalType2zSlices.system.GenT2_Rule import GenT2_Rule
from generalType2zSlices.system.GenT2_Consequent import GenT2_Consequent
from generalType2zSlices.system.GenT2_Rulebase import GenT2_Rulebase
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Triangular import T1MF_Triangular
from intervalType2.sets.IntervalT2MF_Gaussian import IntervalT2MF_Gaussian
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from generalType2zSlices.sets.GenT2MF_Gaussian import GenT2MF_Gaussian
from generalType2zSlices.sets.GenT2MF_Triangular import GenT2MF_Triangular
from generalType2zSlices.multicore.FLCFactory import FLCFactory


class SimplezGT2FLS_multicore:
    """
    Class SimplezGT2FLS_multicore: 
    A simple example of a zSlices based general Type-2 FLS based on the "How much 
    to tip the waiter" scenario.
    The example is an extension of the Interval Type-2 FLS example where we extend the MFs
    and use zSlices based General Type-2 Fuzzy System classes.
    We have two inputs: food quality and service level and as an output we would
    like to generate the applicable tip.
    This uses multicore processing


    Parameters:None
        
    Functions: 
        getTip
        PlotMFs
        getControlSurfaceData
        
    """

    def __init__(self,unit = False) -> None:
        self.PRINTTIME = True
        self.start = time.time()
        self.numberOfzLevels = 4
        self.typeReduction = 0
        self.xDiscs = 50
        self.yDiscs = 10

        #Inputs to the FLS
        self.food = Input("Food Quality",Tuple(0,10)) #Rating from 0-10
        self.service = Input("Service Level",Tuple(0,10)) #Rating from 0-10
        #Output
        self.tip = Output(("Tip"),Tuple(0,30)) #Tip from 0-30%

        self.plot = Plot()

        #Set up the membership functions (MFs) for each input and output
        badFoodUMF = T1MF_Triangular("Upper MF for bad food",0.0,0.0,10.0)
        badFoodLMF = T1MF_Triangular("Lower MF for bad food",0.0,0.0,8.0)
        badFoodIT2MF = IntervalT2MF_Triangular("IT2MF for bad food",badFoodUMF,badFoodLMF)
        badFoodMF = GenT2MF_Triangular("zGT2MF for bad food", primer = badFoodIT2MF, numberOfzLevels = self.numberOfzLevels)


        greatFoodUMF = T1MF_Triangular("Upper MF for great food",0.0,10.0,10.0)
        greatFoodLMF = T1MF_Triangular("Lower MF for great food",2.0,10.0,10.0)
        greatFoodIT2MF = IntervalT2MF_Triangular("IT2MF for great food",greatFoodUMF,greatFoodLMF)
        greatFoodMF = GenT2MF_Triangular("zGT2MF for great food", primer = greatFoodIT2MF, numberOfzLevels = self.numberOfzLevels)


        unfriendlyServiceUMF = T1MF_Triangular("Upper MF for unfriendly service",0.0,0.0,8.0)
        unfriendlyServiceLMF = T1MF_Triangular("Lower MF for unfriendly service",0.0,0.0,6.0)
        unfriendlyServiceIT2MF = IntervalT2MF_Triangular("IT2MF for unfriendly service",unfriendlyServiceUMF,unfriendlyServiceLMF)
        unfriendlyServiceMF = GenT2MF_Triangular("zGT2MF for unfriendly service", primer = unfriendlyServiceIT2MF, numberOfzLevels = self.numberOfzLevels)

        friendlyServiceUMF = T1MF_Triangular("Upper MF for friendly service",2.0,10.0,10.0)
        friendlyServiceLMF = T1MF_Triangular("Lower MF for friendly service",4.0,10.0,10.0)
        friendlyServiceIT2MF = IntervalT2MF_Triangular("IT2MF for friendly service",friendlyServiceUMF,friendlyServiceLMF)
        friendlyServiceMF = GenT2MF_Triangular("zGT2MF for friendly service", primer = friendlyServiceIT2MF, numberOfzLevels = self.numberOfzLevels)

        lowTipUMF = T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0)
        lowTipLMF = T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0)
        lowTipIT2MF = IntervalT2MF_Gaussian("IT2MF for Low Tip",lowTipUMF,lowTipLMF)
        lowTipMF = GenT2MF_Gaussian("zGT2MF for Low tip", lowTipIT2MF, self.numberOfzLevels)

        mediumTipUMF = T1MF_Gaussian("Upper MF medium tip", 15.0, 6.0)
        mediumTipLMF = T1MF_Gaussian("Lower MF medium tip", 15.0, 4.0)
        mediumTipIT2MF = IntervalT2MF_Gaussian("IT2MF for medium Tip",mediumTipUMF,mediumTipLMF)
        mediumTipMF = GenT2MF_Gaussian("zGT2MF for medium tip", mediumTipIT2MF, self.numberOfzLevels)


        highTipUMF = T1MF_Gaussian("Upper MF high tip", 30.0, 6.0)
        highTipLMF = T1MF_Gaussian("Lower MF high tip", 30.0, 4.0)
        highTipIT2MF = IntervalT2MF_Gaussian("IT2MF for high Tip",highTipUMF,highTipLMF) 
        highTipMF = GenT2MF_Gaussian("zGT2MF for high tip", highTipIT2MF, self.numberOfzLevels)

        #Set up the antecedents and consequents
        badFood = GenT2_Antecedent("BadFood",badFoodMF, self.food)
        greatFood = GenT2_Antecedent("GreatFood",greatFoodMF, self.food)

        unfriendlyService =  GenT2_Antecedent("UnfriendlyService",unfriendlyServiceMF, self.service)
        friendlyService =  GenT2_Antecedent("FriendlyService",friendlyServiceMF, self.service)

        lowTip =  GenT2_Consequent(  "LowTip",lowTipMF, self.tip )
        mediumTip =  GenT2_Consequent( "MediumTip",mediumTipMF, self.tip )
        highTip =  GenT2_Consequent("HighTip",highTipMF, self.tip )

        #Set up the rulebase and add rules
        self.rulebase = GenT2_Rulebase()
        self.rulebase.addRule(GenT2_Rule([badFood, unfriendlyService], consequent = lowTip))
        self.rulebase.addRule(GenT2_Rule([badFood, friendlyService],consequent = mediumTip))
        self.rulebase.addRule(GenT2_Rule([greatFood, unfriendlyService], consequent =lowTip))
        self.rulebase.addRule(GenT2_Rule([greatFood, friendlyService], consequent =highTip))

        #FLC Multiprocessing class
        self.FLC = FLCFactory(self.rulebase.getIT2Rulebases())

        #get some outputs
        self.getTip(7,8)
        self.getTip(0.0,0.0)

        if self.PRINTTIME:
            print("Found single tip results in (seconds):")
            print(str(time.time()-self.start))
       
        print(self.rulebase.toString())
        #Plot control surface, false for height defuzzification, true for centroid defuzz.
        
        self.plotMFs("Food Quality Membership Functions",[badFoodMF, greatFoodMF], self.food.getDomain(), 100,True,True)
        self.plotMFs("Service Level Membership Functions", [unfriendlyServiceMF, friendlyServiceMF], self.service.getDomain(), 100,True,True)
        self.plotMFs("Level of Tip Membership Functions", [lowTipMF, mediumTipMF, highTipMF], self.tip.getDomain(), 100,True,True)
        self.getControlSurfaceData(False,self.xDiscs,self.yDiscs)

        if self.PRINTTIME:
            print("Generated graphs for tip results in (seconds):")
            print(str(time.time()-self.start))
        if not unit:
            self.plot.show()
        
        
    def getTip(self,foodQuality,serviceLevel) -> None:
        """Calculate the output based on the two inputs"""
        self.food.setInput(foodQuality)
        self.service.setInput(serviceLevel)

        print("The food was: "+str(self.food.getInput()))
        print("The service was: "+str(self.service.getInput()))
        print("Using height center of sets type reduction, the zSlices based general type-2 FLS recommends a "
                + "tip of: "+str(self.FLC.runFactory(0)[self.tip]))
        print("Using centroid type reduction, the zSlices based general type-2 FLS recommends a"
                + "tip of: "+str(self.FLC.runFactory(1)[self.tip]))
        
        
     
    def getControlSurfaceData(self,useCentroidDefuzz,input1Discs,input2Discs,unit = False) -> None:
        """Get the data to plot the control surface"""
        if unit:
            test = []
        incrX = self.food.getDomain().getSize()/(input1Discs-1.0)
        incrY = self.service.getDomain().getSize()/(input2Discs-1.0)
        x = []
        y = []
        z = [ [0]*input1Discs for i in range(input2Discs)]

        for i in range(input1Discs):
            x.append(i*incrX)
        for i in range(input2Discs):
            y.append(i*incrY)
        
        for x_ in range(input1Discs):
            self.food.setInput(x[x_])
            for y_ in range(input2Discs):
                self.service.setInput(y[y_])
                if useCentroidDefuzz:
                    out = self.FLC.runFactory(1)[self.tip]
                else:
                    out = self.FLC.runFactory(0)[self.tip]
                if out == None or math.isnan(out):
                    z[y_][x_] = 0.0
                    if unit:
                        test.append(0.0)
                else:
                    z[y_][x_] = out
                    if unit:
                        test.append(out)
        if unit:
            return test
        self.plot.plotControlSurface(x,y,z,self.food.getName(),self.service.getName(),self.tip.getName())
        
    def plotMFs(self,name,sets,xAxisRange,discretizationLevel,plotAsLines,plotAsSurface):
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
    SimplezGT2FLS_multicore()
