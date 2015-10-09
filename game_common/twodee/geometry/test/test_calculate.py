import unittest

from twodee.geometry import calculate

class TestMultiplyVectorAndScalar(unittest.TestCase):
    def test_scalarIsZero_vectorIsZero(self):
        startVector = (1, 1)
        newVector =\
            calculate.multiplyVectorAndScalar(vector=startVector,
                                              scalar=0)
        self.assertEquals((0,0),
                          newVector)
        
    def test_scalarIsOne_vectorIsUnchanged(self):
        startVector = (2, 2)
        newVector =\
            calculate.multiplyVectorAndScalar(vector=startVector,
                                              scalar=1)
        self.assertEquals((2, 2),
                          newVector)
        
    def test_scalarIsTwo_vectorIsDoubled(self):
        startVector = (2, 2)
        newVector =\
            calculate.multiplyVectorAndScalar(vector=startVector,
                                              scalar=2)
        self.assertEquals((4, 4),
                          newVector)
        
    def test_scalarIsOneHalf_vectorIsHalved(self):
        startVector = (2, 2)
        newVector =\
            calculate.multiplyVectorAndScalar(vector=startVector,
                                              scalar=.5)
        self.assertEquals((1, 1),
                          newVector)
        
class TestAddVectors(unittest.TestCase):
    def test_twoZeroVectors_resultIsZero(self):
        vector1 = (0, 0)
        vector2 = (0, 0)
        result = calculate.addVectors(vector1,
                                      vector2)
        self.assertEquals((0, 0),
                          result)
        
    def test_twoVectorsOfOnes_resultIsVectorOfTwos(self):
        vector1 = (1, 1)
        vector2 = (1, 1)
        result = calculate.addVectors(vector1,
                                      vector2)
        self.assertEquals((2, 2),
                          result)
        
    def test_addPositiveAndNegativeVectors(self):
        vector1 = (2, 2)
        vector2 = (-1, -1)
        result = calculate.addVectors(vector1,
                                      vector2)
        self.assertEquals((1, 1),
                          result)
        
class TestAddPointAndVector(unittest.TestCase):
    def test_originPlusZero_stillOrigin(self):
        point = (0, 0)
        vector = (0, 0)
        resultPoint = calculate.addPointAndVector(point=point,
                                             vector=vector)
        self.assertEquals((0, 0),
                          resultPoint)
        
    def test_originPlusVector_pointBecomesEndpointOfVector(self):
        point = (0, 0)
        vector = (1, 1)
        resultPoint = calculate.addPointAndVector(point=point,
                                             vector=vector)
        self.assertEquals((1, 1),
                          resultPoint)
        
    def test_pointPlusVector(self):
        point = (1, 1)
        vector = (2, 2)
        resultPoint = calculate.addPointAndVector(point=point,
                                             vector=vector)
        self.assertEquals((3, 3),
                          resultPoint)
        
class TestSubtractPoints(unittest.TestCase):
    def test_originMinusOrigin_vectorIsZero(self):
        point1 = (0, 0)
        point2 = (0, 0)
        resultVector = calculate.subtractPoints(point1, 
                                                point2)
        self.assertEquals((0, 0),
                          resultVector)
        
    def test_pointMinusSamePoint_vectorIsZero(self):
        point1 = (1, 1)
        point2 = (1, 1)
        resultVector = calculate.subtractPoints(point1,
                                                point2)
        self.assertEquals((0, 0),
                          resultVector)
        
    def test_firstArgumentIsSmallerThanFirst_returnPositiveVector(self):
        point1 = (1, 1)
        point2 = (3, 3)
        resultVector = calculate.subtractPoints(point1,
                                                point2)
        self.assertEquals((-2, -2),
                          resultVector)
        
    def test_firstArgumentIsLargerThanFirst_returnNegativeVector(self):
        point1 = (3, 3)
        point2 = (1, 1)
        resultVector = calculate.subtractPoints(point1,
                                                point2)
        self.assertEquals((2, 2),
                          resultVector)
        
class TestSubtractVectors(unittest.TestCase):
    def test_twoZeroVectors_vectorIsZero(self):
        vector1 = (0, 0)
        vector2 = (0, 0)
        resultVector = calculate.subtractPoints(vector1, 
                                                vector2)
        self.assertEquals((0, 0),
                          resultVector)
        
    def test_vectorMinusSameVector_vectorIsZero(self):
        vector1 = (1, 1)
        vector2 = (1, 1)
        resultVector = calculate.subtractPoints(vector1,
                                                vector2)
        self.assertEquals((0, 0),
                          resultVector)
        
    def test_firstArgumentIsSmallerThanFirst_returnNegativeVector(self):
        vector1 = (1, 1)
        vector2 = (3, 3)
        resultVector = calculate.subtractPoints(vector1,
                                                vector2)
        self.assertEquals((-2, -2),
                          resultVector)
        
    def test_firstArgumentIsLargerThanFirst_returnPositiveVector(self):
        vector1 = (3, 3)
        vector2 = (1, 1)
        resultVector = calculate.subtractPoints(vector1,
                                                vector2)
        self.assertEquals((2, 2),
                          resultVector)

#In order for answers to be sensible, both vectors must be normalized.
class TestDotProduct(unittest.TestCase):
    def test_vectorsAreTheSame_dotProductIs1(self):
        vector1 = (1, 0)
        vector2 = (1, 0)
        dotProduct = calculate.dotProduct(vector1,
                                         vector2)
        self.assertEquals(1,
                          dotProduct)
        
    def test_plus90degrees_dotProductIs0(self):
        vector1 = (1, 0)
        vector2 = (0, 1)
        dotProduct = calculate.dotProduct(vector1,
                                         vector2)
        self.assertEquals(0,
                          dotProduct)
        
    def test_minus90degrees_dotProductIs0(self):
        vector1 = (1, 0)
        vector2 = (0, -1)
        dotProduct = calculate.dotProduct(vector1,
                                         vector2)
        self.assertEquals(0,
                          dotProduct)
        
    def test_vectorsAreFacingInOppositeDirections(self):
        vector1 = (1, 0)
        vector2 = (-1, 0)
        dotProduct = calculate.dotProduct(vector1,
                                          vector2)
        self.assertEquals(-1,
                          dotProduct)
        
class TestWithinTolerance(unittest.TestCase):
    def test_toleranceIsZero_withinTolerance(self):
        tolerance = 0
        value = 1
        threshold = 1
        withinTolerance = calculate.withinTolerance(value,
                                                    threshold,
                                                    tolerance)
        self.assertTrue(withinTolerance)
        
    def test_toleranceIsZero_aboveTolerance(self):
        tolerance = 0
        value = 1
        threshold = .9
        withinTolerance = calculate.withinTolerance(value,
                                                    threshold,
                                                    tolerance)
        self.assertFalse(withinTolerance)
        
    def test_toleranceIsZero_belowTolerance(self):
        tolerance = 0
        value = .9
        threshold = 1
        withinTolerance = calculate.withinTolerance(value,
                                                    threshold,
                                                    tolerance)
        self.assertFalse(withinTolerance)
        
