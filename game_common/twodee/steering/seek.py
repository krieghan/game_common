from game_common.twodee.geometry import (
                         calculate,
                         vector)

def seek(agent,
         targetPosition):
    maxSpeed = agent.getMaxSpeed()
    agentPosition = agent.getPosition()
    agentVelocity = agent.getVelocity()
    agentToTarget = calculate.subtractPoints(targetPosition,
                                             agentPosition)
    
    desiredVelocity = vector.setMagnitude(agentToTarget,
                                          maxSpeed)
    
    return calculate.subtractVectors(desiredVelocity,
                                     agentVelocity)
      
    
