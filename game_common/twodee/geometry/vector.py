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

def pick_closest_vector(vector_tuple, candidate_vectors):
    vector_radians = getDirectionRadians(vector_tuple)
    closest_vector = None
    closest_difference = None
    for candidate in candidate_vectors:
        candidate_radians = getDirectionRadians(candidate)
        difference = abs(vector_radians - candidate_radians)
        if closest_difference is None or difference < closest_difference:
            closest_vector = candidate
            closest_difference = difference

    return closest_vector

#"Outside" and "Inside" assume a shape that is specified clockwise.

def getRightPerpendicular(vectorTuple):
    (x, y) = vectorTuple
    return (y, -x)

def getLeftPerpendicular(vectorTuple):
    (x, y) = vectorTuple
    return normalize((-y, x))
    
class InvalidVector(Exception):
    pass
