from game_common.twodee.steering import arrive
from game_common.twodee.geometry import (
                         calculate,
                         vector)

def interpose(agent,
              enemy,
              charge):
    agentPosition = agent.getPosition()
    agentMaxSpeed = agent.getMaxSpeed()
    enemyPosition = enemy.getPosition()
    enemyVelocity = enemy.getVelocity()
    chargePosition = charge.getPosition()
    chargeVelocity = charge.getVelocity()
    enemyToCharge = calculate.subtractPoints(chargePosition,
                                             enemyPosition)
    midVector = calculate.multiplyVectorAndScalar(enemyToCharge,
                                                  .5)
    midPoint = calculate.addPointAndVector(enemyPosition,
                                           midVector)
    
    agentToMidPoint = calculate.subtractPoints(midPoint,
                                               agentPosition)
    distanceToMidPoint = vector.getMagnitude(agentToMidPoint)
    timeToMidPoint = distanceToMidPoint / agentMaxSpeed
    
    enemyToFuturePosition = calculate.multiplyVectorAndScalar(enemyVelocity,
                                                              timeToMidPoint)
    enemyFuturePosition = calculate.addPointAndVector(enemyPosition,
                                                      enemyToFuturePosition)
    
    chargeToFuturePosition = calculate.multiplyVectorAndScalar(chargeVelocity,
                                                               timeToMidPoint)
    chargeFuturePosition = calculate.addPointAndVector(chargePosition,
                                                       chargeToFuturePosition)
        
    
    
    enemyFutureToChargeFuture = calculate.subtractPoints(chargeFuturePosition,
                                                         enemyFuturePosition)
    futureMidVector = calculate.multiplyVectorAndScalar(enemyFutureToChargeFuture,
                                                        .5)
    futureMidPoint = calculate.addPointAndVector(enemyFuturePosition,
                                                 futureMidVector)
    
    return arrive.arrive(agent,
                         futureMidPoint)
