from game_common.twodee.geometry import (
                         point,
                         vector)

class Ray:
    """A ray has position (point) and direction and magnitude (vector).  The vector is based on the difference
       between the two points that are given in __init()"""
	
    def __init__(self, point, vector):
        self.point = point
        self.vector = vector
        
    def __str__(self):
        return 'Ray Instance: [%s, %s]' % (self.point, self.vector)
    
    def GetPoint(self):
        return self.point
    
    def GetVector(self):
        return self.vector
        
    def SetPoint(self, point):
        self.point = point
    
    def SetVector(self, vector):
        self.vector = vector
