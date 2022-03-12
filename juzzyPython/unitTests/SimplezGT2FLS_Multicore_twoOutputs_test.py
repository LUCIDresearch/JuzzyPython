"""
SimplezGT2FLS_Multicore_twoOutputs_test.py
Created 9/3/2022
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimplezGT2FLS_multicore_twoOutputs import SimplezGT2FLS_multicore_twoOutputs
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLS_Multicore_twoOutputsCentroid.txt"
        test =  SimplezGT2FLS_multicore_twoOutputs(unit=True)
        z = test.getControlSurfaceData(test.getTipObject(),True,100,100,True)
        y = test.getControlSurfaceData(test.getSmileObject(),True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        y = [round(i,10) for i in y]
        self.assertEqual(z+y,lines)
    
    def testHeightDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLS_Multicore_twoOutputsHeight.txt"
        test =  SimplezGT2FLS_multicore_twoOutputs(unit=True)
        z = test.getControlSurfaceData(test.getTipObject(),False,100,100,True)
        y = test.getControlSurfaceData(test.getSmileObject(),False,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        y = [round(i,10) for i in y]
        self.assertEqual(z+y,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
