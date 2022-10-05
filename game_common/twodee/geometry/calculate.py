'''Calculation functionality for 2D vectors and points.'''

import math


from game_common.twodee.geometry import vector

def multiplyVectorAndScalar(vector,
                            scalar):
    (x, y) = vector
    return (x * scalar, y * scalar)

def addVectors(*vectors):
    totalx, totaly = (0, 0)
    for (vectorx, vectory) in vectors:
        totalx += vectorx
        totaly += vectory
    return (totalx, totaly)

def addPointAndVector(point,
                      vector):
    (pointx, pointy) = point
    (vectorx, vectory) = vector
    return (pointx + vectorx, pointy + vectory)

def subtractPoints(point1,
                   point2):
    (point1x, point1y) = point1
    (point2x, point2y) = point2
    return (point1x - point2x,
            point1y - point2y)
    
def subtractVectors(vector1,
                    vector2):
    (vector1x, vector1y) = vector1
    (vector2x, vector2y) = vector2
    return (vector1x - vector2x,
            vector1y - vector2y)
    
def dotProduct(vector1, 
               vector2):
    vector1x, vector1y = vector1
    vector2x, vector2y = vector2
    return (vector1x * vector2x + vector1y * vector2y)

def normalizedDotProduct(vector1,
                         vector2):
    vector1 = vector.normalize(vector1)
    vector2 = vector.normalize(vector2)
    return dotProduct(vector1,
                      vector2)

def withinTolerance(value,
                    threshold,
                    tolerance):
    distance = abs(threshold - value)
    if distance <= tolerance:
        return True
    else:
        return False


    
def pointToWorldSpace(local_point, agent_point, agent_direction):
    [local_x, local_y] = local_point.getXAndY()
    [origin_x, origin_y] = agent_point.getXAndY()
    
    direction = math.radians(agent_direction)
    c = math.cos(direction)
    s = math.sin(direction)
    
    identity = globals()['identity3']
    
    transform2 = identity.copy()
    rotate = identity.copy()
    
    transform2[2][0] = origin_x
    transform2[2][1] = origin_y
    rotate[0][0] = c
    rotate[1][1] = c
    rotate[0][1] = s
    rotate[1][0] = -s

    newpoint = [local_x, local_y, 1]
    newpoint = numpy.dot(newpoint, rotate)
    newpoint = numpy.dot(newpoint, transform2)
    newpoint = [round(newpoint[0], 4), round(newpoint[1], 4)]

    return newpoint

def getMagnitudeSquared(vector):
    x = vector.getX()
    y = vector.getY()
    return x * x + y * y
    

def addPoints(point1, point2, resultant_point=None):
    (x1, y1) = point1.getXAndY()
    (x2, y2) = point2.getXAndY()
    
    if resultant_point == None:
        print("AddPoints: Instantiating New Point to Return")
        return Point(x1 + x2, y1 + y2)
    else:
        resultant_point.setXAndY(x1 + x2, y1 + y2)
        return resultant_point
    
def averagePoints(point1, point2, resultant_point=None):
    (x1, y1) = point1.getXAndY()
    (x2, y2) = point2.getXAndY()
    
    if resultant_point == None:
        print("AveragePoints: Instantiating New Point to Return")
        return Point((x1 + x2) / 2.0, (y1 + y2) / 2.0)
    else:
        resultant_point.setXAndY((x1 + x2) / 2.0, (y1 + y2) / 2.0)
        return resultant_point
    
    
    
