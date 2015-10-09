import numpy
import math

identity3 = numpy.identity(3, dtype=float)

def vectorToWorldSpace(vector,
                       localOrigin,
                       localDirection):
    vectorx, vectory = vector
    originx, originy = localOrigin
   
    c = math.cos(localDirection)
    s = math.sin(localDirection)
    
    identity = globals()['identity3']
    
    transform1 = identity.copy()
    transform2 = identity.copy()
    rotate = identity.copy()
    
    transform1[2][0] = -originx
    transform1[2][1] = -originy
    transform2[2][0] = originx
    transform2[2][1] = originy
    rotate[0][0] = c
    rotate[1][0] = -s
    rotate[0][1] = s
    rotate[1][1] = c
    
    newvector = [vectorx, vectory, 0]
    newvector = numpy.dot(newvector, rotate)
    
    return (round(newvector[0], 4), round(newvector[1], 4))


def pointToWorldSpace(point,
                      localOrigin,
                      localDirection):
    [x, y] = point
    [ox, oy] = localOrigin
    
    c = math.cos(localDirection)
    s = math.sin(localDirection)
    
    transform = numpy.array([[c, s, 0],
                             [-s, c, 0],
                             [ox, oy, 1]])
    
    
    localpoint = [x, y, 1]
    worldpoint = numpy.dot(localpoint, transform)
    
    newpoint = (round(worldpoint[0], 4), round(worldpoint[1], 4))

    return newpoint

def pointToLocalSpace(point,
                      localOrigin,
                      localDirection):
    pointx, pointy = point
    originx, originy = localOrigin
    
    c = math.cos(localDirection)
    s = math.sin(localDirection)
    
    identity = globals()['identity3']
    
    transform1 = identity.copy()
    rotate = identity.copy()
    
    transform1[2][0] = -originx
    transform1[2][1] = -originy
    rotate[0][0] = c
    rotate[1][0] = s
    rotate[0][1] = -s
    rotate[1][1] = c
    
    
       
    newpoint = [pointx, pointy, 1]
    
    
    #Do the rotation...
    
    newpoint = numpy.dot(newpoint, transform1)
    newpoint = numpy.dot(newpoint, rotate)
    
    #Then move the point by the offset of the local space origin from the world space origin
    return (round(newpoint[0], 4), round(newpoint[1], 4))
