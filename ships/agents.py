import math
from wx.glcanvas import GLCanvas
from OpenGL import GL, GLU

from twodee.geometry import (vector,
                         calculate)

from ai import colors

class Ship(object):
    
    implements(interfaces.Steerable)
    
    def __init__(self, 
                 canvas,
                 position, 
                 velocity,
                 color,
                 steeringController=None,
                 length=60,
                 width=30,
                 mass=1):
        self.canvas = canvas
        self.maxforce = 2000
        self.maxspeed = 5
        self.mass = mass
        self.steeringController = steeringController
        self.color = color
        self.position = position
        self.velocity = velocity
        self.length = length
        self.width = width
        self.minDetectionLength = 120
        velocityMagnitude = vector.getMagnitude(velocity)
        self.obstacleDetectionDimensions =\
            [self.minDetectionLength + (velocityMagnitude / self.maxspeed) * self.minDetectionLength,
             width]
        
    def draw(self):
        
        GL.glPushMatrix()
        x, y = self.position
        direction = self.getDirectionDegrees()
        GL.glTranslate(x, y, 0)
        GL.glRotatef(direction, 0, 0, 1)
        GL.glColor3f(*self.color)
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex2f(-self.length / 2, self.width / 2)
        GL.glVertex2f(self.length / 2, 0)
        GL.glVertex2f(-self.length / 2, -self.width / 2)
        GL.glEnd()
        #self.drawCoordinateAxes()
        #self.drawDetectionBox()
        
        GL.glPopMatrix()
        
    def drawDetectionBox(self):
        detectionLength, detectionWidth = self.obstacleDetectionDimensions
        GL.glColor3f(1, 1, 1)
        GL.glBegin(GL.GL_LINE_LOOP)
        GL.glVertex2f(0, detectionWidth / 2)
        GL.glVertex2f(detectionLength, detectionWidth / 2)
        GL.glVertex2f(detectionLength, -detectionWidth / 2)
        GL.glVertex2f(0, -detectionWidth / 2)
        GL.glEnd()
        
    def drawCoordinateAxes(self):
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(1, 0, 0)
        GL.glVertex(0, 0)
        GL.glVertex(100, 0)
        GL.glColor3f(0, 1, 0)
        GL.glVertex(0, 0)
        GL.glVertex(-100, 0)
        GL.glColor3f(0, 0, 1)
        GL.glVertex(0, 0)
        GL.glVertex(0, 100)
        GL.glColor3f(0, 1, 1)
        GL.glVertex(0, 0)
        GL.glVertex(0, -100)
        GL.glEnd()
        
        
    def drawCenterPoint(self):
        GL.glBegin(GL.GL_POINTS)
        GL.glVertex2f(0, 0)
        GL.glEnd()
        
    def getMaxForce(self):
        return self.maxforce
    
    def getSteeringController(self):
        return self.steeringController
    
    def getMaxSpeed(self):
        return self.maxspeed
    
    def getVelocity(self):
        return self.velocity
    
    def getHeading(self):
        return vector.normalize(self.velocity)
    
    def getSpeed(self):
        return vector.getMagnitude(self.velocity)
    
    def getLength(self):
        return self.length
    
    def getTarget(self):
        return self.steeringController.getTarget()
        
    
    def setSteeringController(self,
                              steeringController):
        self.steeringController = steeringController
        
    def setActionSelector(self,
                          actionSelector):
        self.actionSelector = actionSelector
    
    def getDirection(self):
        return vector.getDirectionRadians(self.velocity)
    
    def getDirectionDegrees(self):
        return vector.getDirectionDegrees(self.velocity)
    
    def getDirectionRadians(self):
        return vector.getDirectionRadians(self.velocity)
    
    def getPosition(self):
        return self.position
        
    def update(self,
               timeStep,
               timeElapsed):
        canvas = self.canvas
        maxspeed = self.maxspeed
        maxforce = self.maxforce
        minDetectionLength = self.minDetectionLength
        self.actionSelector.update(timeStep)
        
        force = self.steeringController.calculate()
        force = vector.truncate(vectorTuple=force,
                                cap=maxforce)
        
        acceleration = calculate.multiplyVectorAndScalar(vector=force,
                                                         scalar=timeElapsed / self.mass)
        
        velocity = calculate.addVectors(self.velocity,
                                        acceleration)

        velocity = vector.truncate(velocity,
                                   maxspeed)
        self.velocity = velocity                

        speed = vector.getMagnitude(velocity)
        
        #if speed > .0000001:
        #    self.heading = vector.normalize(velocity)
        #    self.side = vector.getPerpVector(self.heading)
       
        (x, y) = calculate.addPointAndVector(self.position,
                                             velocity)
        self.position = (x % canvas.getWorldWidth(),
                         y % canvas.getWorldHeight())
        
        
        
        self.obstacleDetectionDimensions[0] =\
            minDetectionLength + (speed / maxspeed) * minDetectionLength 

    def getObstacleDetectionDimensions(self):
        return self.obstacleDetectionDimensions

class Target(object):
    
    def __init__(self, 
                 canvas,
                 position,
                 height=30,
                 width=90,
                 color=colors.BLUE):
        self.target_width = width
        self.target_height = height
        self.color = color
        self.canvas = canvas
        self.position = position

    def update(self,
               timeStep,
               timeElapsed):
        pass

    def getPosition(self):
        return self.position

    def draw(self):
        GL.glPushMatrix()
        x, y = self.position
        GL.glTranslate(x, y, 0)
        GL.glColor3f(*self.color)
        
        GL.glBegin(GL.GL_LINE_LOOP)
            
        wdiv2 = self.target_width / 2
        hdiv2 = self.target_height / 2
            
        GL.glVertex2f(-wdiv2, hdiv2)
        GL.glVertex2f(wdiv2, hdiv2)
        GL.glVertex2f(wdiv2, -hdiv2)
        GL.glVertex2f(-wdiv2, -hdiv2)
           
        GL.glEnd()
            
        GL.glBegin(GL.GL_LINES)
            
        GL.glVertex2f(0, hdiv2)
        GL.glVertex2f(0, -hdiv2)
        GL.glVertex2f(wdiv2, 0)
        GL.glVertex2f(-wdiv2, 0)
            
        GL.glEnd()
        GL.glPopMatrix()
        
    def getVelocity(self):
        return (0, 0)
        
class Obstacle(object):
    def __init__(self, 
                 position, 
                 radius,
                 color=colors.WHITE,
                 numlines=10):
        self.radius = radius
        self.granularity = radius / 30.0
        self.color = color
        self.position = position
        self.numlines = numlines
        
    def update(self,
               timeStep,
               timeElapsed):
        pass
    
    def draw(self):
        
        GL.glPushMatrix()
        x, y = self.position
        GL.glTranslate(x, y, 0)
        GL.glColor3f(*self.color)
        
        GL.glColor3f(*self.color)
        GL.glBegin(GL.GL_LINE_LOOP)
        for i in range(self.numlines):
            GL.glVertex3f(self.radius * math.cos((i * 2 * math.pi) / self.numlines), 
                          self.radius * math.sin((i * 2 * math.pi) / self.numlines), 
                          0)
            
        GL.glEnd()
        GL.glPopMatrix()
        
    def getPosition(self):
        return self.position
    
    def getRadius(self):
        return self.radius
    
    def setColor(self,
                 newColor):
        self.color = newColor
        