"""
SimpleT1FLS_twoOutputsUt.py
Created 22/12/2021
"""
import numpy as np
import unittest
from juzzyPython.examples.SimpleT1FLS_twoOutputs import SimpleT1FLS_twoOutputs
import logging

class TestSimpleNST1FLS(unittest.TestCase):
#NOTE all NaN are replaced by 0.0
    def testCentroidDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoTipCen.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(True,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoTipHeight.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(False,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testCentroidDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoTipCen.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getTip(),True,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzzTip(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoTipHeight.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getTip(),False,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testCentroidDefuzzSmile(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoSmileCen.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getSmile(),True,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
    def testHeightDefuzzSmile(self):
        log= logging.getLogger("Test")
        f = "../javaTestResults/SimpleT1FLS_twoSmileHeight.txt"
        test = SimpleT1FLS_twoOutputs()
        z = test.getControlSurfaceData(test.getSmile(),False,10,10,True)
        with open(f) as file:
            lines = file.readlines()
            lines = [round(float(line.rstrip()),10) for line in lines]
        z = [round(i,10) for i in z]
        self.assertEqual(z,lines)
    
if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
