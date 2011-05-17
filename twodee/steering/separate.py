import random
from twodee.geometry import (calculate,
                         vector)

def separate(agent,
             neighbors):
    
    agentPosition = agent.getPosition()
    
    cumulativeForce = (0, 0)
    for neighbor in neighbors:
        if neighbor == agent:
            continue
        neighborPosition = neighbor.getPosition()
        neighborToAgent = calculate.subtractPoints(agentPosition,
                                                   neighborPosition)
        distanceToAgent = vector.getMagnitude(neighborToAgent)
        if distanceToAgent == 0:
            neighborHeadingToAgent = vector.normalize((random.random() - 1, 
                                                       random.random() - 1))
            magnitude = 100
        else:
            neighborHeadingToAgent = vector.normalize(neighborToAgent)
            magnitude = max(agent.length, agent.width) / distanceToAgent
            
        separationForceForThisNeighbor =\
            calculate.multiplyVectorAndScalar(neighborHeadingToAgent,
                                              magnitude)
        cumulativeForce = calculate.addVectors(cumulativeForce,
                                               separationForceForThisNeighbor)
        

    return cumulativeForce