"""
SimpleT1FLS.py
Created 19/12/2021
"""
import sys
sys.path.append("..")

from generic.Tuple import Tuple
from generic.Output import Output
from generic.Input import Input

from type1.system.T1_Rule import T1_Rule
from type1.system.T1_Antecedent import T1_Antecedent
from type1.system.T1_Consequent import T1_Consequent
from type1.system.T1_Rulebase import T1_Rulebase

from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Triangular import T1MF_Triangular
from type1.sets.T1MF_Gauangle import T1MF_Gauangle

class SimpleT1FLS:
    """
    Class SimpleT1FLS: 

    Parameters:None
        
    Functions: 
        
    """

    def __init__(self) -> None:
        self.food = Input("Food Quality",Tuple(0,10))
        self.service = Input("Service Level",Tuple(0,10))
        self.tip = Output(("Tip"),Tuple(0,30))

        badFoodMF = T1MF_Triangular("MF for bad food",0.0,0.0,10.0)
        greatFoodMF = T1MF_Triangular("MF for great food",0.0,10.0,10.0)

        unfriendlyServiceMF = T1MF_Gauangle("MF for unfriendly service",0.0,0.0,6.0)
        okServiceMF = T1MF_Gauangle("MF for ok service",2.5, 5.0, 7.5)
        friendlyServiceMF = T1MF_Gauangle("MF for friendly service",4.0, 10.0, 10.0)

        lowTipMF = T1MF_Gaussian("Low tip", 0.0, 6.0)
        mediumTipMF = T1MF_Gaussian("Medium tip", 15.0, 6.0)
        highTipMF = T1MF_Gaussian("High tip", 30.0, 6.0)

        #Set up the antecedents and consequents - note how the inputs are associated...
        badFood = T1_Antecedent(badFoodMF, self.food,"BadFood")
        greatFood = T1_Antecedent(greatFoodMF, self.food,"GreatFood")

        unfriendlyService =  T1_Antecedent(unfriendlyServiceMF, self.service,"UnfriendlyService")
        okService = T1_Antecedent(okServiceMF, self.service,"OkService")
        friendlyService =  T1_Antecedent(friendlyServiceMF, self.service,"FriendlyService")

        lowTip =  T1_Consequent( lowTipMF, self.tip,  "LowTip")
        mediumTip =  T1_Consequent( mediumTipMF, self.tip, "MediumTip")
        highTip =  T1_Consequent(highTipMF, self.tip , "HighTip")

        self.rulebase = T1_Rulebase()
        self.rulebase.addRule(T1_Rule([badFood, unfriendlyService], consequent = lowTip))
        self.rulebase.addRule(T1_Rule([badFood, okService], consequent =lowTip))
        self.rulebase.addRule(T1_Rule([badFood, friendlyService],consequent = mediumTip))
        self.rulebase.addRule(T1_Rule([greatFood, unfriendlyService], consequent =lowTip))
        self.rulebase.addRule(T1_Rule([greatFood, okService], consequent =mediumTip))
        self.rulebase.addRule(T1_Rule([greatFood, friendlyService], consequent =highTip))

        self.tip.setDiscretisationLevel(50)

        self.getTip(7,8)

        print(self.rulebase.toString())
    
    def getTip(self,foodQuality,serviceLevel) -> None:
        self.food.setInput(foodQuality)
        self.service.setInput(serviceLevel)
        print("The food was: "+str(self.food.getInput()))
        print("The service was: "+str(self.service.getInput()))
        print("Using height defuzzification, the FLS recommends a tip of"
                + "tip of: "+str(self.rulebase.evaluate(0)[self.tip]))
        print("Using centroid defuzzification, the FLS recommends a tip of"
                + "tip of: "+str(self.rulebase.evaluate(1)[self.tip]))
    

if __name__ == "__main__":
    SimpleT1FLS()
