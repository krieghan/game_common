import math

from wx.glcanvas import GLCanvas
from OpenGL import GL, GLU

from twodee.geometry import (calculate,
                         vector)

vector1 = vector.Vector(0, 0)

class Stationary:
    def __init__(self, parent, Point):
        self.vector1 = globals()['vector1']
        self.point = Point
        self.world = parent
        self.color = []
        
    def getPoint(self):
        return self.point
    
    def getColor(self):
        return self.color

    def setColor(self, color):
        self.color = color

class Target(Stationary):
    
    def __init__(self, parent, point):
        self.target_width = 30
        self.target_height = 15
        Stationary.__init__(self, parent, point)
        self.color = [0, 0, 1]
    
    
    def update(self):
        for element in self.world.getObject('attacker'):        
            if geometry.subPoints(self.point, element.point, resultant_vector=self.vector1).getMagnitude() < 3:
                self.color = [0, 1, 0]                
                return
        
        for element in self.world.getObject('defender'):
            if geometry.subPoints(self.point, element.point, resultant_vector=self.vector1).getMagnitude() < 3:
                self.color = [0, 1, 0]
                return
        
        #self.color = [0, 0, 1]
    
    def draw(self):
        
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
        
class Obstacle(Stationary):
    def __init__(self, parent, point, radius):
        Stationary.__init__(self, parent, point)
        self.radius = radius
        self.granularity = radius / 30.0
        self.color = [1, 1, 1]
        
    def getRadius(self):
        return self.radius
    
    def setRadius(self, radius):
        self.radius = radius
    
    def setGranularity(self, gran):
        self.granularity = gran
    
    def setColor(self, color):
        self.color = color
    
    def draw(self, numlines=10):
        GL.glColor3f(1, 1, 1)
        GL.glBegin(GL.GL_LINE_LOOP)
        for i in range(numlines):
            GL.glVertex3f(self.radius * math.cos((i * 2 * math.pi) / numlines), 
                          self.radius * math.sin((i * 2 * math.pi) / numlines), 
                          0)
            
        GL.glEnd()