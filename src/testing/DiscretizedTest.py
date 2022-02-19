import sys
sys.path.append("..")

from type1.sets.T1MF_Discretized import T1MF_Discretized
from generic.Tuple import Tuple

test = T1MF_Discretized("Test",[Tuple(0,10),Tuple(5,16),Tuple(10,20),Tuple(2,30),Tuple(4,18),Tuple(9,50)])
print(test.writeToFileHighRes("test.txt",10))