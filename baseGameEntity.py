from Behaviors import *
from State import *

class BaseGameEntity:
    currentid = 0
    
    def __init__(self, name=None, world=None):
        self.id = self.__class__.currentid
        self.__class__.currentid += 1
        self.name = name
        self.location = None
        self.world = world
        
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name        
    
    def Announce(self, message):
        
        #globals()['world'].f.write("%d: %s - '%s'\n" % (globals()['time_step'], self.name, message))
        print "%d: %s - '%s'" % (self.world.timestep, self.name, message)
        
    def HandleMessage(self, message):
        pass


        
class Agent(BaseGameEntity, DispatchesMessages, HasLocation, HasState, HasAgents):
    def __init__(self, name=None, start_state=State(), global_state=State(), unconditional_global_state=State(), world=None):
        BaseGameEntity.__init__(self, name, world=world)
        self.fsm = StateMachine(self, start_state, global_state, unconditional_global_state)
        self.items = ItemManager()
        self.attributes = AttributeManager()
        self.interact = True
        
        self.attributes['wealth'] = 0
        self.attributes['hunger'] = 0
        self.attributes['fatigue'] = 0
        self.attributes['thirst'] = 0
        self.attributes['bladder'] = 0
        self.attributes['strength'] = 20
        self.attributes['speed'] = 50
        self.attributes['endurance'] = 50
        self.attributes['composure'] = 20
        self.attributes['greed'] = 30
        
        self.attributes['encumberance'] = self.GetEncumberance()

        self.attributes['fatigue_lower_threshold'] = 10
        self.attributes['fatigue_upper_threshold'] = 15
        self.attributes['hunger_lower_threshold'] = 20
        self.attributes['hunger_upper_threshold'] = 25
        self.attributes['thirst_lower_threshold'] = 10
        self.attributes['thirst_upper_threshold'] = 13
        self.attributes['encumberance_lower_threshold'] = self.attributes['strength'] * 1.9
        self.attributes['encumberance_upper_threshold'] = self.attributes['strength'] * 2.1
        self.attributes['bladder_lower_threshold'] = self.attributes['endurance'] / 10
        self.attributes['bladder_upper_threshold'] = self.attributes['endurance'] / 5
        
        #self.agent_manager[name] = self
        
    def update(self):
        self.fsm.update()
        
    def GetEncumberance(self):
        encumberance = 0
        for item in self.items.GetValues():
            encumberance += item.quantity * item.weight
        return encumberance
        
    def GetFSM(self):
        return self.fsm
    
    def SetGlobalState(self, state):
        self.fsm.SetGlobalState(self, state)

    def IsFatigueSatisfied(self):
      return self.attributes['fatigue'] < self.attributes['fatigue_lower_threshold']
    
    def IsThirstSatisfied(self):
        return self.attributes['thirst'] < self.attributes['thirst_lower_threshold']
        
    def IsHungerSatisfied(self):
        return self.attributes['hunger'] < self.attributes['hunger_lower_threshold']
    
    def IsBladderSatisfied(self):
        return self.attributes['bladder'] < self.attributes['bladder_lower_threshold']
    
    def IsEncumberanceLow(self):
        return self.attributes['encumberance'] < self.attributes['encumberance_lower_threshold']
    
    def IsTired(self):
      return self.attributes['fatigue'] > self.attributes['fatigue_upper_threshold']
    
    def IsEncumbered(self):
        return self.attributes['encumberance'] > self.attributes['encumberance_upper_threshold']

    def IsBladderFull(self):
        return self.attributes['bladder'] > self.attributes['bladder_upper_threshold']
    
    def IsHungry(self):
        return self.attributes['hunger'] > self.attributes['hunger_upper_threshold']

    def IsThirsty(self):
        return self.attributes['thirst'] > self.attributes['thirst_upper_threshold']

    def LockInteraction(self):
        self.interact = False
        
    def ReleaseInteraction(self):
        self.interact = True
        
class Location(BaseGameEntity, HasState, DispatchesMessages):
    def __init__(self, name, world=None):
        BaseGameEntity.__init__(self, name, world=world)
        
        self.items = ItemManager()
        self.agents = AgentManager()
    
    def __getitem__(self, name):
        if self.items.has_key(name):
            return self.items[name]
        if self.agents.has_key(name):
            return self.agents[name]
        else:
            raise ItemNotFound()
    

    def __setitem__(self, name, element):
        if type(element) == type(Agent()):
            if self.agents.HasKey(name):
                del self.agents[name].location[name]
            self.agents[name] = element
            element.location = self
        elif type(element) == type(Item()):
            if self.items.HasKey(name):
               del self.items[name].location[name]
            self.items[name] = element
            element.location = self
        else:
            raise TypeMismatch()
                
    def __delitem__(self, name):
        if self.agents.HasKey(name):
            del self.agents[name]
        elif self.items.HasKey(name):
            del self.items[name]
         
   
    def HandleMessage(self, message):
        self.message_dispatcher.ScheduleMessage(Message(message.source, self.GetContents(), message.message, 0, None, world=self.world))

    def GetItems(self):
        return self.items
    
    def GetAgents(self):
        return self.agents
       
    def GetContents(self):
        return self.GetItems() + self.GetAgents()        

class Message(BaseGameEntity):
    def __init__(self, source, destination, message, dispatchTime, extraInfo=None, world=None):
        BaseGameEntity.__init__(self, message, world=world)
        self.source = source
        self.destination = destination
        self.message = message
        self.dispatchTime = self.world.timestep + dispatchTime
        self.extraInfo = extraInfo

    
    #def __cmp__(self, message):
    #    return cmp(self.GetDispatchTime(), message.GetDispatchTime())

    
    def GetDispatchTime(self):
        return self.dispatchTime

class Item(BaseGameEntity, HasState, HasLocation, DispatchesMessages):
    def __init__(self, name = None, value=0, weight=5, durability=100, quantity=1, manager=None, world=None):
        BaseGameEntity.__init__(self, name, world=world)
        self.items = ItemManager()
        self.manager=manager
        self.attributes = AttributeManager()
        self.attributes['value'] = value
        self.attributes['weight'] = weight
        self.attributes['durability'] = durability
        self.attributes['quantity'] = quantity
    
    def GetManager(self):
        return self.manager
    
    def SetManager(self, manager):
        self.manager = manager
        
    def AddQuantity(self, quantity):
      self.attributes['quantity'] += quantity
      
class MovingEntity:

    def __init__(self, parent, Point, Velocity):
        
        self.world = parent
        self.steer = SteeringBehaviors(self, self.world)
        self.point = Point
        self.velocity = Velocity

        self.heading = self.velocity.GetNormalized()
        self.side = self.heading.GetPerpVector()
        
        
        self.force = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        
        self.mass = .1
        self.maxvelocity = 5
        self.maxforce = 500

        self.waypoint_activation_distance = 7
        
        self.agent_width = 16
        self.agent_height = 8
        
        self.min_detection_length = 120
        
        self.obs_detection_box_length = self.min_detection_length + (self.velocity.GetMagnitude() / self.maxvelocity) * self.min_detection_length
        self.obs_detection_box_width = self.agent_height
        
        self.neighbor_proximity = 300
        self.neighboring_vehicles = []
    
    
    #Mutators:
    
    
    
    def SetMass(self, mass):
        self.mass = mass
    
    def SetMaxVelocity(self, maxvelocity):
        self.maxvelocity = maxvelocity
    
    def SetMaxForce(self, maxforce):
        self.maxforce = maxforce
    
    def SetObstacleDetectionBox(self, box, index = -1):
        if index == -1:
            self.obs_detection_box_length = box[1]
            self.obs_detection_box_width = box[0]
        if index == 0:
            self.obs_detection_box_width = box[0]
        if index == 1:
            self.obs_detection_box_length = box[1]
        
    def SetAgentWidth(self, width):
        self.agent_width = width
    
    def SetAgentHeight(self, height):
        self.agent_height = height
    
    def SetNeighborProximity(self, prox):
        self.neighbor_proximity = prox
        
    def SetPoint(self, Point):
        self.point = Point
    
    def SetVelocity(self, Velocity):
        self.velocity = Velocity
            
    def SetAcceleration(self, Acc):
        self.acceleration = Acc
    
    #Accesors:
    
    def GetAgentWidth(self):
        return self.agent_width
        
    def GetAgentHeight(self):
        return self.agent_height
    
    
    def GetMaxVelocity(self):
        return self.maxvelocity
    
    def GetMaxForce(self):
        return self.maxforce
    
    def GetMass(self):
        return self.mass
    
    def GetNeighboringVehicles(self):
        return self.neighboring_vehicles
    
    def GetPoint(self):
        return self.point
    
    def GetVelocity(self):
        return self.velocity
    
    def GetHeading(self):
        return self.heading
    
    def GetSide(self):
        return self.side
    
    def GetObstacleDetectionBox(self, index = -1):
        if index == -1:
            return [self.obs_detection_box_width, self.obs_detection_box_length]
        if index == 0:
            return self.obs_detection_box_width
        if index == 1:
            return self.obs_detection_box_length
    
    def GetWaypointDistance(self):
        return self.waypoint_activation_distance
    
        
    
    
    def ModifyAcceleration(self, modifier):
        self.acceleration += modifier
    
    def FindNearest(self, mode):
        if mode == 0:
            defender = self.world.GetObject('defender')
            if len(defender) >= 1:
                minelement = defender[0]
                minelementmag2 = GetMagnitudeSquared(SubPoints(self.point, minelement.point))
            else:
                minelement = None
            for element in defender:
                candidate_magnitude = GetMagnitudeSquared(SubPoints(self.GetPoint(), element.GetPoint()))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
                    
        elif mode == 1:
            attacker = self.world.GetObject('attacker')
            if len(attacker) >= 1:
                minelement = attacker[0]
                minelementmag2 = GetMagnitudeSquared(SubPoints(self.point, minelement.point))
            else:
                minelement = None
            for element in attacker:
                candidate_magnitude = GetMagnitudeSquared(SubPoints(self.GetPoint(), element.GetPoint()))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
        
        elif mode == 2:
            minelement = self.world.target[0]
            minelementmag2 = GetMagnitudeSquared(SubPoints(self.point, minelement.point))
            for element in self.world.target:
                candidate_magnitude = GetMagnitudeSquared(SubPoints(self.GetPoint(), element.GetPoint()))
                if candidate_magnitude < minelementmag2:
                    minelement = element
                    minelementmag2 = candidate_magnitude
                    
        return minelement
                    
    def Update(self, time):
        if self.world.timestep % 10 == 0:
            self.FindNeighbors()
            
        force = self.Calculate()
        force.SetMagnitude(min(self.maxforce, force.GetMagnitude()))
        
        self.acceleration = MultScalar(1.0 / self.mass, force)
        self.acceleration = MultScalar(time, self.acceleration)

        self.velocity = AddVectors(self.velocity, self.acceleration)

        self.velocity.Truncate(self.maxvelocity)
        
        if self.velocity.GetMagnitude() > .0000001:
            self.heading = self.velocity.GetNormalized()
            self.side = self.heading.GetPerpVector()
                                
        
        self.point = AddPointAndVector(self.point, self.velocity)
    
        self.point.SetXAndY(self.point.GetX() % self.world.GetWorldWidth(), self.point.GetY() % self.world.GetWorldHeight())
        self.obs_detection_box_length = self.min_detection_length + (self.velocity.GetMagnitude() / self.maxvelocity) * self.min_detection_length
        
    def FindNeighbors(self):
        if self.mode == "attack":
            container = self.world.GetObject('attacker')
        if self.mode == "defend":
            container = self.world.GetObject('defender')
            
        for agent in container:
            if agent != self:
                distance = SubPoints(agent.point, self.point).GetMagnitude()
                if distance < self.neighbor_proximity:
                    self.neighboring_vehicles.append(agent)
                
          
