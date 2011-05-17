import math

def getDirectionRadians(vectorTuple):
    return math.atan2(vectorTuple[1], vectorTuple[0])

def getDirectionDegrees(vectorTuple):
    return math.degrees(getDirectionRadians(vectorTuple))

def truncate(vectorTuple,
             cap):
    magnitude = getMagnitude(vectorTuple)
    if magnitude > cap:
        return setMagnitude(vectorTuple,
                            cap)
    else:
        return vectorTuple

def getMagnitude(vectorTuple):
    x, y = vectorTuple
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

def getMagnitudeSquared(vectorTuple):
    x, y = vectorTuple
    return math.pow(x, 2) + math.pow(y, 2)

def getManhattanMagnitude(vectorTuple):
    x, y = vectorTuple
    return x + y

def setMagnitude(vectorTuple,
                 newMagnitude):
    directionRadians = getDirectionRadians(vectorTuple)
    return (round(newMagnitude * math.cos(directionRadians), 5),
            round(newMagnitude * math.sin(directionRadians), 5))
    
def setDirection(vectorTuple,
                 newDirection):
    magnitude = getMagnitude(vectorTuple)
    return (round(magnitude * math.cos(newDirection), 5),
            round(magnitude * math.sin(newDirection), 5))

def normalize(vectorTuple):
    return setMagnitude(vectorTuple, 1)

def normalizeAndHandle(vectorTuple):
    try:
        normalizedVector = normalize(vectorTuple)
    except InvalidVector:
        normalizedVector = (1, 0)
    return normalizedVector

def createVector(magnitude,
                 direction):
    return (round(magnitude * math.cos(direction), 5),
            round(magnitude * math.sin(direction), 5))

#"Outside" and "Inside" assume a shape that is specified clockwise.

def getPerpVector(vectorTuple):
    (x, y) = vectorTuple
    return (y, -x)

def getOtherPerpVector(vectorTuple):
    (x, y) = vectorTuple
    return normalize((-y, x))
    

    
class InvalidVector(Exception):
    pass


#New Code

############################

#Old Code.  To phase out soon.


class Vector:
    """Vectors are vital for specifying rays.  A vector has the ability to set its X or Y value, or its direction
       or magnitude (updates must be made with these changes).  A vector also has the ability to return its 
       normalized counterpart."""
    	
    def __init__(self, vectorx, vectory):
        print "Vector Instantiated"
        self.vectorCacheState = True
        self.cartesianCacheState = True
        self.direction = 0
        self.magnitude = 0
        self.vectorx = round(vectorx, 5)
        self.vectory = round(vectory, 5)
        self.restoreVectorCacheState()
        
        
    def __str__(self):
        return 'Vector Instance: [%s, %s]' % (self.GetX(), self.GetY())
   
    def restoreMagnitude(self):
        self.magnitude = math.sqrt(math.pow(self.vectorx, 2) + math.pow(self.vectory, 2))
    
    def restoreDirection(self):
        self.direction = math.degrees(math.atan2(self.vectory, self.vectorx))
        
    def restoreX(self):
        self.vectorx = round(self.magnitude * math.cos(math.radians(self.direction)), 5)
        
    def restoreY(self):
        self.vectory = round(self.magnitude * math.sin(math.radians(self.direction)), 5)
   
    def restoreVectorCacheState(self):
        self.magnitude = math.sqrt(self.vectorx * self.vectorx + self.vectory * self.vectory)
        self.direction = math.degrees(math.atan2(self.vectory, self.vectorx))
        self.vectorCacheState = True
    
    def restoreCartesianCacheState(self):
        direction = math.radians(self.direction)
        self.vectorx = round(self.magnitude * math.cos(direction), 5)
        self.vectory = round(self.magnitude * math.sin(direction), 5)
        self.cartesianCacheState = True
    
    def getX(self):
        if not self.cartesianCacheState:
            self.restoreCartesianCacheState()
        return self.vectorx
       
    def getY(self):
        if not self.cartesianCacheState:
            self.restoreCartesianCacheState()
        return self.vectory
    
    def getXAndY(self):
        if not self.cartesianCacheState:
            self.restoreCartesianCacheState()
        return [self.getX(), self.getY()]
    
    def getDirection(self):
        if not self.vectorCacheState:
            self.restoreVectorCacheState()
        return self.direction
	
    def getMagnitude(self):
        if not self.vectorCacheState:
            self.restoreVectorCacheState()
        return self.magnitude                

    def setVector(self, vector):
        self = vector
        
    
    def setX(self, x):
        if not self.cartesianCacheState:
            self.restoreY()
        self.vectorx = round(x, 5)
        self.vectorCacheState = False
        self.cartesianCacheState = True

    
    def setY(self, y):
        if not self.cartesianCacheState:
            self.restoreX()
        self.vectory = round(y, 5)
        self.vectorCacheState = False
        self.cartesianCacheState = True
    
    def setXAndY(self, x, y):
        self.vectorx = round(x, 5)
        self.vectory = round(y, 5)
        self.vectorCacheState = False
        self.cartesianCacheState = True
        
    def setDirection(self, direction):
        if not self.vectorCacheState:
            self.restoreMagnitude()
        self.direction = direction
        self.cartesianCacheState = False
        self.vectorCacheState = True
            
    def setMagnitude(self, magnitude):
        if not self.vectorCacheState:
            self.restoreDirection()
        self.magnitude = magnitude
        self.cartesianCacheState = False
        self.vectorCacheState = True
    
    def normalize(self):
        self.setMagnitude(1)
    
    def getNormalized(self, resultant_vector=None):
        if not resultant_vector:
            newvector = Vector(self.vectorx, self.vectory)
            newvector.setMagnitude(1)
            return newvector
        else:
            resultant_vector.setXAndY(self.vectorx, self.vectory)
            resultant_vector.setMagnitude(1)
            return resultant_vector
    
    def getPerpVector(self, resultant_vector=None):
        if not resultant_vector:
            return Vector(-self.getY(), self.getX())
        else:
            resultant_vector.setXAndY(-self.getY(), self.getX())
            return resultant_vector
        
    def getInteriorPerpVector(self, resultant_vector=None):
        if not resultant_vector:
            return Vector(self.getY(), -self.getX())
        else:
            resultant_vector.setXAndY(self.getY(), -self.getX())
            return resultant_vector
        
    
    def truncate(self, threshold):
        self.setMagnitude(min(self.getMagnitude(), threshold))