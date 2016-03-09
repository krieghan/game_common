from game_common.twodee.geometry import (
                         calculate,
                         vector)

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
        
    
