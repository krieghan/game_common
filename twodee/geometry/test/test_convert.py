import math
import unittest

from twodee.geometry import convert

class TestPointToLocalSpace(unittest.TestCase):
    def test_localSpaceIsWorldSpace_pointIsTheSame(self):
        newPoint = convert.pointToLocalSpace(point=(1, 1),
                                             localOrigin=(0, 0),
                                             localDirection=0)
        self.assertEquals((1, 1),
                          newPoint)
        
    def test_pointIsOnLocalSpaceOrigin_pointIsZero(self):
        newPoint = convert.pointToLocalSpace(point=(1, 1),
                                             localOrigin=(1, 1),
                                             localDirection=0)
        self.assertEquals((0, 0),
                          newPoint)
        
    def test_pointIsOneAwayFromLocalSpaceOrigin_pointIsOne(self):
        newPoint = convert.pointToLocalSpace(point=(2, 2),
                                             localOrigin=(1, 1),
                                             localDirection=0)
        self.assertEquals((1, 1),
                          newPoint)
        
    def test_localSpaceIsRotated90Degrees(self):
        newPoint = convert.pointToLocalSpace(point=(1, 0),
                                             localOrigin=(0, 0),
                                             localDirection=math.pi / 2)
        self.assertEquals((0, -1),
                          newPoint)
        
class TestVectorToWorldSpace(unittest.TestCase):
    def test_localSpaceIsWorldSpace_vectorIsTheSame(self):
        newVector = convert.vectorToWorldSpace(vector=(1, 1),
                                               localOrigin=(0, 0),
                                               localDirection=0)
        self.assertEquals((1, 1),
                          newVector)
        
    def test_localSpaceIsOnlyTranslated_vectorIsTheSame(self):
        newVector = convert.vectorToWorldSpace(vector=(1, 1),
                                               localOrigin=(2, 2),
                                               localDirection=0)
        self.assertEquals((1, 1),
                          newVector)
        
    def test_localSpaceIsRotated90Degrees_vectorIsRotated90Degrees(self):
        newVector = convert.vectorToWorldSpace(vector=(1, 0),
                                               localOrigin=(0, 0),
                                               localDirection=math.pi / 2)
        self.assertEquals((0, 1),
                          newVector)
        
    def test_localSpaceIsTranslatedAndRotated_vectorIsRotated(self):
        newVector = convert.vectorToWorldSpace(vector=(2, 0),
                                               localOrigin=(0, 1),
                                               localDirection=math.pi / 2)
        self.assertEquals((0, 2),
                          newVector)
        
class TestPointToWorldSpace(unittest.TestCase):
    def test_worldSpaceIsLocalSpace_pointIsTheSame(self):
        newPoint = convert.pointToWorldSpace(point=(1, 1),
                                             localOrigin=(0, 0),
                                             localDirection=0)
        self.assertEquals((1, 1),
                          newPoint)
        
    def test_localSpaceIsTranslated_pointIsTranslated(self):
        newPoint = convert.pointToWorldSpace(point=(1, 1),
                                             localOrigin=(1, 1),
                                             localDirection=0)
        self.assertEquals((2, 2),
                          newPoint)
        
    def test_localSpaceIsRotated_pointIsRotated(self):
        newPoint = convert.pointToWorldSpace(point=(1, 0),
                                             localOrigin=(0, 0),
                                             localDirection=math.pi / 2)
        self.assertEquals((0, 1),
                          newPoint)
        
    def test_localSpaceIsTranslatedAndRotated_pointIsTranslatedAndRotated(self):
        newPoint = convert.pointToWorldSpace(point=(1, 0),
                                             localOrigin=(1, 0),
                                             localDirection=math.pi / 2)
        self.assertEquals((1, 1),
                          newPoint)
        
    def test_2(self):
        newPoint = convert.pointToWorldSpace(point=(1, -1),
                                             localOrigin=(1, 1),
                                             localDirection=math.pi / 2)
        self.assertEquals((2, 2), newPoint)
        
    def test_3(self):
        newPoint = convert.pointToWorldSpace(point=(1, -1),
                                             localOrigin=(1, 1),
                                             localDirection=-math.pi / 4)
        self.assertEquals((0, 0), newPoint)
        
