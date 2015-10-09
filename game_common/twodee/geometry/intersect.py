from game_common.twodee.geometry import (
                         calculate,
                         vector)

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
        
    
