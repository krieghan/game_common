from twodee.geometry import (calculate,
                             vector,
                             convert)
import arrive


    
def followpath(agent,
               target=None):
    '''Return the force necessary to steer a given agent along
       a path defined in its steering controller.  If a target
       is specified, the path is computed relative to that 
       target.'''
    if target:
        return _followpath(agent,
                           getCurrentPointInWorldSpace,
                           targetPosition=target.getPosition(),
                           targetDirection=target.getDirection())
    else:
        return _followpath(agent,
                           getCurrentPointFromPath,
                           targetPosition=None,
                           targetDirection=None)
    


def _followpath(agent,
                getCurrentPoint,
                targetPosition,
                targetDirection):
    steeringController = agent.getSteeringController()
    path = steeringController.getPath()
    currentPoint = getCurrentPoint(path,
                                   targetPosition,
                                   targetDirection)
    agentPosition = agent.getPosition()
    agentToCurrentPoint = calculate.subtractPoints(currentPoint,
                                                   agentPosition)
    squaredDistanceToCurrentPoint = vector.getMagnitudeSquared(agentToCurrentPoint)
    if squaredDistanceToCurrentPoint < steeringController.waypointSquaredDistance:
        if path.complete():
            return arrive.arrive(agent,
                                 currentPoint)
        path.next()
        nextPoint = getCurrentPoint(path,
                                    targetPosition,
                                    targetDirection)
        return arrive.arrive(agent,
                             nextPoint)
    else:
        return arrive.arrive(agent,
                             currentPoint)

def getCurrentPointInWorldSpace(path,
                                targetPosition,
                                targetDirection):
    localPoint = path.current()
    worldPoint = convert.pointToWorldSpace(localPoint,
                                           targetPosition,
                                           targetDirection)
    return worldPoint

def getCurrentPointFromPath(path,
                            targetPosition=None,
                            targetDirection=None):
    return path.current()
    



class Path(object):
    def __init__(self, 
                 points,
                 closed=False):
        self.points = points
        self.closed = closed
        self.currentindex = 0
   
    def current(self):
        if self.currentindex is None:
            return None
        
        return self.points[self.currentindex]
    
    def next(self):
        currentindex = self.currentindex + 1
        pathlength = len(self.points)
        if self.closed:
            currentindex = currentindex % pathlength
        else:
            if currentindex >= pathlength:
                raise InvalidPathState()
                
                
        self.currentindex = currentindex
    
    def previous(self):
        currentindex = self.currentindex - 1
        pathlength = len(self.points)
        if self.closed:
            currentindex = currentindex % len(points)
        else:
            if currentindex < 0:
                raise InvalidPathState()
                
        self.currentindex = currentindex
    
    def complete(self):
        if not self.closed:
            return self.currentindex >= len(self.points) - 1
        
        return False
    
class InvalidPathState(Exception):
    pass
            
        