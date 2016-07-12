import unittest

import zope.interface

from game_common.twodee.geometry import intersect
from game_common import interfaces

class TestLineSegmentWithLineSegment(unittest.TestCase):
    def test_twoParallelLines(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((-1, 1), (1, 1))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals(None,
                          intersectionPoint)
        
    def test_twoLineSegmentsThatDoNotIntersect(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((5, -1), (5, 1))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals(None,
                          intersectionPoint)
        
    def test_twoLinesIntersectAtOrigin(self):
        line1 = ((-1, 0), (1, 0))
        line2 = ((0, -1), (0, 1))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals((0, 0),
                          intersectionPoint)
        
    def test_twoLinesIntersectAtOneOne(self):
        line1 = ((0, 1), (2, 1))
        line2 = ((1, 0), (1, 2))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals((1, 1),
                          intersectionPoint)
        
    def test_twoLinesOfUnequalLength(self):
        line1 = ((0, 0), (100, 0))
        line2 = ((50, 1), (50, -1))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals((50, 0),
                          intersectionPoint)
        
    def test_twoDiagonals(self):
        line1 = ((-1, -1), (1, 1))
        line2 = ((-1, 1), (1, -1))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertEquals((0, 0),
                          intersectionPoint)
        
    def test_1(self):
        line1 = ((338, 1188), (342, 1248))
        line2 = ((25, 1225), (1255, 1225))
        intersectionPoint = intersect.getLineSegmentIntersection(line1,
                                                   line2)
        self.assertTrue(intersectionPoint)

class StubAgentWithBoundaries(object):
    zope.interface.implements(
            [interfaces.Collideable])

    def __init__(self, boundaries, direction, position):
        self.boundaries = boundaries
        self.direction = direction
        self.position = position

    def getBoundaries(self):
        return self.boundaries

    def getDirection(self):
        return self.direction

    def getPosition(self):
        return self.position

    def handleCollision(self, otherElement):
        pass
    

class RectangleCollidesWithRectangle(unittest.TestCase):
    def test_identical_rectangles_collide(self):
        rect_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(0, 0))
        rect_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(0, 0))
        self.assertTrue(intersect.collidesWith(
                            rect_agent1, 
                            rect_agent2))


    def test_two_rectangles_collide(self):
        rect_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(0, 0))
        rect_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(1, 1))
        self.assertTrue(intersect.collidesWith(
                            rect_agent1, 
                            rect_agent2))

    def test_two_rectangles_do_not_collide(self):
        rect_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(0, 0))
        rect_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (0, 0),
                                (1, 0),
                                (1, 1),
                                (0, 1))},
                direction=0,
                position=(2, 2))
        self.assertFalse(intersect.collidesWith(
                            rect_agent1, 
                            rect_agent2))

class CircleCollidesWithCircle(unittest.TestCase):
    def test_identical_circles_collide(self):
        circle_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 0))
        circle_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 0))
        self.assertTrue(intersect.collidesWith(
                            circle_agent1, 
                            circle_agent2))
         
    def test_two_circles_collide(self):
        circle_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 0))
        circle_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, .5))
        self.assertTrue(intersect.collidesWith(
                            circle_agent1, 
                            circle_agent2))

    def test_two_circles_dont_collide(self):
        circle_agent1 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 0))
        circle_agent2 = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 2))
        self.assertFalse(intersect.collidesWith(
                            circle_agent1, 
                            circle_agent2))

class PolygonCollidesWithPolygon(unittest.TestCase):
    def test_identical_octagons_collide(self):
        oct_agent1 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, 0))
        oct_agent2 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, 0))
        self.assertTrue(intersect.collidesWith(
                            oct_agent1, 
                            oct_agent2))

    def test_two_octagons_collide(self):
        oct_agent1 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, 0))
        oct_agent2 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, .5))
        self.assertTrue(intersect.collidesWith(
                            oct_agent1, 
                            oct_agent2))

    def test_two_octagons_dont_collide(self):
        oct_agent1 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, 0))
        oct_agent2 = StubAgentWithBoundaries(
            boundaries={intersect.Polygon : (intersect.makePolygonFromPoints(
                                                [(1, 2),
                                                 (2, 1),
                                                 (2, -1),
                                                 (1, -2),
                                                 (-1, -2),
                                                 (-2, -1),
                                                 (-2, 1),
                                                 (-1, 2)]))},
            direction=0,
            position=(0, 14))
        self.assertFalse(intersect.collidesWith(
                            oct_agent1, 
                            oct_agent2))

class CircleCollidesWithRectangle(unittest.TestCase):
    def test_circle_inside_rectangle(self):
        rect_agent = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (-100, 100),
                                (100, 100),
                                (100, -100),
                                (-100, -100))},
                direction=0,
                position=(0, 0))
        circle_agent = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 0))
        self.assertTrue(intersect.collidesWith(
                            circle_agent,
                            rect_agent))

    def test_rectangle_inside_circle(self):
        rect_agent = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (-1, 1),
                                (1, 1),
                                (1, -1),
                                (-1, -1))},
                direction=0,
                position=(0, 0))
        circle_agent = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 100)},
                direction=0,
                position=(0, 0))
        self.assertTrue(intersect.collidesWith(
                            circle_agent,
                            rect_agent))

    def test_circle_collides_with_rectangle(self):
        rect_agent = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (-1, 1),
                                (1, 1),
                                (1, -1),
                                (-1, -1))},
                direction=0,
                position=(0, 0))
        circle_agent = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 1))
        self.assertTrue(intersect.collidesWith(
                            circle_agent,
                            rect_agent))

    def test_circle_doesnot_collide_with_rectangle(self):
        rect_agent = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (-1, 1),
                                (1, 1),
                                (1, -1),
                                (-1, -1))},
                direction=0,
                position=(0, 0))
        circle_agent = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 10))
        self.assertFalse(intersect.collidesWith(
                            circle_agent,
                            rect_agent))

    def test_rectangle_collides_with_circle(self):
        rect_agent = StubAgentWithBoundaries(
                boundaries={intersect.Rectangle : (
                                (-1, 1),
                                (1, 1),
                                (1, -1),
                                (-1, -1))},
                direction=0,
                position=(0, 0))
        circle_agent = StubAgentWithBoundaries(
                boundaries={intersect.Circle : ((0, 0), 1)},
                direction=0,
                position=(0, 1))
        self.assertTrue(intersect.collidesWith(
                            rect_agent,
                            circle_agent))


class LineSegmentsOverlap(unittest.TestCase):
    def test_they_overlap(self):
        self.assertTrue(intersect.lineSegmentsOverlap(
            ((0, 0), (0, 2)),
            ((0, 1), (0, 3))))

    def test_joined_segments(self):
        self.assertTrue(intersect.lineSegmentsOverlap(
            ((0, 0), (0, 1)),
            ((0, 1), (0, 2))))

    def test_they_do_not_overlap(self):
        self.assertFalse(intersect.lineSegmentsOverlap(
            ((0, 0), (0, 1)),
            ((0, 2), (0, 3))))

