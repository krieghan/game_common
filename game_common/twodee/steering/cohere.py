from game_common.twodee.geometry import (calculate)
import seek

def cohere(agent, 
           neighbors):
    if not neighbors:        
        return (0, 0)
    
    agentPosition = agent.getPosition()
    cumulativeVector = (0, 0)
    
    neighborCount = 0
    for neighbor in neighbors:
        if neighbor == agent:
            continue
        neighborCount += 1
        originToNeighbor = neighbor.getPosition()
        cumulativeVector = calculate.addVectors(cumulativeVector,
                                                originToNeighbor)
    
    if not neighborCount:
        return (0, 0)
    originToCenterPoint = calculate.multiplyVectorAndScalar(
                                        cumulativeVector,
                                        float(1) / neighborCount)
    centerPoint = originToCenterPoint
    return seek.seek(agent,
                     centerPoint)
