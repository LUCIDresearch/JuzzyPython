"""
SimpleIT2FLS.py
Created 20/1/2022
"""
import time
import math
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.generic.Plot import Plot
from juzzyPython.intervalType2.system.IT2_Antecedent import IT2_Antecedent
from juzzyPython.intervalType2.system.IT2_Consequent import IT2_Consequent
from juzzyPython.intervalType2.system.IT2_Rule import IT2_Rule
from juzzyPython.intervalType2.system.IT2_Rulebase import IT2_Rulebase
from juzzyPython.type1.sets.T1MF_Gaussian import T1MF_Gaussian
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.type1.sets.T1MF_Gauangle import T1MF_Gauangle
from juzzyPython.intervalType2.sets.IntervalT2MF_Gauangle import IntervalT2MF_Gauangle
from juzzyPython.intervalType2.sets.IntervalT2MF_Gaussian import IntervalT2MF_Gaussian
from juzzyPython.intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular

class SimpleIT2FLS:
    """
    Class SimpleIT2FLS: 
    A simple example of an interval Type-2 FLS based on the "How much to tip the waiter"
    scenario.
    The example is an extension of the Type-1 FLS example where we extend the MFs
    and use the Interval Type-2 System classes. Note that in contrast to the type-1
    case, here only two sets are used to model the service quality.
    We have two inputs: food quality and service level and as an output we would
    like to generate the applicable tip.

    Parameters:None
        
    Functions: 
        getTip
        PlotMFs
        getControlSurfaceData
        
    """

    def __init__(self,unit = False) -> None:
        self.PRINTTIME = True
        self.start = time.time()

        #Inputs to the FLS
        self.food = Input("Food Quality",Tuple(0,10)) #Rating from 0-10
        self.service = Input("Service Level",Tuple(0,10)) #Rating from 0-10
        #Output
        self.tip = Output(("Tip"),Tuple(0,30)) #Tip from 0-30%

        self.plot = Plot()

        #Set up the membership functions (MFs) for each input and output
        badFoodUMF = T1MF_Triangular("Upper MF for bad food",0.0,0.0,10.0)
        badFoodLMF = T1MF_Triangular("Lower MF for bad food",0.0,0.0,8.0)
        badFoodMF = IntervalT2MF_Triangular("IT2MF for bad food",badFoodUMF,badFoodLMF)

        greatFoodUMF = T1MF_Triangular("Upper MF for great food",0.0,10.0,10.0)
        greatFoodLMF = T1MF_Triangular("Lower MF for great food",2.0,10.0,10.0)
        greatFoodMF = IntervalT2MF_Triangular("IT2MF for great food",greatFoodUMF,greatFoodLMF)

        unfriendlyServiceUMF = T1MF_Gauangle("Upper MF for unfriendly service",0.0,0.0,8.0)
        unfriendlyServiceLMF = T1MF_Gauangle("Lower MF for unfriendly service",0.0,0.0,6.0)
        unfriendlyServiceMF = IntervalT2MF_Gauangle("IT2MF for unfriendly service",unfriendlyServiceUMF,unfriendlyServiceLMF)

        friendlyServiceUMF = T1MF_Gauangle("Upper MF for friendly service",2.0,10.0,10.0)
        friendlyServiceLMF = T1MF_Gauangle("Lower MF for friendly service",4.0,10.0,10.0)
        friendlyServiceMF = IntervalT2MF_Gauangle("IT2MF for friendly service",friendlyServiceUMF,friendlyServiceLMF)

        lowTipUMF = T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0)
        lowTipLMF = T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0)
        lowTipMF = IntervalT2MF_Gaussian("IT2MF for Low Tip",lowTipUMF,lowTipLMF)

        mediumTipUMF = T1MF_Gaussian("Upper MF medium tip", 15.0, 6.0)
        mediumTipLMF = T1MF_Gaussian("Lower MF medium tip", 15.0, 4.0)
        mediumTipMF = IntervalT2MF_Gaussian("IT2MF for medium Tip",mediumTipUMF,mediumTipLMF)

        highTipUMF = T1MF_Gaussian("Upper MF high tip", 30.0, 6.0)
        highTipLMF = T1MF_Gaussian("Lower MF high tip", 30.0, 4.0)
        highTipMF = IntervalT2MF_Gaussian("IT2MF for high Tip",highTipUMF,highTipLMF) 

        #Set up the antecedents and consequents
        badFood = IT2_Antecedent(badFoodMF, self.food,"BadFood")
        greatFood = IT2_Antecedent(greatFoodMF, self.food,"GreatFood")

        unfriendlyService =  IT2_Antecedent(unfriendlyServiceMF, self.service,"UnfriendlyService")
        friendlyService =  IT2_Antecedent(friendlyServiceMF, self.service,"FriendlyService")

        lowTip =  IT2_Consequent( lowTipMF, self.tip,  "LowTip")
        mediumTip =  IT2_Consequent( mediumTipMF, self.tip, "MediumTip")
        highTip =  IT2_Consequent(highTipMF, self.tip , "HighTip")

        #Set up the rulebase and add rules
        self.rulebase = IT2_Rulebase()
        self.rulebase.addRule(IT2_Rule([badFood, unfriendlyService], consequent = lowTip))
        self.rulebase.addRule(IT2_Rule([badFood, friendlyService],consequent = mediumTip))
        self.rulebase.addRule(IT2_Rule([greatFood, unfriendlyService], consequent =lowTip))
        self.rulebase.addRule(IT2_Rule([greatFood, friendlyService], consequent =highTip))

        #get some outputs
        self.getTip(7,8)
        self.getTip(0,0)

        if self.PRINTTIME:
            print("Found single tip results in (seconds):")
            print(str(time.time()-self.start))

        print(self.rulebase.toString())
        #Plot control surface, false for height defuzzification, true for centroid defuzz.
        self.getControlSurfaceData(False,100,100)
        self.plotMFs("Food Quality Membership Functions",[badFoodMF, greatFoodMF], self.food.getDomain(), 100)
        self.plotMFs("Service Level Membership Functions", [unfriendlyServiceMF, friendlyServiceMF], self.service.getDomain(), 100)
        self.plotMFs("Level of Tip Membership Functions", [lowTipMF, mediumTipMF, highTipMF], self.tip.getDomain(), 100)

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
        print("Using center of sets type reduction, the IT2 FLS recommends a"
                + "tip of: "+str(self.rulebase.evaluate(0)[self.tip]))
        print("Using centroid type reduction, the IT2 FLS recommends a"
                + "tip of: "+str(self.rulebase.evaluate(1)[self.tip]))
        
        print("Centroid of the output for TIP (based on centroid type reduction):")
        centroid = self.rulebase.evaluateGetCentroid(1)
        centroidTip = list(centroid[self.tip])
        if isinstance(centroidTip[0],Tuple):
            centroidTipXValues = centroidTip[0]
            centroidTipYValues = centroidTip[1]
        else:
            centroidTipXValues = centroidTip[1]
            centroidTipYValues = centroidTip[0]
        print(centroidTipXValues.toString()+" at y= "+str(centroidTipYValues))
        
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
                    out = self.rulebase.evaluate(1).get(self.tip)
                else:
                    out = self.rulebase.evaluate(0).get(self.tip)
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
        

    def plotMFs(self,name,sets,xAxisRange,discretizationLevel):
        """Plot the lines for each membership function of the sets"""
        self.plot.figure()
        self.plot.title(name)
        for i in range(len(sets)):
            self.plot.plotMF2(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,False)
        self.plot.legend()

if __name__ == "__main__":
    SimpleIT2FLS()
