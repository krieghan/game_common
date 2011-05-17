from BaseGameEntity import BaseGameEntity
from EntityManager import EntityManager, LocationManager, AgentManager, ItemManager
from Point import Point
from BaseGameEntity import Agent, Item
from Exceptions import LocationException

from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Location(BaseGameEntity):
    def __init__(self, name=None, world=None, point=None, **parentLocations):
        BaseGameEntity.__init__(self, name, world=world)
        
        self.childLocations = LocationManager()
        self.parentLocations = LocationManager()
        
        self.point = point
        
        self.items = ItemManager()
        self.agents = AgentManager()
    
    def __getitem__(self, name):
        
        hasAgent = self.agents.HasKey(name)
        hasItem = self.items.HasKey(name)
        
        if hasAgent and hasItem:
            raise CrossEntityException()

        if hasAgent:
            return self.agents[name]
        if hasItem:
            return self.items[name]
        
    def __setitem__(self, name, element):
        
        if issubclass(element.__class__, Item):
            
            if not self.items.HasKey(name):
                del element.location[name]
                self.items[name] = element
                element.location = self
            else:
                raise LocationException('Location %s already has item with name %s' % (self.name, name))
            
        elif issubclass(element.__class__, Agent):
            if not self.agents.HasKey(name):
                del element.location[name]
                self.agents[name] = element
                element.location = self
            else:
                raise LocationException('Location %s already has agent with name %s' % (self.name, name))
        

    def __delitem__(self, name):
        if self.items.HasKey(name):
            del self.items[name]
        if self.agents.HasKey(name):
            del self.agents[name]
   
    def AddParentLocation(self, location):
        location.childLocations.Add(self.key, entity=self)
        self.parentLocations.Add(location.key, entity=location)
        
    def AddChildLocation(self, location):
        self.childLocations.Add(location.key, entity=location)
        location.parentLocations.Add(self.key, entity=self)

    def HandleMessage(self, message):
        message_dispatcher.ScheduleMessage(Message(message.source, self.GetContents(), message.message, 0, None, world=self.world))

    def GetItems(self):
        return self.items
    
    def GetAgents(self):
        return self.agents
       
    def GetContents(self):
        return self.items + self.agents
    
class ScreenCell(Location):
    def __init__(self, name=None, world=None, point=None, height=None, width=None, **parentLocations):
        Location.__init__(self, name=name, world=world, point=point, **parentLocations)
        (x, y) = self.point.GetXAndY()
        xdistance = width / 2.0
        ydistance = height / 2.0
        self.upperleft = Point(x - xdistance, y - ydistance)
        self.upperright = Point(x + xdistance, y - ydistance)
        self.lowerleft = Point(x - xdistance, y + ydistance)
        self.lowerright = Point(x + xdistance, y + ydistance)
        
    def Draw(self):
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 1, 1)
        glVertex3f(self.lowerleft.GetX(), self.lowerleft.GetY(), 0)
        glVertex3f(self.upperleft.GetX(), self.upperleft.GetY(), 0)
        glVertex3f(self.upperright.GetX(), self.upperright.GetY(), 0)
        glVertex3f(self.lowerright.GetX(), self.lowerright.GetY(), 0)
        glEnd()
        