import unittest

from twodee.geometry import vector


class TestNormalize(unittest.TestCase):
    def test_normalizeFive(self):
        startVector = (0, 5)
        newVector = vector.normalize(startVector)
        self.assertEquals((0, 1),
                          newVector)
        
    def test_normalizeOneHalf(self):
        startVector = (0, .5)
        newVector = vector.normalize(startVector)
        self.assertEquals((0, 1),
                          newVector)
        
    def test_normalizeZero(self):
        startVector = (0, 0)
        self.assertRaises(vector.InvalidVector,
                          vector.normalize,
                          startVector)
        
class TestGetPerpVector(unittest.TestCase):
    def test_positiveX_positiveY(self):
        startVector = (1, 0)
        perpVector = vector.getPerpVector(startVector)
        self.assertEquals((0, -1),
                          perpVector)
        
    def test_negativeX_negativeY(self):
        startVector = (-1, 0)
        perpVector = vector.getPerpVector(startVector)
        self.assertEquals((0, 1),
                          perpVector)
        
    def test_positiveY_negativeX(self):
        startVector = (0, 1)
        perpVector = vector.getPerpVector(startVector)
        self.assertEquals((1, 0),
                          perpVector)
        
    def test_negativeY_positiveX(self):
        startVector = (0, 1)
        perpVector = vector.getPerpVector(startVector)
        self.assertEquals((1, 0),
                          perpVector)
        
    def test_diagonal_xBecomesNegativeY_yBecomesPositiveX(self):
        startVector = (1, 2)
        perpVector = vector.getPerpVector(startVector)
        self.assertEquals((2, -1),
                          perpVector)


class TestTruncate(unittest.TestCase):
    def test_forceOneMaxFive_returnOne(self):
        startVector = (0, 1)
        newVector = vector.truncate(startVector,
                                    5)
        self.assertEquals((0, 1),
                          newVector)
        
    def test_forceFiveMasOne_returnOne(self):
        startVector = (0, 5)
        newVector = vector.truncate(startVector,
                                    1)
        self.assertEquals((0, 1),
                          newVector)

class TestGetMagnitude(unittest.TestCase):
    def test_allX(self):
        startVector = (5, 0)
        magnitude = vector.getMagnitude(startVector)
        self.assertEquals(5,
                          magnitude)
        
    def test_allY(self):
        startVector = (0, 5)
        magnitude = vector.getMagnitude(startVector)
        self.assertEquals(5,
                          magnitude)

class TestSetMagnitude(unittest.TestCase):
    def test_scaleOneToFive(self):
        startVector = (0, 1)
        newVector = vector.setMagnitude(startVector,
                                        5)
        self.assertEquals((0, 5),
                          newVector)
        
    def test_scaleTwoToFive(self):
        startVector = (0, 2)
        newVector = vector.setMagnitude(startVector,
                                        5)
        self.assertEquals((0, 5),
                          newVector)
        
    def test_scaleTenToFive(self):
        startVector = (0, 10)
        newVector = vector.setMagnitude(startVector,
                                        5)
        self.assertEquals((0, 5),
                          newVector)
        
