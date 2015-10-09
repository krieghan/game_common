from game_common.twodee.steering import seek
from game_common.twodee.geometry import (
                         calculate,
                         vector)

def pursue(agent,
           target):
    agentHeading = agent.getHeading()
    targetHeading = target.getHeading()
    targetPosition = target.getPosition()
    relativeHeading = calculate.dotProduct(agentHeading,
                                           targetHeading)
    
    #If the target is heading at me, then just Seek
    if relativeHeading < -.95:
        return seek.seek(agent,
                         targetPosition)

    agentPosition = agent.getPosition()
    agentMaxSpeed = agent.getMaxSpeed()

    
    targetSpeed = target.getSpeed()
    targetVelocity = target.getVelocity()
    agentToTarget = calculate.subtractPoints(targetPosition,
                                             agentPosition)
    distanceToTarget = vector.getMagnitude(agentToTarget)
    
    lookAheadTime = distanceToTarget / (agentMaxSpeed + targetSpeed)
    
    lookAheadVector = calculate.multiplyVectorAndScalar(targetVelocity,
                                                        lookAheadTime)
    
    lookAheadPosition = calculate.addPointAndVector(targetPosition,
                                                    lookAheadVector)
    
    return seek.seek(agent,
                     lookAheadPosition)
    
    
