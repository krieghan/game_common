import random
from game_common.twodee.geometry import (
                         calculate,
                         convert,
                         vector)

def wander(agent):
    steeringController = agent.getSteeringController()
    centerToTargetVector = steeringController.centerToWanderTarget
    wanderDistance = steeringController.wanderDistance
    wanderJitter = steeringController.wanderJitter
    wanderRadius = steeringController.wanderRadius
    agentPosition = agent.getPosition()
    projectionVector = (wanderDistance, 0)
    
    targetAdjustment =\
        ((random.random() * 2 - 1) * wanderJitter, 
         (random.random() * 2 - 1) * wanderJitter)
    
    centerToTargetVector = calculate.addVectors(centerToTargetVector,
                                                targetAdjustment)
    
    centerToTargetVector = vector.setMagnitude(centerToTargetVector,
                                               wanderRadius)
    
    localTargetVector = calculate.addVectors(centerToTargetVector,
                                             projectionVector)
    worldTargetVector = convert.vectorToWorldSpace(localTargetVector,
                                                   agentPosition,
                                                   agent.getDirectionRadians())
    
    return worldTargetVector
    
