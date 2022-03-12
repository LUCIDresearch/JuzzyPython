"""
SimpleNST1IT2FLSut.py
Created 27/12/2021
"""
import sys
import numpy as np
import unittest
from juzzyPython.examples.SimpleNST1IT2FLS import SimpleNST1IT2FLS
import logging
import sys
class TestSimpleT2FLS(unittest.TestCase):

    def testCentroidDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNST1IT2FLSCentroid.txt"
        test = SimpleNST1IT2FLS(unit=True)
        z = test.getControlSurfaceData(True,100,100,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),9) for line in lines]
        z = [round(i,9) for i in z]
        self.assertEqual(z,lines)
    
    def testCOSDefuzz(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleNST1IT2FLSCOS.txt"
        test = SimpleNST1IT2FLS(unit=True)
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
