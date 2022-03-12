"""
SimpleT1FLS_twoOutputs.py
Created 22/12/2021
"""
import math
import time
from juzzyPython.generic.Tuple import Tuple
from juzzyPython.generic.Output import Output
from juzzyPython.generic.Input import Input
from juzzyPython.generic.Plot import Plot
from juzzyPython.type1.system.T1_Rule import T1_Rule
from juzzyPython.type1.system.T1_Antecedent import T1_Antecedent
from juzzyPython.type1.system.T1_Consequent import T1_Consequent
from juzzyPython.type1.system.T1_Rulebase import T1_Rulebase
from juzzyPython.type1.sets.T1MF_Gaussian import T1MF_Gaussian
from juzzyPython.type1.sets.T1MF_Triangular import T1MF_Triangular
from juzzyPython.type1.sets.T1MF_Gauangle import T1MF_Gauangle
from juzzyPython.testing.timeRecorder import timeDecorator

class SimpleT1FLS_twoOutputs:
    """
    Class SimpleT1FLS_twoOutputs: 
    A simple example of a type-1 FLS based on the "How much to tip the waiter"
    scenario which has been augmented to showcase the use of two outputs.
    We have two inputs: food quality and service level and as an output we would
    like to generate the applicable tip as well as a recommended smile as a sign of satisfaction.

    Parameters:None
        
    Functions: 
        getTip
        PlotMFs
        getControlSurfaceData
        getOutput
        getSmile
        
    """

    def __init__(self,unit = False) -> None:

        #Inputs to the FLS
        self.food = Input("Food Quality",Tuple(0,10)) #Rating from 0-10
        self.service = Input("Service Level",Tuple(0,10)) #Rating from 0-10
        #Output
        self.tip = Output(("Tip"),Tuple(0,30)) #Tip from 0-30%
        self.smile = Output(("Smile"),Tuple(0,1)) #Smile from 0-1

        self.plot = Plot()

        #Set up the membership functions (MFs) for each input and output
        badFoodMF = T1MF_Triangular("MF for bad food",0.0,0.0,10.0)
        greatFoodMF = T1MF_Triangular("MF for great food",0.0,10.0,10.0)

        unfriendlyServiceMF = T1MF_Gauangle("MF for unfriendly service",0.0,0.0,6.0)
        okServiceMF = T1MF_Gauangle("MF for ok service",2.5, 5.0, 7.5)
        friendlyServiceMF = T1MF_Gauangle("MF for friendly service",4.0, 10.0, 10.0)

        lowTipMF = T1MF_Gaussian("Low tip", 0.0, 6.0)
        mediumTipMF = T1MF_Gaussian("Medium tip", 15.0, 6.0)
        highTipMF = T1MF_Gaussian("High tip", 30.0, 6.0)

        smallSmileMF = T1MF_Triangular("MF for Small Smile",0.0,0.0,1.0)
        bigSmileMF = T1MF_Triangular("MF for Big Smile",0.0,1.0,1.0)

        #Set up the antecedents and consequents
        badFood = T1_Antecedent(badFoodMF, self.food,"BadFood")
        greatFood = T1_Antecedent(greatFoodMF, self.food,"GreatFood")

        unfriendlyService =  T1_Antecedent(unfriendlyServiceMF, self.service,"UnfriendlyService")
        okService = T1_Antecedent(okServiceMF, self.service,"OkService")
        friendlyService =  T1_Antecedent(friendlyServiceMF, self.service,"FriendlyService")

        lowTip =  T1_Consequent( lowTipMF, self.tip,  "LowTip")
        mediumTip =  T1_Consequent( mediumTipMF, self.tip, "MediumTip")
        highTip =  T1_Consequent(highTipMF, self.tip , "HighTip")

        smallSmile =  T1_Consequent(smallSmileMF, self.smile, "SmallSmile")
        bigSmile =  T1_Consequent(bigSmileMF, self.smile , "BigSmile")

        #Set up the rulebase and add rules
        self.rulebase = T1_Rulebase()
        self.rulebase.addRule(T1_Rule([badFood, unfriendlyService], consequents = [smallSmile,lowTip]))
        self.rulebase.addRule(T1_Rule([badFood, okService], consequents =[smallSmile,lowTip]))
        self.rulebase.addRule(T1_Rule([badFood, friendlyService],consequent = mediumTip))
        self.rulebase.addRule(T1_Rule([greatFood, unfriendlyService], consequent =lowTip))
        self.rulebase.addRule(T1_Rule([greatFood, okService], consequents =[smallSmile,mediumTip]))
        self.rulebase.addRule(T1_Rule([greatFood, friendlyService], consequents =[bigSmile,highTip]))

        #just an example of setting the discretisation level of an output - the usual level is 100
        self.tip.setDiscretisationLevel(50)

        #get some outputs
        self.getOutput(7,8)
        self.getOutput(0,2.5)
        self.getOutput(10,1.0)
        print("--> Note that for smile the output is -Not a Number- (nan). This is because no rule was defined for the given input combination and the -smile- output")
       

        print(self.rulebase.toString())
        #Plot control surface, false for height defuzzification, true for centroid defuzz.
        self.getControlSurfaceData(self.tip,False,100,100)
        self.getControlSurfaceData(self.smile,True,100,100)
        print("--> Note that in the control surfaces any areas which would result in NaN are replaced by 0 by convention.")

        self.plotMFs("Food Quality Membership Functions",[badFoodMF, greatFoodMF], self.food.getDomain(), 100)
        self.plotMFs("Service Level Membership Functions", [unfriendlyServiceMF, okServiceMF, friendlyServiceMF], self.service.getDomain(), 100)
        self.plotMFs("Level of Tip Membership Functions", [lowTipMF, mediumTipMF, highTipMF], self.tip.getDomain(), 100)
        self.plotMFs("Satisfaction Smile Membership Functions", [smallSmileMF, bigSmileMF], self.smile.getDomain(), 100)

      
        if not unit:
            self.plot.show()
    
    @timeDecorator
    def getOutput(self,foodQuality,serviceLevel) -> None:
        """Calculate the output based on the two inputs"""
        self.food.setInput(foodQuality)
        self.service.setInput(serviceLevel)
        print("The food was: "+str(self.food.getInput()))
        print("The service was: "+str(self.service.getInput()))
        out = self.rulebase.evaluate(0)
        tip = out[self.tip]
        if not self.smile in out:
            smile = float('NaN')
        else:
            smile = out[self.smile]
        print("Using height defuzzification, the FLS recommends a tip of"
                + "tip of: "+str(tip) + " and a smile of: "+str(smile))
        out = self.rulebase.evaluate(1)
        tip = out[self.tip]
        if not self.smile in out:
            smile = float('NaN')
        else:
            smile = out[self.smile]
        print("Using centroid defuzzification, the FLS recommends a tip of"
                + "tip of: "+str(tip) + " and a smile of: "+str(smile))
    
    @timeDecorator
    def getControlSurfaceData(self,o,useCentroidDefuzz,input1Discs,input2Discs,unit = False) -> None:
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
                    out = self.rulebase.evaluate(1).get(o)
                else:
                    out = self.rulebase.evaluate(0).get(o)
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
        self.plot.plotControlSurface(x,y,z,self.food.getName(),self.service.getName(),o.getName())
    
    @timeDecorator
    def plotMFs(self,name,sets,xAxisRange,discretizationLevel):
        """Plot the lines for each membership function of the sets"""
        self.plot.figure()
        self.plot.title(name)
        for i in range(len(sets)):
            self.plot.plotMF(name.replace("Membership Functions",""),sets[i].getName(),sets[i],discretizationLevel,xAxisRange,Tuple(0.0,1.0),False)
        self.plot.legend()
    
    def getTip(self) -> Output:
        return self.tip
    
    def getSmile(self) -> Output:
        return self.smile

if __name__ == "__main__":
    SimpleT1FLS_twoOutputs()
