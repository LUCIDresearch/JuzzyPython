"""
SimplezGT2FLSNSIT2_test.py
Created 9/3/2022
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimplezGT2FLSNSIT2 import SimplezGT2FLSNSIT2
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLSNSIT2Centroid.txt"
        test = SimplezGT2FLSNSIT2(unit=True)
        z = test.getControlSurfaceData(True,50,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLSNSIT2Height.txt"
        test = SimplezGT2FLSNSIT2(unit=True)
        z = test.getControlSurfaceData(False,50,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
