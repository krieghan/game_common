from geometry import *
from Line import Line


class Polygon:
	    
    def __init__(self, linelist = [], colorlist = [1, 1, 1]):
        self.color = colorlist
        self.lines = []
       
        
        for i in linelist:
            self.lines.append(CollisionLine(i[0], i[1], self))
    
    def __str__(self):
        return 'Polygon Instance: [%s]' % (self.lines)
    
    def GetColor(self):
        return self.color
    
    def SetColor(self, colorlist):
        self.color = colorlist   
    
    def GetLines(self):
        return self.lines

    def SetLines(self, linelist = []):
        self.lines = linelist
    
    def FindBoundaries(self):
        left = right = self.lines[0].GetPosition(0, 0)
        top = bottom = self.lines[0].GetPosition(0, 1)
        
                
        for i in self.lines:
            if i.GetPosition(0, 0) < left:
                left = i.GetPosition(0, 0)
            if i.GetPosition(0, 0) > right:
                right = i.GetPosition(0, 0)
            if i.GetPosition(0, 1) < bottom:
                bottom = i.GetPosition(0, 1)
            if i.GetPosition(0, 1) > top:
                top = i.GetPosition(0, 1)
        
        return [left, right, top, bottom]