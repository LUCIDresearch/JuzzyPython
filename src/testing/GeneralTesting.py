import sys
sys.path.append("..")

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
test = T1MF_Meet(T1MF_Discretized("Test",[Tuple(0,5),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]),T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,18),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)]))
print(test.findMax(T1MF_Trapezoidal("test",[1.0,2.0,3.0,4.0])))