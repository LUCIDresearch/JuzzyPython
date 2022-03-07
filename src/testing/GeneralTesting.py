import sys



sys.path.append("..")
from generalType2zSlices.system.GenT2Engine_Intersection import GenT2Engine_Intersection

from generalType2zSlices.system.GenT2Engine_Defuzzification import GenT2Engine_Defuzzification

from generalType2zSlices.sets.GenT2MF_CylExtension import GenT2MF_CylExtension

from generalType2zSlices.sets.GenT2MF_Trapezoidal import GenT2MF_Trapezoidal
from generalType2zSlices.sets.GenT2MF_Discretized import GenT2MF_Discretized
from intervalType2.sets.IntervalT2MF_Trapezoidal import IntervalT2MF_Trapezoidal

from generalType2zSlices.sets.GenT2MF_Triangular import GenT2MF_Triangular
from generalType2zSlices.sets.GenT2MF_Gaussian import IntervalT2MF_Gaussian,GenT2MF_Gaussian
from generalType2zSlices.sets.GenT2MF_Union import GenT2MF_Union
from generalType2zSlices.system.GenT2Engine_Union import GenT2Engine_Union
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from type1.sets.T1MF_Discretized import T1MF_Discretized
from type1.sets.T1MF_Union import T1MF_Union
from type1.sets.T1MF_Singleton import T1MF_Singleton
from type1.sets.T1MF_Triangular import T1MF_Triangular
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from type1.sets.T1MF_Gaussian import T1MF_Gaussian
from type1.sets.T1MF_Meet import T1MF_Meet
from generalType2zSlices.system.GenT2_Antecedent import GenT2_Antecedent
from generalType2zSlices.system.GenT2_Consequent import GenT2_Consequent
from generic.Input import Input
from generic.Output import Output
from generalType2zSlices.system.GenT2_Rule import GenT2_Rule
from generic.Tuple import Tuple
from similarity.JaccardSimilarity import JaccardSimilarity
test = T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,16),Tuple(9,50)])
#print(test.writeToFileHighRes("test.txt",10))
#test = T1MF_Union(T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]),T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]))
#print(test.getSupport().toString())
#test = T1MF_Trapezoidal("test",[1.0,2.0,3.0,4.0])
#test = T1MF_Meet(T1MF_Discretized("Test",[Tuple(0,5),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]),T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,18),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]))
#print(test.findMax(T1MF_Trapezoidal("test",[1.0,2.0,3.0,4.0])))
#inputlmf = T1MF_Trapezoidal("inputlmf",[1,1,1.1,1.1])
#inputumf = T1MF_Trapezoidal("inputumf",[1,2,33,44])
#inputMfprimer = IntervalT2MF_Trapezoidal("inputmfprimer",inputumf,inputlmf)
#inputMf = GenT2MF_Trapezoidal("inputmf",primer = inputMfprimer,numberOfzLevels=4)
#test = GenT2Engine_Union()
#uni = test.getUnion(inputMf,inputMf)
lowTipUMF = T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0)
lowTipLMF = T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0)
lowTipIT2MF = IntervalT2MF_Gaussian("IT2MF for Low Tip",lowTipUMF,lowTipLMF)
lowTipMF = GenT2MF_Gaussian("zGT2MF for Low tip", primers = [lowTipIT2MF,lowTipIT2MF,lowTipIT2MF])
disc = GenT2MF_Discretized(lowTipMF,4)
#cyl = GenT2MF_CylExtension(test,4)
defuzz = GenT2Engine_Defuzzification(4)
inter = GenT2Engine_Intersection()
#inte =  inter.getIntersection(lowTipMF,lowTipMF)
#print(inte.toString())
#print(defuzz.typeReduce_standard(lowTipMF,4,4))
#print(cyl.getFS(4).toString())
numberOfzLevels = 4
typeReduction = 0
xDiscs = 50
yDiscs = 10

#Inputs to the FLS
food = Input("Food Quality",Tuple(0,10)) #Rating from 0-10
service = Input("Service Level",Tuple(0,10)) #Rating from 0-10
#Output
tip = Output(("Tip"),Tuple(0,30)) #Tip from 0-30%

#Set up the membership functions (MFs) for each input and output
badFoodUMF = T1MF_Triangular("Upper MF for bad food",0.0,0.0,10.0)
badFoodLMF = T1MF_Triangular("Lower MF for bad food",0.0,0.0,8.0)
badFoodIT2MF = IntervalT2MF_Triangular("IT2MF for bad food",badFoodUMF,badFoodLMF)
badFoodMF = GenT2MF_Triangular("zGT2MF for bad food", primer = badFoodIT2MF, numberOfzLevels = numberOfzLevels)
badFood = GenT2_Antecedent("BadFood",badFoodMF, food)
lowTipUMF = T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0)
lowTipLMF = T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0)
lowTipIT2MF = IntervalT2MF_Gaussian("IT2MF for Low Tip",lowTipUMF,lowTipLMF)
lowTipMF = GenT2MF_Gaussian("zGT2MF for Low tip", lowTipIT2MF, numberOfzLevels)
lowTip =  GenT2_Consequent(  "LowTip",lowTipMF, tip )
unfriendlyServiceUMF = T1MF_Triangular("Upper MF for unfriendly service",0.0,0.0,8.0)
unfriendlyServiceLMF = T1MF_Triangular("Lower MF for unfriendly service",0.0,0.0,6.0)
unfriendlyServiceIT2MF = IntervalT2MF_Triangular("IT2MF for unfriendly service",unfriendlyServiceUMF,unfriendlyServiceLMF)
unfriendlyServiceMF = GenT2MF_Triangular("zGT2MF for unfriendly service", primer = unfriendlyServiceIT2MF, numberOfzLevels = numberOfzLevels)
unfriendlyService =  GenT2_Antecedent("UnfriendlyService",unfriendlyServiceMF, service)

highTipUMF = T1MF_Gaussian("Upper MF high tip", 30.0, 6.0)
highTipLMF = T1MF_Gaussian("Lower MF high tip", 30.0, 4.0)
highTipIT2MF = IntervalT2MF_Gaussian("IT2MF for high Tip",highTipUMF,highTipLMF) 
highTipMF = GenT2MF_Gaussian("zGT2MF for high tip", highTipIT2MF, numberOfzLevels)
highTip =  GenT2_Consequent("HighTip",highTipMF, tip )

r1 = GenT2_Rule([badFood, unfriendlyService], consequent = highTip)
r2 = GenT2_Rule([badFood, unfriendlyService], consequent = lowTip)
jac = JaccardSimilarity()
print(jac.getSimilarity(highTipMF,lowTipMF,10))
