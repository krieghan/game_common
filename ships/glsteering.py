import wx
import wx.glcanvas
import random
import math

from OpenGL import GL, GLU

from ai.ships import agents, actionselector
from ai.steering import steeringcontroller
from twodee.geometry import (calculate,
                         vector) 
from ai import (colors)


def drawCircle(radius, numlines):
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for i in xrange(numlines):
        
        glVertex3f(radius * math.cos((i * 2 * math.pi) / numlines), radius * math.sin((i * 2 * math.pi) / numlines), 0)
        
    glEnd()

class GLSteering(wx.glcanvas.GLCanvas):
   
    #We want to start with some dimensions and locations
    
    worldmaxleft = 0
    worldmaxright = 1250
    worldmaxtop = 1250
    worldmaxbottom = 0
    
    worldwidth = worldmaxright - worldmaxleft
    worldheight = worldmaxtop - worldmaxbottom
    
    
    viewport_left = 0
    viewport_bottom = 0
    viewport_height = 0
    viewport_width = 0
    
    agent_width = 60
    agent_height = 30
    
    time = 10.0
    
    mode = "attack"
    wall = []
    wall_list = None
    obstacle_list = None

    time_elapsed = time / 1000

    def __init__(self, 
                 parent,
                 wallfilename=None):
        wx.glcanvas.GLCanvas.__init__(self, parent,-1)
        self.init = 0        
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_LEFT_UP, self.handleClick)
        self.Bind(wx.EVT_TIMER, self.handleTime)
        
        self.timer = wx.Timer(self)
        
        self.attackers = []
        self.defenders = []
        self.targets = []
        self.obstacles = []        
        self.walls = []
        self.glWallList = None
        self.timeStep = 0
        self.wallfilename = wallfilename
        
    def getWorldWidth(self):
        return self.worldwidth
    
    def getWorldHeight(self):
        return self.worldheight
        
    def initWalls(self,
                  wallfilename):
        
        self.glWallList = GL.glGenLists(1)
        GL.glNewList(self.glWallList, GL.GL_COMPILE_AND_EXECUTE)
        
        f = open(wallfilename, 'r')
        lines = f.read().split('\n')
        
        for line in lines:
            [x1, y1, x2, y2] = line.split()
            [x1, y1, x2, y2] = [int(x1), int(y1), int(x2), int(y2)]
            self.walls.append(((x1, y1), (x2, y2)))
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(x1, y1)
            GL.glVertex2f(x2, y2)
            GL.glEnd()
    
        GL.glEndList()

        
    
    #hooks for pyOpenGL

    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        """
        GL.glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        GL.glEnable(GL.GL_TEXTURE_2D)
        self.setupView()
        return

        
    #methods on this function


    def setupView(self):
        """This function does the actual work to setup the window so we can 
        draw in it.  Most of its task is going to be sizing the Viewport to
        maintain aspect ratio and sizing the World Window to achieve the 
        maximum possible zoom.
        
        """
        
        self.clientsize = self.GetClientSizeTuple()
       
        height = self.worldheight 
        width = self.worldwidth  
        
        #The ratio of the width to the height in the client-area
        screenratio = float(self.clientsize[0]) / float(self.clientsize[1])
        
        ratio = width / height
        #Should seem familiar, since we did it in class...
        if ratio > screenratio:
        
            self.viewport_left = 0
            self.viewport_bottom = (self.clientsize[1] - (self.clientsize[0] / ratio)) / 2
            self.viewport_width = self.clientsize[0]
            self.viewport_height = self.clientsize[0] / ratio
            
            
        if ratio < screenratio:
        
            self.viewport_left = (self.clientsize[0] - self.clientsize[1] * ratio) / 2
            self.viewport_bottom = 0
            self.viewport_width = self.clientsize[1] * ratio
            self.viewport_height = self.clientsize[1]
        
        self.viewport_right = self.viewport_left + self.viewport_width
        self.viewport_top = self.viewport_bottom + self.viewport_height
        
        #glViewport(0, 0, self.clientsize[0], self.clientsize[1])
        
        GL.glViewport(self.viewport_left, self.viewport_bottom, self.viewport_width, self.viewport_height)
         
        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(self.worldmaxleft, self.worldmaxright, self.worldmaxbottom, self.worldmaxtop)
        




    def onPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint its surface. 
        This just makes sure that OpenGL is inited and passes the work off to another function.
        """
		
        dc = wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = 1
        self.onDraw()
        return
	
    def onSize(self,event):
        """ This function is called when a resize event occurs. The primary
        purpose for this is to readjust the viewport appropriately.
        """
		
        self.setupView()
        event.Skip()

        
    def onDraw(self):
        """This is the main drawing function. It does the work of plotting the in-progress polygon or 
        the accepted and rejected line segments.
        """
        
        self.SetCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)       
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        for canvasElement in self.getAllCanvasElements():
            canvasElement.draw()
        
        if self.glWallList is None:
            if self.wallfilename:
                self.initWalls(self.wallfilename)
    
        GL.glColor3f(1, 1, 1)
        GL.glCallList(self.glWallList)
        
        #GL.glColor3f(1, 1, 1)
        
#        if self.attackers:
#            if self.attackers[0].steer.path is not None:
#                GL.glBegin(GL.GL_LINE_STRIP)
#                for waypoint in self.attacker[0].steer.path.getPointList():
#            
#                    GL.glVertex2f(*waypoint.getXAndY())
#        
#                if self.attacker[0].steer.path.mode == "open":
#                    GL.glVertex2f(*self.attacker[0].steer.path.getPointAt(0).getXAndY())
#                GL.glEnd()
            
        
        self.SwapBuffers()
        self.setupView()
        return

    def agentMode(self, mode):
        if mode == 0:
            self.mode = "defend"
        elif mode == 1:
            self.mode = "attack"
        elif mode == 2:
            self.mode = "target"
        elif mode == 3:
            self.mode = "obstacle"
    
    def start(self):
        self.timer.Start(self.time)
        self.going = True
        
    def stop(self):
        self.timer.Stop()
        self.going = False
        
    def clear(self):
        self.stop()
        self.attackers = []
        self.defenders = []
        self.targets = []
        self.obstacles = []
        
        self.onDraw()
    
    def getAllCanvasElements(self):
        return self.attackers + self.defenders + self.targets + self.obstacles
    
    def getShips(self):
        return self.attackers + self.defenders
    
    def handleTime(self, event):
        
        self.timeStep += 1
        
        for canvasElement in self.getAllCanvasElements():
            canvasElement.update(timeStep=self.timeStep,
                                 timeElapsed=self.time_elapsed)
        
        
        self.onDraw()
        event.Skip()
    
    
    def handleClick(self, event):
        """Called when the user clicks in the canvas.  The main idea of this
        function is to record the points in points[].  A conversion must take
        place in GiveWorldXY for the points to be expressed in terms of the world.
        """
        
        vectorx = random.random() * 2
        vectory = random.random() * 2
        clickx = event.GetX()
        clicky = event.GetY()
        
        self.clientsize = self.GetClientSizeTuple()
        
        #If the click isn't in the viewport, I can't do anything with it
        
        if (clickx < self.viewport_left or
            clickx > self.viewport_right or
            self.clientsize[1] - clicky > self.viewport_top or
            self.clientsize[1] - clicky < self.viewport_bottom):
            event.Skip()
            return
        
        
                
        position = self.getWorldPositionFromClientPosition(clickx,
                                                           clicky)
        velocity = (vectorx,
                    vectory) 
        
        if self.mode == "attack":
            ship = agents.Ship(canvas=self,
                               position=position, 
                               velocity=velocity,
                               color=colors.RED)
            steeringController = getSteeringController(canvas=self,
                                                       agent=ship)
            ship.setSteeringController(steeringController)
            actionSelector = actionselector.AttackerSelector(agent=ship)
            ship.setActionSelector(actionSelector)
            self.attackers.append(ship)
        elif self.mode == "defend":
            ship = agents.Ship(canvas=self,
                               position=position, 
                               velocity=velocity,
                               color=colors.GREEN)
            steeringController = getSteeringController(canvas=self,
                                                       agent=ship)
            ship.setSteeringController(steeringController)
            actionSelector = actionselector.DefenderSelector(agent=ship)
            ship.setActionSelector(actionSelector)
            self.defenders.append(ship)
        elif self.mode == "target":
            target = agents.Target(self,
                                   position)
            self.targets.append(target)
        elif self.mode == "obstacle":
            obstacle = agents.Obstacle(position=position, 
                                       radius=50)
            self.obstacles.append(obstacle)
                    
        self.onDraw()
        event.Skip()
        return
    
    
    def getWorldPositionFromClientPosition(self, x, y):
        """Our conversion function.  Here, we must convert from canvas coordinates (which is how the
        click is expressed) to viewport coordinates and then to world coordinates."""

        self.clientsize = self.GetClientSizeTuple()
        
        yscale = float(self.worldmaxtop - self.worldmaxbottom) / float(self.viewport_height)
        
        xscale = float(self.worldmaxright - self.worldmaxleft) / float(self.viewport_width)

        
        
        return [(x - self.viewport_left) * xscale, (self.clientsize[1] - y - self.viewport_bottom) * yscale]


    def getElementsWithinDistanceSquared(self,
                                         agent,
                                         distanceThresholdSquared,
                                         elementTypes=None):
        
        if elementTypes is None:
            elementsToConsider = self.getAllCanvasElements()
        else:
            elementsToConsider = []
            if 'attacker' in elementTypes:
                elementsToConsider.extend(self.attackers)
            if 'defender' in elementTypes:
                elementsToConsider.extend(self.defenders)
            if 'obstacle' in elementTypes:
                elementsToConsider.extend(self.obstacles)
            if 'target' in elementTypes:
                elementsToConsider.extend(self.targets)
                
        elementsWithinDistance = []
        agentPosition = agent.getPosition()
        for element in elementsToConsider:
            if element == agent:
                continue
            elementPosition = element.getPosition()
            agentToElement = calculate.subtractPoints(elementPosition,
                                                      agentPosition)
            distanceSquaredToElement =\
                vector.getMagnitudeSquared(agentToElement)
            if distanceSquaredToElement <= distanceThresholdSquared:
                elementsWithinDistance.append(element)
            
        return elementsWithinDistance


    def getClosestCanvasElement(self,
                                agent,
                                elementTypes=None):
        if elementTypes is None:
            elements = self.getAllCanvasElements()
        else:
            elements = []
            
            if 'defender' in elementTypes:
                elements += self.defenders
            if 'attacker' in elementTypes:
                elements += self.attackers
            if 'obstacle' in elementTypes:
                elements += self.obstacles
            if 'target' in elementTypes:
                elements += self.targets
            
        closestElement = None
        closestDistanceSquared = None
        agentPosition = agent.getPosition()
        
        for element in elements:
            elementPosition = element.getPosition()
            agentToElement = calculate.subtractPoints(elementPosition,
                                                      agentPosition)
            distanceSquared = vector.getMagnitudeSquared(agentToElement)
            if closestElement is None or distanceSquared < closestDistanceSquared:
                closestElement = element
                closestDistanceSquared = distanceSquared 
            
        return closestElement
        
        

def getSteeringController(canvas,
                          agent):
    steeringController = steeringcontroller.SteeringController(agent=agent)
    return steeringController

