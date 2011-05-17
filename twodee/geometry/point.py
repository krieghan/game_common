class Point:
    """Class definition for our points.  A point has is pure-position, and thus is not capable of very much.
       A point's main contribution is for making lines.  Points have the ability to set and report their
       position."""
    	
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return
        
    def __str__(self):
        return 'Point Instance: [%s, %s]' % (self.getX(), self.getY())
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getXAndY(self):
        return [self.x, self.y]
    
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y, y
    
    def setXAndY(self, x, y):
        self.x = x
        self.y = y
