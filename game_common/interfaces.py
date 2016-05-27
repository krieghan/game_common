import zope.interface

class Collideable(zope.interface.Interface):
    def getBoundaries():
        pass

    def handleCollision(otherElement):
        pass

    def getDirection():
        pass

class Renderable(Collideable):
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
    height = zope.interface.Attribute("height")
    width = zope.interface.Attribute("width")
    max_left = zope.interface.Attribute("max_left")
    max_right = zope.interface.Attribute("max_right")
    max_top = zope.interface.Attribute("max_top")
    max_bottom = zope.interface.Attribute("max_bottom")

    def start():
        pass

    def getAllCanvasElements():
        pass

    def render():
        pass

    def update(currentTime):
        pass

