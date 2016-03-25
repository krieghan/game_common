from game_common.twodee.geometry import (
                         calculate,
                         vector)

class Circle:
    pass

class Rectangle:
    pass

class Polygon:
    pass

    
def collidesWith(canvasElement, otherCanvasElement):
    intersects = False

    boundaries = canvasElement.getBoundaries()
    other_boundaries = otherCanvasElement.getBoundaries()

    if (Circle in boundaries.keys() and 
        Circle in other_boundaries.keys())
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
        Rectangle in other_boundaries.keys())
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
                boundary_in_world_space,
                other_boundary_in_world_space)
        if not intersects:
            return False
        
def circleWithRectangle(circle, rectangle):
    pass

def rectangleWithPolygon(rectangle, polygon):
    pass

def circleWithPolygon(circle, polygon):
    pass

def lineSegmentWithPolygon(line_segment, polygon):
    pass

def lineSegmentWithCircle(line_segment, circle):
    pass

def lineSegmentWithRectangle(line_segment, rectangle):
    pass

def pointInCircle(point, circle):
    pass

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
    circle1_to_circle2 = calculate.subtractPoints(circle2, circle1)
    bounding_distance_squared = (radius_1 ** 2) + (radius_2 ** 2)
    actual_distance_squared = vector.getMagnitudeSquared(
            circle1_to_circle2)
    return actual_distance_squared < bounding_distance_squared:

def rectangleWithRectangle(rectangle1, rectangle2):
    top_left_1, bottom_right_1 = rectangle1
    top_left_2, bottom_right_2 = rectangle2

    if (top_left_1[0] > bottom_right_2[0] or 
        top_left_2[0] > bottom_right_1[0]):
        return False

    if (top_left_1[1] < bottom_right_2[1] or 
        top_left_2[1] < bottom_right_1[1]):
        return False

    return True

def polygonWithPolygon(polygon1, polygon2):
    for line_from_1 in polygon1:
        for line_from_2 in polygon2:
            if lineWithLine(line_from_1, line_from_2) is not None:
                return True

    return False

def lineWithLine(line1, line2):
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
    
    #The lines are parallel.  Let's pretend they don't intersect
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
                canvasElement.getDirection()))

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

