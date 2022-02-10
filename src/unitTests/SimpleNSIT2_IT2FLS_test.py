"""
SimpleNSIT2_IT2FLSut.py
Created 27/12/2021
"""
import sys
sys.path.append("..")
import numpy as np
import unittest
from examples.SimpleNSIT2_IT2FLS import SimpleNSIT2_IT2FLS
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNSIT2_IT2FLSCentroid.txt"
        test = SimpleNSIT2_IT2FLS()
        z = test.getControlSurfaceData(True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),9) for line in lines]
        z = [round(i,9) for i in z]
        self.assertEqual(z,lines)
    
    def testCOSDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNSIT2_IT2FLSCOS.txt"
        test = SimpleNSIT2_IT2FLS()
        z = test.getControlSurfaceData(False,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),9) for line in lines]
        z = [round(i,9) for i in z]
        self.assertEqual(z,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
