"""
Based on Template.py from C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import sys
from WestWorld import WestWorld

from Point import Point

from GraphicLocations import Lake, Mine, Saloon, MinerHome, Bank, Room
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher



class GLWest(GLCanvas):
    
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
    
    time_elapsed = time / 1000.00
    
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        
        self.timer = wx.Timer(self)
        self.parent = parent
        self.timer.Start(self.time)
        self.environment = WestWorld(self)

        self.locationsToDraw = ['miner_home', 'lake', 'mine', 'saloon', 'bank', 'bathroom', 'fisher_bedroom', 'miner_bedroom', 'kitchen']
        self.agentsToDraw = ['miner_bob', 'fisher_dan', 'miner_wife']


        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can 
        draw in it.  Most of its task is going to be sizing the Viewport to
        maintain aspect ratio and sizing the World Window to achieve the 
        maximum possible zoom."""
        
        
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
        
        glViewport(self.viewport_left, self.viewport_bottom, self.viewport_width, self.viewport_height)
         
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.worldmaxleft, self.worldmaxright, self.worldmaxbottom, self.worldmaxtop)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        Again, we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        glEnable(GL_TEXTURE_2D)
        self.SetupView()
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint 
        its surface. This just makes sure that OpenGL is inited and passes the work off 
        to another function.
        """
        dc = wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = 1
        self.OnDraw()
        return

    def OnSize(self,event):
        """ This function is called when a resize event occurs. The primary
        purpose for this is to readjust the viewport appropriately.
        """
        self.SetupView()
        if self.init:
            self.OnDraw()
        event.Skip()

    def DisplayMessage(self, message):
        current_message = self.parent.label_1.GetLabel().split('\n')
        for i in range(len(current_message) - 1):
            current_message[i] = current_message[i + 1]
            
        
        if len(current_message) <= 30:
            current_message.append('%s\n' % message)
        else:
            current_message[len(current_message) - 1] = message
            current_message = current_message[:30]
        
        current_message = '\n'.join(current_message)
        self.parent.label_1.SetLabel(current_message)
        

    def OnDraw(self):
        """This is the main drawing function. We will put all of our OpenGL 
        drawing calls in here. If we want to force a repaint, this is the 
        function that should be called. Note that this should always start 
        by calling SetCurrent() and end by calling SwapBuffers().
        """
        self.SetCurrent()
        glClear(GL_COLOR_BUFFER_BIT)
               
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()
        
        for key in self.locationsToDraw:
            location = location_manager[key]
            if hasattr(location, 'Draw'):
                location.Draw()
                
        for key in self.agentsToDraw:
            agent = agent_manager[key]
            if hasattr(agent, 'Draw'):
                agent.Draw()
            

        for row in location_manager['screenCells']:
            for cell in row:
                if hasattr(cell, 'Draw'):
                    cell.Draw()
                 

        self.SwapBuffers()

        return

    def HandleTime(self, event):
        
        self.environment.world.UpdateTimeStep()
        
        self.environment.RunSimulationIteration()
                
        self.OnDraw()
        event.Skip()