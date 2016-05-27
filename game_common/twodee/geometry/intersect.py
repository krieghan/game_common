import math

from game_common.twodee.geometry import (
                         calculate,
                         convert,
                         vector)

class Circle:
    pass

class Rectangle:
    pass

class Polygon:
    pass

    
def collidesWith(canvasElement, otherCanvasElement):
    intersects = None

    boundaries = canvasElement.getBoundaries()
    other_boundaries = otherCanvasElement.getBoundaries()

    if not boundaries or not other_boundaries:
        return False

    if (Circle in boundaries.keys() and 
        Circle in other_boundaries.keys()):
        boundary_in_world_space =\
                convertCircleToWorldSpace(canvasElement)
        other_boundary_in_world_space =\
                convertCircleToWorldSpace(otherCanvasElement)

        intersects = circleWithCircle(
                boundary_in_world_space,
                other_boundary_in_world_space)
        if not intersects:
            return False

    if (Rectangle in boundaries.keys() and 
        Rectangle in other_boundaries.keys()):
        boundary_in_world_space =\
            convertRectangleToWorldSpace(canvasElement)
        other_boundary_in_world_space =\
            convertRectangleToWorldSpace(otherCanvasElement)

        intersects = circleWithCircle(
                boundary_in_world_space,
                other_boundary_in_world_space)
        if not intersects:
            return False

    if (Polygon in boundaries.keys() and
        Polygon in other_boundaries.keys()):
        boundary_in_world_space =\
            convertPolygonToWorldSpace(canvasElement)
        other_boundary_in_world_space =\
            convertPolygonToWorldSpace(otherCanvasElement)

        intersects = polygonWithPolygon(
                boundary_in_world_space,
                other_boundary_in_world_space)
        if not intersects:
            return False

    if Circle in boundaries.keys() and Rectangle in other_boundaries.keys():
        boundary_in_world_space =\
            convertCircleToWorldSpace(canvasElement)
        other_boundary_in_world_space =\
            convertRectangleToWorldSpace(otherCanvasElement)

        intersects = circleWithRectangle(
                boundary_in_world_space,
                other_boundary_in_world_space)
        if not intersects:
            return False

    if Rectangle in boundaries.keys() and Circle in other_boundaries.keys():
        boundary_in_world_space =\
            convertRectangleToWorldSpace(canvasElement)
        other_boundary_in_world_space =\
            convertCircleToWorldSpace(otherCanvasElement)

        intersects = circleWithRectangle(
                other_boundary_in_world_space,
                boundary_in_world_space)
        if not intersects:
            return False

    if intersects is None:
        raise NotImplementedError("%s and %s" % (boundaries, other_boundaries))

    return intersects
        
def circleWithRectangle(circle, rectangle):
    return circleWithPolygon(
                circle,
                getRectangleLineSegments(rectangle))

def rectangleWithPolygon(rectangle, polygon):
    return polygonWithPolygon(
            getRectangleLineSegments(rectangle),
            polygon)

def circleWithPolygon(circle, polygon):
    for line_segment in polygon:
        if lineSegmentWithCircle(
                line_segment,
                circle):
            return True
    return False

def lineSegmentWithPolygon(line_segment, polygon):
    for polygon_line_segment in polygon:
        if lineSegmentWithLineSegment(
                polygon_line_segment,
                line_segment):
            return True

    return False

def lineWithCircle(line, circle):
    circle_point, circle_radius = circle
    line_point1, line_point2 = line
    a = calculate.subtractPoints(circle_point, line_point1)
    b = calculate.subtractPoints(line_point2, line_point1)
    left_perpendicular = vector.getLeftPerpendicular(b)  

    # Project a onto the left perpendicular vector
    a_onto_left_perpendicular = calculate.dotProduct(
            a, 
            vector.normalize(left_perpendicular))
    return math.pow(a_onto_left_perpendicular, 2) < math.pow(circle_radius, 2)
    

def lineSegmentWithCircle(line_segment, circle):
    if not lineWithCircle(line_segment, circle):
        return False

    circle_point, circle_radius = circle
    line_seg_point1, line_seg_point2 = line_segment

    # Line to circle vector (pick an endpoint)
    a = calculate.subtractPoints(circle_point, line_seg_point1)
    # Line segment vector
    b = calculate.subtractPoints(line_seg_point2, line_seg_point1)
    
    # a is the vector from line_point1 and the circle's center-point
    # b is the vector from line_point1 to line_point2
    # If a and b are pointing in opposing directions, then there is 
    # no intersection
    if calculate.dotProduct(a, b) <= 0:
        return False

    # Project a onto b.  If this projection is longer than the 
    # length of the line segment, then there is no intersection
    a_onto_b = calculate.dotProduct(a, vector.normalize(b))
    return math.pow(a_onto_b, 2) <= vector.getMagnitudeSquared(b)

def lineSegmentWithRectangle(line_segment, rectangle):
    return lineSegmentWithPolygon(
            line_segment,
            getRectangleLineSegments(rectangle))

def pointInCircle(point, circle):
    circle_point, circle_radius = circle
    point_to_circle = calculate.subtractPoints(circle_point, point)
    return vector.getMagnitudeSquared(point_to_circle) <= math.pow(circle_radius, 2)

def pointInRectangle(point, rectangle):
    a, b, c, d = rectangle
    ap = calculate.subtractPoints(point, a)
    ab = calculate.subtractPoints(b, a)
    ad = calculate.subtractPoints(d, a)
    return (
        0 <= calculate.dotProduct(ap, ab) <= calculate.dotProduct(ab, ab) and
        0 <= calculate.dotProduct(ap, ad) <= calculate.dotProduct(ad, ad))


def circleWithCircle(circle1, circle2):
    position_1, radius_1 = circle1
    position_2, radius_2 = circle2
    circle1_to_circle2 = calculate.subtractPoints(position_2, position_1)
    bounding_distance_squared = (radius_1 ** 2) + (radius_2 ** 2)
    actual_distance_squared = vector.getMagnitudeSquared(
            circle1_to_circle2)
    return actual_distance_squared < bounding_distance_squared

def rectangleWithRectangle(rectangle1, rectangle2):
    a1, b1, c1, d1 = rectangle1
    a2, b2, c2, d2 = rectangle2

    if (a1[0] > c2[0] or 
        a2[0] > c1[0]):
        return False

    if (a1[1] < c2[1] or 
        a2[1] < c1[1]):
        return False

    return True

def polygonWithPolygon(polygon1, polygon2):
    for line_from_1 in polygon1:
        for line_from_2 in polygon2:
            if lineWithLine(line_from_1, line_from_2) is not None:
                return True

    return False

def lineSegmentWithLineSegment(line1, line2):
    A, B = line1
    C, D = line2
    bVector = calculate.subtractPoints(B, A)
    dVector = calculate.subtractPoints(D, C)
    cVector = calculate.subtractPoints(C, A)
    
    bperp = vector.getPerpVector(bVector)
    dperp = vector.getPerpVector(dVector)
    
    dperpDotB = calculate.dotProduct(dperp,
                                     bVector)
    dperpDotC = calculate.dotProduct(dperp,
                                     cVector)
    bperpDotC = calculate.dotProduct(bperp,
                                     cVector)
    
    #The lines are parallel.  
    if dperpDotB == 0:
        return None
    
    distanceAlongB = float(dperpDotC) / float(dperpDotB)
    distanceAlongD = float(bperpDotC) / float(dperpDotB)
    
    if (distanceAlongB > 0 and distanceAlongB < 1 and
        distanceAlongD > 0 and distanceAlongD < 1):
        
        AToIntersectionPoint = calculate.multiplyVectorAndScalar(bVector,
                                                                 distanceAlongB)
        intersectionPoint = calculate.addPointAndVector(A,
                                                        AToIntersectionPoint)
        return intersectionPoint
        
def convertCircleToWorldSpace(canvasElement):
    circle = canvasElement.getBoundaries().get(Circle)
    return (convert.pointToWorldSpace(
                circle[0],
                canvasElement.getPosition(),
                canvasElement.getDirection()),
            circle[1])

def convertRectangleToWorldSpace(canvasElement):
    rectangle = canvasElement.getBoundaries().get(Rectangle)
    return (convert.pointToWorldSpace(
                rectangle[0],
                canvasElement.getPosition(),
                canvasElement.getDirection()),
            convert.pointToWorldSpace(
                rectangle[1],
                canvasElement.getPosition(),
                canvasElement.getDirection()),
            convert.pointToWorldSpace(
                rectangle[2],
                canvasElement.getPosition(),
                canvasElement.getDirection()),
            convert.pointToWorldSpace(
                rectangle[3],
                canvasElement.getPosition(),
                canvasElement.getDirection()),

 )

def convertPolygonToWorldSpace(canvasElement):
    polygon = canvasElement.getBoundaries().get(Polygon)
    polygon_in_world_space = []
    for line in polygon:
        line_in_world_space = (
            convert.pointToWorldSpace(
                line[0],
                canvasElement.getPosition(),
                canvasElement.getDirection()),
            convert.pointToWorldSpace(
                line[1],
                canvasElement.getPosition(),
                canvasElement.getDirection()))
        boundary_in_world_space.append(line_in_world_space)
    return tuple(polygon_in_world_space)

def getRectangleLineSegments(rectangle):
    (a, b, c, d) = rectangle
    ab = (a, b)
    bc = (b, c)
    cd = (c, d)
    da = (d, a)
    return (ab, bc, cd, da)


