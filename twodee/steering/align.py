from twodee.geometry import (calculate,
                             vector)

def align(agent,
          neighbors):
    #Save us from divide-by-zero
    if not neighbors:
        return (0, 0)
    
    cumulativeHeading = (0, 0)
    for neighbor in neighbors:
        neighborVelocity = neighbor.getVelocity()
        neighborHeading = vector.normalize(neighborVelocity)
        cumulativeHeading = calculate.addVectors(cumulativeHeading,
                                                 neighborHeading)
    averageHeading = calculate.multiplyVectorAndScalar(cumulativeHeading,
                                                       float(1) / len(neighbors))
    return averageHeading
    