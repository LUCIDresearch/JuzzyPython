"""
SimplezGT2FLS_test.py
Created 9/3/2022
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimplezGT2FLS import SimplezGT2FLS
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLSCentroid.txt"
        test = SimplezGT2FLS(unit=True)
        z = test.getControlSurfaceData(True,50,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimplezGT2FLSHeight.txt"
        test = SimplezGT2FLS(unit=True)
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
