from SteeringBehaviors import SteeringBehaviors
from common import geometry
from EntityManager import EntityManager, ItemManager, AttributeManager, StatusManager
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher
from Machines import StateMachine

from common.Vector import Vector
from common.Point import Point
from common.State import State


vector1 = Vector(0, 0)
vector2 = Vector(0, 0)
vector3 = Vector(0, 0)
vector4 = Vector(0, 0)

point1 = Point(0, 0)
class BaseGameEntity(object):
    currentid = 0
    
    def __init__(self, name=None, world=None, key=None):
        self.id = self.__class__.currentid
        self.__class__.currentid += 1
        self.name = name
        self.location = None
        self.world = world
        self.vector1 = Vector(0, 0)
        self.key = key
        
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name        
    
    def announce(self, message):
        self.world.announce("%d: %s - '%s'" % (self.world.timestep, self.name, message))
        
    def handleMessage(self, message):
        pass

    def scheduleMessage(self, message):
        return message_dispatcher.scheduleMessage(message)

    def changeLocation(self, new_location):
        if type(new_location) == str:
            new_location = location_manager[new_location]

        if location_manager.hasKey(self.name):
            self.location.popitem(self.name)
         
        self.location = new_location
        self.location[self.name] = self



        
class Agent(BaseGameEntity):
    def __init__(self, name=None, start_state=State(), global_state=State(), unconditional_global_state=State(), world=None):
        BaseGameEntity.__init__(self, name, world=world)
        self.fsm = StateMachine(self, start_state, global_state, unconditional_global_state)
        self.items = ItemManager()
        self.attributes = AttributeManager()
        self.interact = True
        self.status = StatusManager()

        
    def updateState(self):
        self.fsm.update()
        
    def getEncumberance(self):
        encumberance = 0
        for item in self.items.getValues():
            encumberance += item.quantity * item.weight
        return encumberance
        
    def getFSM(self):
        return self.fsm
    
    def setGlobalState(self, state):
        self.fsm.setGlobalState(self, state)

    
    def lockInteraction(self):
        self.interact = False
        
    def releaseInteraction(self):
        self.interact = True

class MovingEntity:

    def __init__(self, parent, point, velocity):
        
        self.world = parent
        self.steer = SteeringBehaviors(self, self.world)
        self.point = point
        self.velocity = velocity

        self.heading = self.velocity.getNormalized()
        self.side = self.heading.getPerpVector()
        
        self.vector1 = globals()['vector1']
        self.vector2 = globals()['vector2']
        
        self.point1 = globals()['point1']
        
        self.force = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.force = Vector(0, 0)
        
        self.mass = .01
        self.maxvelocity = 5
        self.maxforce = 500

        self.waypoint_activation_distance = 7
        
        self.agent_width = 16
        self.agent_height = 8
        
        self.min_detection_length = 120
        
        self.obs_detection_box_length = self.min_detection_length + (self.velocity.getMagnitude() / self.maxvelocity) * self.min_detection_length
        self.obs_detection_box_width = self.agent_height
        
        self.neighbor_proximity = 50
        self.neighboring_vehicles = []
        self.neighbor_types = []
    
    
    #Mutators:
    
    
    
    def setMass(self, mass):
        self.mass = mass
    
    def setMaxVelocity(self, maxvelocity):
        self.maxvelocity = maxvelocity
    
    def setMaxForce(self, maxforce):
        self.maxforce = maxforce
    
    def setObstacleDetectionBox(self, box, index = -1):
        if index == -1:
            self.obs_detection_box_length = box[1]
            self.obs_detection_box_width = box[0]
        if index == 0:
            self.obs_detection_box_width = box[0]
        if index == 1:
            self.obs_detection_box_length = box[1]
        
    def setAgentWidth(self, width):
        self.agent_width = width
    
    def setAgentHeight(self, height):
        self.agent_height = height
    
    def setNeighborProximity(self, prox):
        self.neighbor_proximity = prox
        
    def setPoint(self, point):
        self.point = point
    
    def setVelocity(self, velocity):
        self.velocity = velocity
            
    def SetAcceleration(self, acc):
        self.acceleration = acc
    
    #Accesors:
    
    def getAgentWidth(self):
        return self.agent_width
        
    def getAgentHeight(self):
        return self.agent_height
    
    
    def getMaxVelocity(self):
        return self.maxvelocity
    
    def getMaxForce(self):
        return self.maxforce
    
    def getMass(self):
        return self.mass
    
    def getNeighboringVehicles(self):
        return self.neighboring_vehicles
    
    def getPoint(self):
        return self.point
    
    def getVelocity(self):
        return self.velocity
    
    def getHeading(self):
        return self.heading
    
    def getSide(self):
        return self.side
    
    def getObstacleDetectionBox(self, index=-1):
        if index == -1:
            return [self.obs_detection_box_width, self.obs_detection_box_length]
        if index == 0:
            return self.obs_detection_box_width
        if index == 1:
            return self.obs_detection_box_length
    
    def getWaypointDistance(self):
        return self.waypoint_activation_distance
    
    def modifyAcceleration(self, modifier):
        self.acceleration += modifier
    
    def findNearest(self, mode):
        if mode == 0:
            defender = self.world.getObject('defender')
            if len(defender) >= 1:
                minelement = defender[0]
                minelementmag2 = geometry.getMagnitudeSquared(
                                    geometry.subPoints(self.point, 
                                                       minelement.point, 
                                                       resultant_vector=self.vector1))
            else:
                minelement = None
            for element in defender:
                candidate_magnitude = geometry.getMagnitudeSquared(
                                            geometry.subPoints(self.getPoint(), 
                                                               element.getPoint(), 
                                                               resultant_vector=self.vector1))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
                    
        elif mode == 1:
            attacker = self.world.getObject('attacker')
            if len(attacker) >= 1:
                minelement = attacker[0]
                minelementmag2 =\
                    geometry.getMagnitudeSquared(geometry.subPoints(
                                                self.point, 
                                                minelement.point, 
                                                resultant_vector=self.vector1))
            else:
                minelement = None
            for element in attacker:
                candidate_magnitude = geometry.getMagnitudeSquared(
                                        geometry.subPoints(self.getPoint(), 
                                                           element.getPoint(), 
                                                           resultant_vector=self.vector1))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
        
        elif mode == 2:
            targets = self.world.getObject('target')
            minelement = targets[0]
            minelementmag2 = geometry.getMagnitudeSquared(
                                geometry.subPoints(self.point, 
                                                   minelement.point, 
                                                   resultant_vector=self.vector1))
            for element in targets:
                candidate_magnitude = geometry.getMagnitudeSquared(
                                        geometry.subPoints(self.getPoint(), 
                                                           element.getPoint(), 
                                                           resultant_vector=self.vector1))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
                    
        return minelement
                    
    def updatePosition(self, time):
        self.updateBehaviors()
        if self.world.timestep % 10 == 0:
            self.findNeighbors()
            
        self.force.setXAndY(*self.calculate().getXAndY())
        self.force.setMagnitude(min(self.maxforce, self.force.getMagnitude()))
        
        self.vector1 = geometry.multScalar(1.0 / self.mass, 
                                           self.force, 
                                           resultant_vector=self.vector1)
        self.vector1 = geometry.multScalar(time, 
                                           self.vector1, 
                                           resultant_vector=self.vector1)
        
        self.acceleration.setXAndY(*self.vector1.getXAndY())
        

        self.vector1 = geometry.addVectors(self.velocity, 
                                           self.acceleration, 
                                           resultant_vector=self.vector1)
        self.velocity.setXAndY(*self.vector1.getXAndY())
        

        
        self.velocity.truncate(self.maxvelocity)
        
        if self.velocity.getMagnitude() > .0000001:
            self.heading.setXAndY(*self.velocity.getNormalized(resultant_vector=self.vector1).getXAndY())
            self.side = self.heading.getPerpVector(resultant_vector=self.vector2)
                                
        
        self.point1 = geometry.addPointAndVector(self.point, 
                                                 self.velocity, 
                                                 resultant_point=self.point1)
        (x, y) = self.point1.getXAndY()
        self.point.setXAndY(x % self.world.getWorldWidth(), y % self.world.getWorldHeight())
    
        self.obs_detection_box_length = self.min_detection_length + (self.velocity.getMagnitude() / self.maxvelocity) * self.min_detection_length
        
        
    def findNeighbors(self):
        container = self.getEligibleNeighbors()
        
        for agent in container:
            if agent != self:
                distance = geometry.subPoints(agent.point, self.point, resultant_vector=self.vector1).getMagnitude()
                if distance < self.neighbor_proximity:
                    self.neighboring_vehicles.append(agent)
                    
    def calculate(self):
        return self.steer.calculate()
                
          
class MovingAgent(Agent, MovingEntity):
    def __init__(self, 
                 point, 
                 velocity, 
                 name=None, 
                 start_state=None, 
                 global_state=None, 
                 unconditional_global_state=None, 
                 world=None):
        if start_state is None:
            start_state = State()
        if global_state is None:
            global_state = State()
        if unconditional_global_state is None:
            unconditional_global_state = State()
        Agent.__init__(self, name, start_state, global_state, unconditional_global_state, world)
        MovingEntity.__init__(self, world, point, velocity)
        
    def update(self, time):
        self.updateState()
        self.updatePosition(time)
    
    def distanceToLocation(self, location):
        if type(location) == str:
            location = location_manager[location]
            
        return geometry.subPoints(self.point, 
                                  location.point, 
                                  resultant_vector=self.vector1).getMagnitude()
        
        
    def atLocation(self, location):
        if round(self.distanceToLocation(location), -1) == 0:
            return True
        else:
            return False
        
    def arrivedAtLocation(self, location):
        self.steer.deactivate('arrive')
        self.velocity.setXAndY(0, 0)
        self.changeLocation(location)
            

class Message(BaseGameEntity):
    def __init__(self, source, destination, message, dispatchTime, extraInfo=None, world=None):
        BaseGameEntity.__init__(self, message, world=world)
        self.source = source
        self.destination = destination
        self.message = message
        self.dispatchTime = self.world.timestep + dispatchTime
        self.extraInfo = extraInfo

    def getDispatchTime(self):
        return self.dispatchTime

class Item(BaseGameEntity):
    def __init__(self, 
                 name=None, 
                 value=0, 
                 weight=5, 
                 durability=100, 
                 quantity=1, 
                 manager=None, 
                 world=None):
        BaseGameEntity.__init__(self, name, world=world)
        self.items = ItemManager()
        self.manager=manager
        self.attributes = AttributeManager()
        self.attributes['value'] = value
        self.attributes['weight'] = weight
        self.attributes['durability'] = durability
        self.attributes['quantity'] = quantity
    
    def getManager(self):
        return self.manager
    
    def setManager(self, manager):
        self.manager = manager
        
    def addQuantity(self, quantity):
      self.attributes['quantity'] += quantity
      
