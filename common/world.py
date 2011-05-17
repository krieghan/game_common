class World:
    def __init__(self, 
                 environment,
                 going=False):
        self.timestep = 0
        self.environment = environment
        self.objectreference = {}
        self.keywords = []
        self.hcells = 0
        self.vcells = 0
        self.going = going
    
    def announce(self, message):
        self.environment.Announce(message)
        
    def setHCells(self, hcells):
        self.hcells = hcells
        
    def setWCells(self, wcells):
        self.wcells = wcells
    
    def getWorldSize(self):
        return [self.environment.canvas.worldwidth, self.environment.canvas.worldheight]
    
    def getWorldWidth(self):
        return self.environment.canvas.worldwidth
    
    def getWorldHeight(self):
        return self.environment.canvas.worldheight
    
    def getAgentWidth(self):
        return self.environment.canvas.agent_width
        
    def getAgentHeight(self):
        return self.environment.agent_height
    
    def getHCells(self):
        return self.hcells
    
    def getWCells(self):
        return self.wcells
    
    def getHLength(self):
        return self.GetWorldHeight() / self.hcells
    
    def getWLength(self):
        return self.GetWorldWidth() / self.wcells
    
    def addObject(self, keyword, object):
        self.objectreference[keyword] = object
        self.keywords.append(keyword)
        
    def getObject(self, keyword):
        return self.objectreference[keyword]

    def updateTimeStep(self):
        self.timestep = (self.timestep + 1) % 1000000000.0
        

        