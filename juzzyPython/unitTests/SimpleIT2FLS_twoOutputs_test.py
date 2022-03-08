"""
SimpleIT2FLS_twoOutputsUt.py
Created 27/12/2021
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimpleIT2FLS_twoOutputs import SimpleIT2FLS_twoOutputs
import logging

class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleIT2FLS_twoOutputsTipCentroid.txt"
        test = SimpleIT2FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getTip(),True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testCOSDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleIT2FLS_twoOutputsTipCOS.txt"
        test = SimpleIT2FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getTip(),False,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testCentroidDefuzzSmile(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleIT2FLS_twoOutputsSmileCentroid.txt"
        test = SimpleIT2FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getSmile(),True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testCOSDefuzzSmile(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleIT2FLS_twoOutputsSmileCOS.txt"
        test = SimpleIT2FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getSmile(),False,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
