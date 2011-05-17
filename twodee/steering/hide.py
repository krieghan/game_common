from twodee.geometry import (calculate,
                         vector)

import arrive, evade

def hide(agent,
         attacker, 
         obstacles):
    distanceFromObstacleBoundary = 30
    closestDistance = None
    closestHidingPlace = None
    attackerPosition = attacker.getPosition()
    agentPosition = agent.getPosition()
    for obstacle in obstacles:
        obstaclePosition = obstacle.getPosition()
        hidingPlaceDistanceToObstacle = distanceFromObstacleBoundary + obstacle.getRadius()
        attackerToObstacle = calculate.subtractPoints(obstaclePosition,
                                                      attackerPosition)
        attackerDistanceToObstacle = vector.getMagnitude(attackerToObstacle)
        attackerDistanceToHidingPlace =  hidingPlaceDistanceToObstacle + attackerDistanceToObstacle
        attackerToHidingPlace = vector.setMagnitude(attackerToObstacle,
                                                    attackerDistanceToHidingPlace)

        hidingPlace = calculate.addPointAndVector(attackerPosition,
                                                  attackerToHidingPlace)
        
        agentToHidingPlace = calculate.subtractPoints(hidingPlace,
                                                      agentPosition)
        distanceToHidingPlace = vector.getMagnitude(agentToHidingPlace)
        
        if closestDistance is None or distanceToHidingPlace < closestDistance:
            closestDistance = distanceToHidingPlace
            closestHidingPlace = hidingPlace
        
    if closestHidingPlace is None:
        return evade.evade(agent,
                           attacker)
        
    return arrive.arrive(agent,
                         closestHidingPlace)