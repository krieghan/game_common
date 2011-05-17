from BaseGameEntity import *
from Items import *
from WestWorldStates import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import math

def DrawCircle(radius=50, numlines=12):
    glBegin(GL_POLYGON)
    for i in xrange(numlines):
        glVertex3f(radius * math.cos((i * 2 * math.pi) / numlines), radius * math.sin((i * 2 * math.pi) / numlines), 0)
    glEnd()


class WestWorldAgent(MovingAgent):

    def __init__(self, Point, Velocity, name=None, status_manager=None, start_state=State(), global_state=State(), unconditional_global_state=State(), world=None):
        MovingAgent.__init__(self, Point, Velocity, name, start_state, global_state, unconditional_global_state, world)
        self.color = [1, 1, 1]
        self.status_manager = status_manager
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

        self.attributes['fatigue_lower_threshold'] = 100
        self.attributes['fatigue_upper_threshold'] = 400
        self.attributes['hunger_lower_threshold'] = 100
        self.attributes['hunger_upper_threshold'] = 500
        self.attributes['thirst_lower_threshold'] = 300
        self.attributes['thirst_upper_threshold'] = 900
        self.attributes['encumberance_lower_threshold'] = self.attributes['strength'] * 1.9
        self.attributes['encumberance_upper_threshold'] = self.attributes['strength'] * 2.1
        self.attributes['bladder_lower_threshold'] = self.attributes['endurance'] * 3
        self.attributes['bladder_upper_threshold'] = self.attributes['endurance'] * 4
        
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

    def Draw(self, radius=20):
        glPushMatrix()
        glTranslate(self.GetPoint().GetX(), self.GetPoint().GetY(), 0)
        glColor3f(*self.color)
        DrawCircle(radius=radius)
        glColor3f(1, 1, 1)
        glPopMatrix()

    def Announce(self, status):
        
        self.status['status'] = status
        
class Miner(WestWorldAgent):
    def __init__(self, Point, Velocity, name=None, status_manager=None, start_state = Miner_Mine(), global_state = Miner_Global(), unconditional_global_state=Miner_UGS(), world=None):
        super(Miner, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, unconditional_global_state, world=world)
        self.color = [0, 0, 1]
        self.items['gold'] = Item(name='Gold nugget', value=20, weight=5, durability=70, manager=self.items)
        self.items['mining tool'] = Item(name='Mining tool', value=10, weight=10, durability=60, manager=self.items)
        self.items['clothing'] = Clothing(name='Mining clothes', value=2, weight=3, durability=70, manager=self.items)
        self.attributes['greed'] = 80
        self.attributes['enough_gold'] = self.attributes['greed'] / 10
        self.wife=None
        
    def HandleMessage(self, Message):
         #print Message, Message.message
         if not self.interact:
            return
            
         if Message.message == 'stewdone':
            self.GetFSM().ChangeState(state_manager['miner_eating'])
         
    def HasEnoughGold(self):
        return self.items['gold'].attributes['quantity'] > self.attributes['enough_gold']
        
class Housewife(WestWorldAgent):
   def __init__(self, Point, Velocity, name=None, status_manager=None, start_state=State(), global_state=State(), unconditional_global_state=Wife_UGS(), world=None):
        super(Housewife, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, unconditional_global_state, world=world)
        self.color = [0, 1, 1]
        self.cooking_now = 0
        self.items['fish'] = Food(name='Fish', value=4, weight=2, durability=60, manager=self.items, quantity=0)
        
   def HandleMessage(self, message):
        if not self.interact:
            return
        
        if message.message == 'givefish':
            self.items['fish'].AddQuantity(message.extraInfo)
            message_dispatcher.ScheduleMessage(Message(self, message.source, 'fishtaken', 0, message.extraInfo, self.world))
        
        if message.message == 'imhome':
            if not self.cooking_now:
                self.GetFSM().ChangeState(state_manager['wife_cook_meal'])
        elif message.message =='stewdone':
            self.GetFSM().ChangeState(state_manager['wife_eat_stew'])
        #else:
            #raise InvalidMessage()
            

class Fisherman(WestWorldAgent):
    def __init__(self, Point, Velocity, name = None, status_manager=None, start_state = State(), global_state = State(), unconditional_global_state=State(), world=None):
        super(Fisherman, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, world=world)
        self.color = [0, 1, 0]
        self.items['fish'] = Food(name='Fish', value=4, weight=2, durability=60, manager=self.items)
        self.items['fishing_pole'] = Item(name='Fishing Pole', value=20, weight=5, durability=100, manager=self.items)
        self.attributes['enough_fish'] = self.attributes['greed'] / 10
    
    def HasEnoughFish(self):
        return self.items['fish'].attributes['quantity'] > self.attributes['enough_fish']
    
    def HandleMessage(self, Message):
        if not self.interact:
            return
        if Message.message == 'stewdone':
            self.GetFSM().ChangeState(state_manager['fisherman_eating'])
        if Message.message == 'fishtaken':
            self.items['fish'].attributes['quantity'] -= Message.extraInfo
            self.GetFSM().ChangeState(state_manager['fisherman_global_state'])
        
class Banker(WestWorldAgent):
    def __init__(self, Point, Velocity, name = None, status_manager=None, start_state = State(), global_state = State(), unconditional_global_state=State(), world=None):
        super(Banker, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, world=world)
        self.color = [1, 0, 0]
        
class Barfly(WestWorldAgent):
    def __init__(self, Point, Velocity, name = None, status_manager=None, start_state = State(), global_state = State(), unconditional_global_state=State(), world=None):
        super(Barfly, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, world=world)
        self.color = [1, 1, 0]
        
class Grocer(WestWorldAgent):    
    def __init__(self, Point, Velocity, name = None, status_manager=None, start_state = State(), global_state = State(), unconditional_global_state=State(), world=None):
        super(Grocer, self).__init__(Point, Velocity, name, status_manager, start_state, global_state, world=world)
        self.color = [1, 0, 1]