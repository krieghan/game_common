import wx
import optparse

import glsteering


class AIFrame(wx.Frame):
    def __init__(self,
                 wallfilename=None, 
                 *args,
                 **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.window_1 = glsteering.GLSteering(self,
                                              wallfilename)
        self.radio_btn_2 = wx.RadioButton(self, -1, "Attack")
        self.radio_btn_3 = wx.RadioButton(self, -1, "Defend")
        self.radio_btn_1 = wx.RadioButton(self, -1, "Target")
        self.radio_btn_4 = wx.RadioButton(self, -1, "Obstacle")
        self.button_1 = wx.Button(self, -1, "Start")
        self.button_2 = wx.Button(self, -1, "Stop")
        self.button_3 = wx.Button(self, -1, "Clear")

        self._setProperties()
        self._doLayout()

        self.Bind(wx.EVT_RADIOBUTTON, self.handleAttack, self.radio_btn_2)
        self.Bind(wx.EVT_RADIOBUTTON, self.handleDefend, self.radio_btn_3)
        self.Bind(wx.EVT_RADIOBUTTON, self.handleTarget, self.radio_btn_1)
        self.Bind(wx.EVT_RADIOBUTTON, self.handleObstacle, self.radio_btn_4)
        self.Bind(wx.EVT_BUTTON, self.handleStart, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.handleStop, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.handleClear, self.button_3)

    def _setProperties(self):
        self.SetTitle("AI Test Arena")
        self.SetSize((487, 455))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.window_1.SetBackgroundColour(wx.Colour(236, 233, 216))
        self.radio_btn_2.SetValue(1)

    def _doLayout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.window_1, 1, wx.EXPAND, 0)
        sizer_3.Add(self.radio_btn_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.radio_btn_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.radio_btn_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.radio_btn_4, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_2, 0, wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_3, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()

    def handleAttack(self, event): 
        self.window_1.agentMode(1)
        event.Skip()

    def handleDefend(self, event): 
        self.window_1.agentMode(0)
        event.Skip()

    def handleTarget(self, event):
        self.window_1.agentMode(2)
        event.Skip()

    def handleObstacle(self, event):
        self.window_1.agentMode(3)
        event.Skip()
        
    def handleStart(self, event):
        self.window_1.start()
        event.Skip()

    def handleStop(self, event):
        self.window_1.stop()
        event.Skip()

    def handleClear(self, event):
        self.window_1.clear()
        event.Skip()

def run(useProfile=False):
    
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_2 = AIFrame('walls2.in',
                      None, 
                      -1, 
                      "")
    app.SetTopWindow(frame_2)
    frame_2.Show()
    if useProfile:
        try:
            profile = hotshot.Profile('performance.prof')
            profile.runcall(app.mainLoop)
        finally:
            profile.close()
    else:
        app.MainLoop()


if __name__ == "__main__":
    run(useProfile=False)
    