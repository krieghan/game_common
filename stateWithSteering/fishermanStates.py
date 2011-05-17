from State import *
from random import random
from BaseGameEntity import *
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher

class Fisherman_Global(State):
    
    def execute(self, owner):
    
        if owner.IsBladderFull():
            owner.GetFSM().ChangeState(state_manager['fisherman_seek_bladder_relief'])
        elif owner.IsEncumbered():
            owner.FixEncumberment()
        elif owner.IsThirsty():
            owner.GetFSM().ChangeState(state_manager['fisherman_drink'])
        elif owner.IsHungry():
            owner.GetFSM().ChangeState(state_manager['fisherman_dinner'])
        elif owner.IsTired():
            owner.GetFSM().ChangeState(state_manager['fisherman_sleep'])
        elif owner.HasEnoughFish():
            owner.GetFSM().ChangeState(state_manager['fisherman_deposit'])
        else:
            owner.GetFSM().ChangeState(state_manager['fisherman_fish'])             
        
            
            
class Fisherman_UGS(Unconditional_Global_State):
    def execute(self, owner):
        owner.attributes['thirst'] += 1
        owner.attributes['hunger'] += 1
        owner.attributes['fatigue'] += 1

    
class Fisherman_Fish(State):
    def precondition(self, owner):
        if owner.AtLocation('lake'):
            owner.ArrivedAtLocation('lake')
            owner.Announce("Fishing")
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['lake'].point)
        owner.Announce("Walking to the lake.")
        return False
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['lake'].point)
                
    def execute(self, owner):
        quantity = int(random() * 4)
        owner.items['fish'].AddQuantity(quantity)
                
        
    def exit(self, owner):
        pass
        
class Fisherman_Deposit(State):
    
    def precondition(self, owner):
        
        momlocation = agent_manager['miner_wife'].location
        arrivalpoint = momlocation
        if not hasattr(momlocation, 'point'):
            arrivalpoint = agent_manager['miner_wife']
        if owner.AtLocation(arrivalpoint):
            owner.ArrivedAtLocation(momlocation)
            owner.Announce('Looking for Mom.')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', arrivalpoint.point)
        owner.Announce("Walking to Mom")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', agent_manager['miner_wife'].location.point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        message_dispatcher.ScheduleMessage(Message(owner, agent_manager['miner_wife'], 'givefish', 0, owner.items['fish'].attributes['quantity'], owner.world))

    def exit(self, owner):
        owner.GetFSM().ReleaseGlobal()

class Fisherman_Saloon(State):
    def precondition(self, owner):
        if owner.AtLocation('saloon'):
            owner.ArrivedAtLocation('saloon')
            owner.Announce('Having a beer.')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['saloon'].point)
        owner.Announce("Walking to the saloon.")
        return False
    
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['saloon'].point)
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.attributes['thirst'] -= int(random() * 6)
        owner.attributes['bladder'] += int(random() * 4)
        
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()
            
class Fisherman_Home_Dinner(State):
    
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce('Waiting for Dinner.')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking to Kitchen.")
        return False
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        pass
        
class Fisherman_Home_Eating(State):
    
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce('Eating Dinner.')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking to the kitchen.")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.ChangeLocation('outside')
        
    def execute(self, owner):
        owner.attributes['hunger'] -= int(random() * 6)
        owner.attributes['thirst'] -= int(random() * 6)
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()
        
class Fisherman_Home_Sleep(State):
    
    def precondition(self, owner):
        if owner.AtLocation('fisher_bedroom'):
            owner.ArrivedAtLocation('fisher_bedroom')
            owner.Announce('Fast Asleep')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['fisher_bedroom'].point)
        owner.Announce("Walking to bedroom.")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['fisher_bedroom'].point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        owner.attributes['fatigue'] -= int(random() * 8)
        if owner.IsFatigueSatisfied():
            owner.GetFSM().ReleaseGlobal()
            
    def exit(self, owner):
        pass
    
class Fisherman_Seek_Bladder_Relief(State):
    
    def precondition(self, owner):
        if owner.AtLocation('lake'):
            owner.ArrivedAtLocation('lake')
            owner.Announce('Urinating')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['lake'].point)
        owner.Announce("Walking to the lake.")
        return False
    
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.steer.Activate('arrive', location_manager['lake'].point)
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
        
    def execute(self, owner):
        owner.attributes['bladder'] -= int(random() * 8)
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
            
    def exit(self, owner):
        pass
        
        