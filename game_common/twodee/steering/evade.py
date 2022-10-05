from . import flee

from game_common.twodee.geometry import (
                         calculate,
                         vector)

def evade(agent, 
          target,
          evadeDistanceSquared=None):
    agentPosition = agent.getPosition()
    agentMaxSpeed = agent.getMaxSpeed()
    targetPosition = target.getPosition()
    targetSpeed = target.getSpeed()
    targetVelocity = target.getVelocity()
    targetToAgent = calculate.subtractPoints(agentPosition,
                                             targetPosition)
    distanceToTarget = vector.getMagnitude(targetToAgent)
    lookAheadTime = distanceToTarget / (agentMaxSpeed + targetSpeed)
    lookAheadVector = calculate.multiplyVectorAndScalar(targetVelocity,
                                                        lookAheadTime)
    lookAheadPosition = calculate.addPointAndVector(targetPosition,
                                                    lookAheadVector)
    return flee.flee(agent,
                     lookAheadPosition,
                     evadeDistanceSquared)
    
