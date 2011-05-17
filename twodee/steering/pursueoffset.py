from twodee.geometry import (calculate,
                         convert,
                         vector)
import arrive

def pursueoffset(agent, 
                 targetAgent, 
                 targetToOffset):
    agentPosition = agent.getPosition()
    agentMaxSpeed = agent.getMaxSpeed()
    targetPosition = targetAgent.getPosition()
    targetDirection = targetAgent.getDirection()
    targetSpeed = targetAgent.getSpeed()
    targetVelocity = targetAgent.getVelocity()
    worldTargetToOffset = convert.vectorToWorldSpace(targetToOffset,
                                                     targetPosition,
                                                     targetDirection)
    offsetPosition = calculate.addPointAndVector(targetPosition,
                                                 worldTargetToOffset)
    
    agentToOffset = calculate.subtractPoints(offsetPosition,
                                             agentPosition)
    distanceToOffset = vector.getMagnitude(agentToOffset)
    
    if targetSpeed == 0:
        lookAheadTime = 0
    else:
        lookAheadTime = distanceToOffset / (agentMaxSpeed + targetSpeed)
    
    targetToPredictedPosition = calculate.multiplyVectorAndScalar(targetVelocity,
                                                                  lookAheadTime)
    predictedOffsetPosition = calculate.addPointAndVector(offsetPosition,
                                                          targetToPredictedPosition)
    
    return arrive.arrive(agent,
                         predictedOffsetPosition,
                         .9)
    