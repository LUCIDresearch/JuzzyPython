"""
SimpleT1FLSut.py
Created 22/12/2021
"""
import sys
sys.path.append("..")
import numpy as np
import unittest
from examples.SimpleNST1FLS import SimpleNST1FLS
import logging

class TestSimpleNST1FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNST1FLSCentroid.txt"
        test = SimpleNST1FLS()
        z = test.getControlSurfaceData(True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNST1FLSHeight.txt"
        test = SimpleNST1FLS()
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
