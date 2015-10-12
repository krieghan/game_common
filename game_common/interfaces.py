import zope.interface

class Renderable(zope.interface.Interface):
    active = zope.interface.Attribute("active")
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
    
class IWorld(zope.interface.Interface):
    height = zope.interface.Attribute("height")
    width = zope.interface.Attribute("width")
    max_left = zope.interface.Attribute("max_left")
    max_right = zope.interface.Attribute("max_right")
    max_top = zope.interface.Attribute("max_top")
    max_bottom = zope.interface.Attribute("max_bottom")

    def getAllCanvasElements():
        pass

    def render():
        pass

    def update(currentTime):
        pass
