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
from generic.Tuple import Tuple

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
inte =  inter.getIntersection(lowTipMF,lowTipMF)
print(inte.toString())
#print(defuzz.typeReduce_standard(lowTipMF,4,4))
#print(cyl.getFS(4).toString())

