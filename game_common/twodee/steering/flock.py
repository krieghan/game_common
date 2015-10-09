from game_common.twodee.geometry import calculate

from game_common.twodee.steering import (
        separate, 
        align, 
        cohere)

def flock(agent, 
          neighbors, 
          separationMagnitude=50, 
          alignmentMagnitude=2, 
          cohesionMagnitude=1):
    
    separationForce = separate.separate(agent,
                                        neighbors)
    alignmentForce = align.align(agent,
                                 neighbors)
    cohesionForce = cohere.cohere(agent,
                                  neighbors)
    
    weightedSeparationForce = calculate.multiplyVectorAndScalar(separationForce,
                                                                separationMagnitude)
    weightedAlignmentForce = calculate.multiplyVectorAndScalar(alignmentForce,
                                                               alignmentMagnitude)
    weightedCohesionForce = calculate.multiplyVectorAndScalar(cohesionForce,
                                                              cohesionMagnitude)
    
    totalForce = calculate.addVectors(weightedSeparationForce,
                                      weightedAlignmentForce,
                                      weightedCohesionForce)
    
    return totalForce
