
class AttackerSelector(object):
    def __init__(self,
                 agent):
        self.agent = agent
        self.canvas = agent.canvas
        self.steeringController = agent.getSteeringController()
        
        self.steeringController.activate('avoidobstacles', self.canvas.obstacles)
        self.steeringController.activate('avoidwalls', self.canvas.walls)
        self.steeringController.activate('wander')
    
    def update(self,
               timeStep):
        self.flock()
        
    def flock(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = self.canvas
        
#        neighbors = canvas.attackers
        
        neighbors = canvas.getElementsWithinDistanceSquared(
                                        agent=agent,
                                        elementTypes=('attacker',),
                                        distanceThresholdSquared=10000)
        
        steeringController.activate('flock',
                                    neighbors)
        

    def parade(self):
        steeringController = self.steeringController
        
        canvas = self.canvas
        attackers = canvas.attackers
        if not attackers:
            steeringController.activate('wander')
            return
        
        agent = self.agent
        
        agentToFollow = attackers[-1]
        steeringController.activate('pursueoffset',
                                    agentToFollow,
                                    (-100, 0))
        steeringController

    def followCourse(self):
        agent = self.agent
        steeringController = self.steeringController
        if steeringController.getPath():
            return
        
        points = [(300, 300),
                  (300, 900),
                  (500, 500),
                  (700, 200)]
        steeringController.plotPath(points=points,
                                    closed=True)
        steeringController.deactivate('wander')
        steeringController.activate('followpath')

    def pursueClosestDefender(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestDefender = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('defender',))
        if closestDefender:
            steeringController.activate('pursue',
                                        closestDefender)
            steeringController.deactivate('wander')

        
    def arriveAtClosestTarget(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestTarget = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('target',))
        if closestTarget:
            closestTargetPosition = closestTarget.getPosition()
            steeringController.activate('arrive',
                                        closestTargetPosition)
            steeringController.deactivate('wander')
    
    
    def seekClosestDefender(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestDefender = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('defender',))
        if closestDefender:
            closestDefenderPosition = closestDefender.getPosition()
            steeringController.activate('seek',
                                        closestDefenderPosition)
 
class DefenderSelector(object):
    def __init__(self,
                 agent):
        self.agent = agent
        self.canvas = agent.canvas
        self.steeringController = agent.getSteeringController()
        self.steeringController.activate('avoidobstacles', self.canvas.obstacles)
        self.steeringController.activate('avoidwalls', self.canvas.walls)
        
    def update(self,
               timeStep):
        self.hideFromClosestAttacker()
    
    def hideFromClosestAttacker(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestAttacker = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('attacker',))
        
        if not closestAttacker:
            return
        
        steeringController.deactivate('wander')
        steeringController.activate('hide',
                                    closestAttacker,
                                    canvas.obstacles)
    
    def interposeAttackerAndStationary(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestAttacker = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('attacker',))
        if not closestAttacker:
            return
        
        closestStationaryTarget = canvas.getClosestCanvasElement(agent=agent,
                                                                 elementTypes=('target',))
        
        if not closestStationaryTarget:
            return
        
        steeringController.deactivate('wander')
        steeringController.activate('interpose',
                                    closestAttacker,
                                    closestStationaryTarget)
        
    
    
    def evadeOrInterposeAttacker(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestAttacker = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('attacker',))
        if not closestAttacker:
            return
        
        target = closestAttacker.getTarget()
        
        steeringController.deactivate('wander')
        
        if target == agent:
            steeringController.deactivate('interpose')
            steeringController.activate('evade',
                          closestAttacker)
        else:
            steeringController.deactivate('evade')
            steeringController.activate('interpose',
                                        closestAttacker,
                                        target)
            
            
    
    def fleeClosestAttacker(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestAttacker = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('attacker',))
        if closestAttacker:
            closestAttackerPosition = closestAttacker.getPosition()
            steeringController.activate('flee',
                                        closestAttackerPosition)
            
    def evadeClosestAttacker(self):
        agent = self.agent
        steeringController = self.steeringController
        canvas = agent.canvas
        closestAttacker = canvas.getClosestCanvasElement(agent=agent,
                                                         elementTypes=('attacker',))
        if closestAttacker:
            steeringController.activate('evade',
                                        closestAttacker)