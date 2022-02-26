import sys

sys.path.append("..")
from generalType2zSlices.sets.GenT2MF_Triangular import GenT2MF_Triangular
from generalType2zSlices.sets.GenT2MF_Union import GenT2MF_Union
from generalType2zSlices.system.GenT2Engine_Union import GenT2Engine_Union
from intervalType2.sets.IntervalT2MF_Triangular import IntervalT2MF_Triangular
from type1.sets.T1MF_Discretized import T1MF_Discretized
from type1.sets.T1MF_Union import T1MF_Union
from type1.sets.T1MF_Singleton import T1MF_Singleton
from type1.sets.T1MF_Triangular import T1MF_Triangular
from type1.sets.T1MF_Trapezoidal import T1MF_Trapezoidal
from type1.sets.T1MF_Meet import T1MF_Meet
from generic.Tuple import Tuple

#test = T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,16),Tuple(9,50)])
#print(test.writeToFileHighRes("test.txt",10))
#test = T1MF_Union(T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]),T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]))
#print(test.getSupport().toString())
#test = T1MF_Trapezoidal("test",[1.0,2.0,3.0,4.0])
#test = T1MF_Meet(T1MF_Discretized("Test",[Tuple(0,5),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]),T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,18),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]))
#print(test.findMax(T1MF_Trapezoidal("test",[1.0,2.0,3.0,4.0])))
inputlmf = T1MF_Triangular("inputlmf",1,0,7)
inputumf = T1MF_Triangular("inputumf",0,8,15)
inputMfprimer = IntervalT2MF_Triangular("inputmfprimer",inputumf,inputlmf)
inputMf = GenT2MF_Triangular("inputmf",inputMfprimer,numberOfzLevels=4)
test = GenT2Engine_Union()
uni = test.getUnion(inputMf,inputMf)
print(uni.getFS(5).toString())

