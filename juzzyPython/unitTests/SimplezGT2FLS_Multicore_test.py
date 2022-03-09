"""
SimplezGT2FLS_Multicore_test.py
Created 9/3/2022
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimplezGT2FLS_multicore import SimplezGT2FLS_multicore
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLS_MulticoreCentroid.txt"
        test =  SimplezGT2FLS_multicore(unit=True)
        z = test.getControlSurfaceData(True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLS_MulticoreHeight.txt"
        test =  SimplezGT2FLS_multicore(unit=True)
        z = test.getControlSurfaceData(False,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
