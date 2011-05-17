from Point import Point
from Location import ScreenCell
from Globals import globalRegistry

class ScreenCellBuilder:
    def __init__(self, height=None, width=None, hcells=None, wcells=None):
        self.height = height
        self.width = width
        self.hcells = hcells
        self.wcells = wcells
        
        self.cellheight = height / hcells
        self.cellwidth = width / wcells
        self.cells = []
    
    def buildScreenCells(self):
        for windex in range(self.wcells):
            self.cells.append([])
            for hindex in range(self.hcells):
                upperleft = [windex * self.cellwidth, hindex * self.cellheight]
                center = Point(upperleft[0] + self.cellwidth / 2, upperleft[1] + self.cellheight / 2)
                self.cells[-1].append(ScreenCell(name='ScreenCell %s %s' % (windex, hindex), world=globalRegistry['world'], point=center, height=self.cellheight, width=self.cellwidth))
        
        return self.cells