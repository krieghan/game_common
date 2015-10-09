import unittest

from twodee.geometry import intersect

class TestLineWithLine(unittest.TestCase):
    def test_twoParallelLines(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((-1, 1), (1, 1))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals(None,
                          intersectionPoint)
        
    def test_twoLineSegmentsThatDoNotIntersect(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((5, -1), (5, 1))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals(None,
                          intersectionPoint)
        
    def test_twoLinesIntersectAtOrigin(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((0, -1), (0, 1))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals((0, 0),
                          intersectionPoint)
        
    def test_twoLinesIntersectAtOneOne(self):
        line1 = ((0, 1), (2, 1))
        line2 = ((1, 0), (1, 2))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals((1, 1),
                          intersectionPoint)
        
    def test_twoLinesOfUnequalLength(self):
        line1 = ((0, 0), (100, 0))
        line2 = ((50, 1), (50, -1))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals((50, 0),
                          intersectionPoint)
        
    def test_twoDiagonals(self):
        line1 = ((-1, -1), (1, 1))
        line2 = ((-1, 1), (1, -1))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertEquals((0, 0),
                          intersectionPoint)
        
    def test_1(self):
        line1 = ((338, 1188), (342, 1248))
        line2 = ((25, 1225), (1255, 1225))
        intersectionPoint = intersect.lineWithLine(line1,
                                                   line2)
        self.assertTrue(intersectionPoint)
        
        
        
        