import zope.interface

class Collideable(zope.interface.Interface):
    def getBoundaries():
        pass

    def handleCollision(otherElement):
        pass

    def getDirection():
        pass

    def getPosition():
        pass

class Renderable(zope.interface.Interface):
    def getActive():
        pass

    def getPosition():
        pass

    def getLength():
        pass
    
    def getWidth():
        pass

    def update(timeElapsed):
        pass

    def draw():
        pass

class Moveable(Renderable):
    def getVelocity():
        pass
    
    def getSpeed():
        pass
    
    def getHeading():
        pass

    def getDirectionDegrees():
        pass
    
    def getDirection():
        pass

class Steerable(Moveable):
    
    def getMaxSpeed():
        pass
    
    def getMaxForce():
        pass
    
    def getObstacleDetectionDimensions():
        pass
    
    def getSteeringController():
        pass
    
class Observable(zope.interface.Interface):
    def getObservers():
        pass

class IWorld(zope.interface.Interface):
    def start():
        pass

    def getAllCanvasElements():
        pass

    def render():
        pass

    def update(currentTime):
        pass

    def getHeightWidth():
        pass

    def getMaxLeftRightBottomTop():
        pass
