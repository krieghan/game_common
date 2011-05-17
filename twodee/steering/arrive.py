from twodee.geometry import (calculate,
                         vector)

def arrive(agent,
           targetPosition,
           decelerationFactor=None):
    steeringController = agent.getSteeringController()
    if decelerationFactor is None:
        decelerationFactor = steeringController.decelerationFactor
    agentPosition = agent.getPosition()
    agentToTarget = calculate.subtractPoints(targetPosition,
                                             agentPosition)
    distanceToTarget = vector.getMagnitude(agentToTarget)
        
    if round(distanceToTarget) > 0:
        agentMaxSpeed = agent.getMaxSpeed()
        agentVelocity = agent.getVelocity()
        speed = distanceToTarget / decelerationFactor
        speed = min(speed, agentMaxSpeed)
        desiredVelocity = calculate.multiplyVectorAndScalar(agentToTarget,
                                                            speed / distanceToTarget)
        return calculate.subtractVectors(desiredVelocity,
                                         agentVelocity)

    else:
        return (0, 0)