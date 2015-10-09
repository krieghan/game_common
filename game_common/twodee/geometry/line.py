from game_common.twodee.geometry import (
             geometry,
             calculate,
             point,
             vector)



#Line is deprecated.  Will phase out soon.

class Line:
    """Since this project is based on shapes, lines are very important.  A line has the ability to return
       its true distance, or the distance in either the X or Y direction.  It can also give its angle in 
       relation to the X-Axis, and to return its Normal Perp Vector.  A line also has the ability to
       set its position"""
    
    
    
    def __init__(self, point1, point2):
        "Line Instantiated"
        (x1, y1) = point1
        (x2, y2) = point2
        self.vector1 = Vector(0, 0)
        self.point = [None, None]
        self.point[0] = Point(x1, y1)
        self.point[1] = Point(x2, y2)
        self.vector = geometry.subPoints(self.point[1], self.point[0], resultant_vector=self.vector1)
        
    def __str__(self):
        return 'Line Instance: [%s, %s]' % (self.point[0], self.point[1])
        
    def getPoint(self, pointindex = -1):
        if pointindex == -1:
            return [self.point[0], self.point[1]]
        else:
            return self.point[pointindex]
    
    def setPoint(self, point, pointindex = -1):
        (x, y) = point
        self.point[pointindex].setXAndY(x, y)
        self.vector.setXAndY(*geometry.subPoints(self.point[1], self.point[0], resultant_vector=self.vector1).getXAndY())

    def setLine(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2
        self.point[0].setXAndY(x1, y1)
        self.point[1].setXAndY(x2, y2)
        self.vector.setXAndY(*geometry.subPoints(self.point[1], self.point[0], resultant_vector=self.vector1).getXAndY())
        
    def getDeltaX(self):
        point[1].getX() - point[0].getX()
	
    def getDeltaY(self):
        point[1].getY() - point[0].getY()
	
    def getDistance(self):
        return math.sqrt(math.pow(self.getDeltaX(), 2) + math.pow(self.getDeltaY(), 2))
	
    def getTheta(self):
        return math.degrees(math.atan2(self.getDeltaY(), self.getDeltaX()))
    
    def getVector(self):
        return self.vector
    
    def findNormalPerpVector(self, resultant_vector=None):
        """Having a line return its normal perp vector is vital if we are to do the calculations 
        necessary for this project"""
        if resultant_vector == None:
            new_vector = self.vector.getPerpVector(self, resultant_vector)
            new_vector.normalize()
            return new_vector
        else:
            resultant_vector = self.vector.getPerpVector(self, resultant_vector=self.vector1)
            resultant_vector.normalize()
            return resultant_vector
