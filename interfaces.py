from zope.interface import Interface, implements


class Renderable(Interface):
    def getPosition():
        pass
    
    def getLength():
        pass
    
    def getWidth():
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
    
    