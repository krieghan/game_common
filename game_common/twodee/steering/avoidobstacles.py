import random
import math

from game_common.twodee.geometry import (
                      convert,
                      calculate,
                      vector)

def avoidobstacles(agent,
                   obstacles):
    agentPosition = agent.getPosition()
    agentDirectionRadians = agent.getDirectionRadians()
    (obstacleDetectionLength, 
     obstacleDetectionWidth) = agent.getObstacleDetectionDimensions()
    
    obstaclesInRange = _getObstaclesInRange(agent=agent,
                                            obstacles=obstacles)
    (closestObstacle,
     obstacleLocalPosition) = _getClosestObstacle(agent=agent,
                                                  obstaclesInRange=obstaclesInRange)
    
    if closestObstacle is None:
        return (0, 0)
    
    obstacleX, obstacleY = obstacleLocalPosition
    
    _colorObstacle(closestObstacle)
    
    multiplier = 1.0 + (obstacleDetectionLength - obstacleX) / obstacleDetectionLength
    brake_weight = .2
    forceInLocalSpace =\
        ((closestObstacle.getRadius() - obstacleX) * brake_weight,
         (closestObstacle.getRadius() - obstacleY) * multiplier)
    
    forceInWorldSpace =\
         convert.vectorToWorldSpace(forceInLocalSpace, 
                                    agentPosition, 
                                    agentDirectionRadians)
    return forceInWorldSpace


def _colorObstacle(closestObstacle):
    newColor = (random.random(), random.random(), random.random())
    closestObstacle.setColor(newColor)


def _getObstaclesInRange(agent,
                         obstacles):
    inRange = []
    agentPosition = agent.getPosition()
    (obstacleDetectionLength,
     obstacleDetectionWidth) = agent.getObstacleDetectionDimensions()
    for obstacle in obstacles:
        parentToObstacle =\
            calculate.subtractPoints(obstacle.getPosition(),
                                     agentPosition)
        if (vector.getMagnitude(parentToObstacle) <= 
            obstacleDetectionLength + obstacle.getRadius()):
            inRange.append(obstacle)
    return inRange

def _getClosestObstacle(agent,
                        obstaclesInRange):
    agentPosition = agent.getPosition()
    agentDirectionRadians = agent.getDirectionRadians()
    (obstacleDetectionLength, 
     obstacleDetectionWidth) = agent.getObstacleDetectionDimensions()

    closestObstacle = None
    distanceToClosestInterceptPoint = None
    obstacleLocalPosition = None
    for obstacle in obstaclesInRange:    
        (obstacleX,
         obstacleY) = convert.pointToLocalSpace(obstacle.getPosition(), 
                                                agentPosition, 
                                                agentDirectionRadians)
        
        if obstacleX >= 0:
            expandedRadius = obstacle.getRadius() + (obstacleDetectionWidth / 2)
            if abs(obstacleY) < expandedRadius:
                #obstacleX +/- sqrt(expandedRadius^2 - obstacleY^2)
                
                if expandedRadius ** 2 < obstacleY ** 2:
                    sqrtPart = 0
                else:
                    sqrtPart = math.sqrt((expandedRadius**2) - (obstacleY**2))
                
                interceptPoint = obstacleX - sqrtPart
                
                if interceptPoint <= 0:
                    interceptPoint = obstacleX + sqrtPart
                
                if closestObstacle is None or interceptPoint < distanceToClosestInterceptPoint:
                    closestObstacle = obstacle
                    distanceToClosestInterceptPoint = interceptPoint
                    obstacleLocalPosition = (obstacleX,
                                             obstacleY)
    return (closestObstacle,
            obstacleLocalPosition)

    
