from game_common.twodee.geometry import (
                         calculate,
                         vector)

def flee(agent,
         targetPosition,
         evadeDistanceSquared=None):
    steeringController = agent.getSteeringController()
    agentPosition = agent.getPosition()
    agentMaxSpeed = agent.getMaxSpeed()
    agentVelocity = agent.getVelocity()
    
    agentToTarget = calculate.subtractPoints(agentPosition,
                                             targetPosition)
    distanceSquaredToTarget = vector.getMagnitudeSquared(agentToTarget)

    if (evadeDistanceSquared is not None and 
        distanceSquaredToTarget > evadeDistanceSquared):
        return (0, 0)
    
    desiredVelocity = vector.setMagnitude(agentToTarget,
                                          agentMaxSpeed)
    
    return calculate.subtractVectors(desiredVelocity,
                                     agentVelocity)
    
    
