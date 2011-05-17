from OpenGL.GL import *
import math
from Location import Location

from Globals import globalRegistry, location_manager

def DrawCircle(radius, numlines=12):
    glBegin(GL_POLYGON)
    for i in xrange(numlines):
        
        glVertex3f(radius * math.cos((i * 2 * math.pi) / numlines), radius * math.sin((i * 2 * math.pi) / numlines), 0)
        
    glEnd()
    
def DrawHalfCircle(radius, numlines=12):
    glBegin(GL_POLYGON)
    
    for i in xrange(numlines / 2):
        
        glVertex3f(radius * math.cos((i * 2 * math.pi) / numlines), radius * math.sin((i * 2 * math.pi) / numlines), 0)
        
    glEnd()
    
def DrawRectangle():
    glBegin(GL_POLYGON)
    glVertex3f(-1, 1, 0)
    glVertex3f(1, 1, 0)
    glVertex3f(1, -1, 0)
    glVertex3f(-1, -1, 0)
    glEnd()

class GraphicLocation(Location):
    def __init__(self, point, name=None, world=None, size=50):
        Location.__init__(self, world)
        self.point = point
        self.size = size
        self.AddToScreenCell()
        
    def Draw(self):
        
        glPushMatrix()
        glTranslate(self.point.GetX(), self.point.GetY(), 0)
        self.DrawLocation()
        glPopMatrix()
        
    def AddToScreenCell(self):
        world = globalRegistry['world']
        (xposition, yposition) = self.point.GetXAndY()
        xlength = world.GetWLength()
        ylength = world.GetHLength()
        xindex = xposition / xlength
        yindex = yposition / ylength
        self.AddParentLocation(location_manager['screenCells'][xindex][yindex])
        
        
        
class Lake(GraphicLocation):
    def DrawLocation(self):
        glColor3f(0, 0, 1)
        DrawCircle(self.size)

        
class Mine(GraphicLocation):
    def DrawLocation(self):
        glColor3f(.23, .23, .21875)
        DrawHalfCircle(self.size * 2)

class Saloon(GraphicLocation):
    def DrawLocation(self):
        #glColor3f(.941, .941, .1758)
        glColor3f(1, 1, 0)
        glScalef(40, 20, 1)
        DrawRectangle()
        
    
class MinerHome(GraphicLocation):

    def DrawLocation(self):
        glColor3f(0, 1, 1)
        glPushMatrix()
        glScalef(100, 100, 1)
        DrawRectangle()
        glPopMatrix()
        
    
class Bank(GraphicLocation):
    def DrawLocation(self):
        glColor3f(0, 1, 0)
        glScalef(80, 40, 1)
        DrawRectangle()
    
class Room(GraphicLocation):
    def DrawLocation(self):
        glColor3f(1, 0, 0)
        glScalef(30, 30, 1)
        DrawRectangle()
  