from State import *
from random import random
from BaseGameEntity import *

from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher

class Wife_UGS(State):
   def execute(self, owner):
      owner.attributes['thirst'] += 1
      owner.attributes['hunger'] += 1
      owner.attributes['fatigue'] += 1

        
class Wife_Global(State):
    def execute(self, owner):
        if owner.IsBladderFull():
            owner.GetFSM().ChangeState(state_manager['wife_seek_bladder_relief'])
        elif owner.IsHungry():
            owner.GetFSM().ChangeState(state_manager['wife_cook_meal'])
        elif owner.IsThirsty():
            owner.GetFSM().ChangeState(state_manager['wife_drink_coffee'])
        elif owner.IsTired():
            owner.GetFSM().ChangeState(state_manager['wife_sleep'])
        else:
            owner.GetFSM().ChangeState(state_manager['wife_putter_about'])
        
class Wife_Seek_Bladder_Relief(State):
    
    def precondition(self, owner):
        if owner.AtLocation('bathroom'):
            owner.ArrivedAtLocation('bathroom')
            owner.Announce('Urinating')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['bathroom'].point)
        owner.Announce("Walking to the bathroom")
        return False
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['bathroom'].point)
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
    
    def execute(self, owner):
        owner.attributes['bladder'] -= int(random() * 8)
        
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
        
    def exit(self, owner):
        pass
    
class Wife_Drink_Coffee(State):
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce('Drinking Coffee.')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking to the kitchen")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        owner.attributes['thirst'] -= int(random() * 8)
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()

    def exit(self, owner):
        pass
            
class Wife_Putter_About(State):
    def precondition(self, owner):
        if owner.AtLocation('miner_bedroom'):
            owner.ArrivedAtLocation('miner_bedroom')
            owner.Announce('Reading a magazine')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['miner_bedroom'].point)
        owner.Announce("Walking to bedroom")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['miner_bedroom'].point)
        owner.ChangeLocation('outside')
            
    def execute(self, owner):
        pass
        
    def exit(self, owner):
        pass
        
class Wife_Cook_Meal(State):
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce('Cooking the Stew')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking to the kitchen")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.ChangeLocation('outside')
        message_dispatcher.ScheduleMessage(Message(owner, owner, 'stewdone', 15, None, owner.world))
        self.cooking_now = 1
        owner.GetFSM().LockGlobal()

class Wife_Eat_Stew(State):
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce('Eating Dinner')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking to the kitchen")
        return False
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        message_dispatcher.ScheduleMessage(Message(owner, owner.location, 'stewdone', 0, None, owner.world))
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()
        else:
            owner.attributes['hunger'] -= int(random() * 8)
            owner.attributes['thirst'] -= int(random() * 8)
            
class Wife_Sleep(State):
    def precondition(self, owner):
        if owner.AtLocation('miner_bedroom'):
            owner.Announce('Fast Asleep')
            owner.ArrivedAtLocation('miner_bedroom')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['miner_bedroom'].point)
        owner.Announce("Walking to bedroom")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['miner_bedroom'].point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.attributes['fatigue'] -= int(random() * 8)
        
        if owner.IsFatigueSatisfied():
            owner.GetFSM().ReleaseGlobal()
            