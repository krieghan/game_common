from State import *
from random import random
from BaseGameEntity import *
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher
from geometry import SubPoints
from Vector import Vector

vector1 = Vector(0, 0)


class Miner_Global(State):
    def execute(self, owner):
        if owner.IsBladderFull():
            owner.GetFSM().ChangeState(state_manager['miner_seek_bladder_relief'])
    
        elif owner.IsEncumbered():
            owner.FixEncumberment()
        elif owner.IsThirsty():
            owner.GetFSM().ChangeState(state_manager['miner_drink'])
        elif owner.IsHungry():
            owner.GetFSM().ChangeState(state_manager['miner_dinner'])
        elif owner.IsTired():
            owner.GetFSM().ChangeState(state_manager['miner_sleep'])
        elif owner.HasEnoughGold():
            owner.GetFSM().ChangeState(state_manager['miner_deposit'])
        else:
            owner.GetFSM().ChangeState(state_manager['miner_mine'])
            
class Miner_UGS(Unconditional_Global_State):
    def execute(self, owner):
        owner.attributes['thirst'] += 1
        owner.attributes['hunger'] += 1
        owner.attributes['fatigue'] += 1

class Miner_Mine(State):
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['mine'].point)
        owner.ChangeLocation('outside')
        
    def precondition(self, owner):
        if owner.AtLocation('mine'):
            owner.ArrivedAtLocation('mine')
            owner.Announce("Mining for Gold")
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['mine'].point)
        owner.Announce('Walking to the Mine')
        return False

    def execute(self, owner):
        owner.items['gold'].AddQuantity(int(random() * 2))

        if owner.HasEnoughGold():
            owner.GetFSM().ChangeState(state_manager['miner_deposit'])

    def exit(self, owner):
        pass

class Miner_Home_Dinner(State):
    
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            message_dispatcher.ScheduleMessage(Message(owner, owner.wife, 'imhome', 0, None, world=owner.world))
            owner.Announce("Waiting for Dinner")
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['mine'].point)
        owner.Announce("Walking home for dinner")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.ChangeLocation('mine')
        
        owner.GetFSM().LockGlobal()

    def execute(self, owner):
        pass

class Miner_Home_Eating(State):
    def precondition(self, owner):
        if owner.AtLocation('kitchen'):
            owner.ArrivedAtLocation('kitchen')
            owner.Announce("Eating Dinner")
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.Announce("Walking home to eat")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['kitchen'].point)
        owner.ChangeLocation('kitchen')

    def execute(self, owner):
        
        owner.attributes['hunger'] -= int(random() * 8)
        owner.attributes['thirst'] -= int(random() * 8)
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()

class Miner_Home_Sleep(State):
    
    def precondition(self, owner):
        if owner.AtLocation('miner_bedroom'):
            owner.ArrivedAtLocation('miner_bedroom')
            owner.Announce("Fast asleep")
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
    
    
class Miner_Saloon(State):
    
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
        owner.steer.Activate('arrive', location_manager['saloon'].point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.attributes['thirst'] -= int(random() * 8)
        owner.attributes['bladder'] += int(random() * 4)
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()

class Miner_Bank(State):
    def precondition(self, owner):
        if owner.AtLocation('bank'):
            owner.ArrivedAtLocation('bank')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['bank'].point)
        owner.Announce("Walking to the bank")
        return False
    
    def enter(self, owner):
        owner.steer.Activate('arrive', location_manager['bank'].point)
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        original = owner.attributes['wealth']
        gain = owner.items['gold'].attributes['value'] * owner.items['gold'].attributes['quantity']
        owner.attributes['wealth'] += gain
        owner.items['gold'].attributes['quantity'] = 0
        
        owner.GetFSM().ReleaseGlobal()
        
class Miner_Seek_Bladder_Relief(State):
    def precondition(self, owner):
        if owner.AtLocation('bathroom'):
            owner.ArrivedAtLocation('bathroom')
            owner.Announce('Urinating')
            return True
        if not owner.steer.On('arrive'):
            owner.steer.Activate('arrive', location_manager['bathroom'].point)
        owner.Announce("Walking to bathroom.")
        return False
    
    def enter(self, owner):
        owner.ChangeLocation('outside')
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
        
    def execute(self, owner):
        owner.attributes['bladder'] -= int(random() * 8)
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
        
    def exit(self, owner):
        pass