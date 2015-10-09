from game_common.twodee.geometry.constants import RADIANS45
from game_common.twodee.geometry import (
                         calculate,
                         intersect,
                         vector)

def avoidwalls(agent, 
               walls):
    if not walls:
        return (0, 0)
    agentPosition = agent.getPosition()
    feelers = createFeelers(agent)
    
    closestWall = None
    closestIntersection = None
    distanceSquaredToClosestIntersection = None
    closestFeeler = None

    for feeler in feelers:
        for wall in walls:
            intersectPoint = intersect.lineWithLine(feeler,
                                                    wall)
            if intersectPoint is None:
                continue
            agentToIntersection = calculate.subtractPoints(intersectPoint,
                                                           agentPosition)
            distanceSquaredToIntersection = vector.getMagnitudeSquared(agentToIntersection)
        
            if closestIntersection is None or distanceSquaredToIntersection < distanceSquaredToClosestIntersection:
                distanceSquaredToClosestIntersection = distanceSquaredToIntersection
                closestWall = wall
                closestIntersection = intersectPoint
                closestFeeler = feeler
                
    if closestWall is None:
        return (0, 0)            
    
    (closestFeelerOrigin,
     closestFeelerEndpoint) = closestFeeler
    (wallOrigin,
     wallEndpoint) = closestWall
    wallVector = calculate.subtractPoints(wallEndpoint,
                                          wallOrigin)
    intersectionToFeelerEndpoint = calculate.subtractPoints(closestFeelerEndpoint,
                                                            closestIntersection)
    overshootLength = vector.getMagnitude(intersectionToFeelerEndpoint)
    normalizedWallVector = vector.normalize(wallVector)
    wallNormal = vector.getPerpVector(normalizedWallVector)
    steeringForce = calculate.multiplyVectorAndScalar(wallNormal,
                                                      overshootLength)
    
    return steeringForce

def createFeelers(agent):
    agentPosition = agent.getPosition()
    agentDirection = agent.getDirectionRadians()
    agentLength = agent.getLength()
    feelerLength = agentLength * 1.5
    
    leftVector = vector.createVector(magnitude=feelerLength,
                                     direction=agentDirection + RADIANS45)
    forwardVector = vector.createVector(magnitude=feelerLength,
                                        direction=agentDirection)
    rightVector = vector.createVector(magnitude=feelerLength,
                                      direction=agentDirection - RADIANS45)
    
    leftPoint = calculate.addPointAndVector(agentPosition,
                                            leftVector)
    forwardPoint = calculate.addPointAndVector(agentPosition,
                                               forwardVector)
    rightPoint = calculate.addPointAndVector(agentPosition,
                                             rightVector)
    
    leftLine = (agentPosition, leftPoint)
    forwardLine = (agentPosition, forwardPoint)
    rightLine = (agentPosition, rightPoint)
    
    return (leftLine, forwardLine, rightLine)

