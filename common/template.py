"""
Template

This module contains a basic template for a class that extends the GLCanvas and includes the basic routines 
for setting up simple 2D drawing.

C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *




class GLSystem(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. 
        We'll explain this in more detail later.
        """
        self.SetCurrent()
        size = self.GetSizeTuple()
        glViewport(0,0,size[0], size[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if size[0] > 0 and size[1] > 0:
            glOrtho(0,size[0], 0, size[1], 1, 10)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        Again, we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
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


    def OnDraw(self):
        """This is the main drawing function. We will put all of our OpenGL 
        drawing calls in here. If we want to force a repaint, this is the 
        function that should be called. Note that this should always start 
        by calling SetCurrent() and end by calling SwapBuffers().
        """
        self.SetCurrent()

        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)
        glutWireSphere(60, 6, 6)


        self.SwapBuffers()

        return