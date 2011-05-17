from State import *
from random import random
from BaseGameEntity import *
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher


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
        owner.Announce("Going to work.  Hope I get some gold")
        owner.ChangeLocation('mine')
        
    def execute(self, owner):
        owner.Announce("Mining for Gold")
        owner.items['gold'].AddQuantity(int(random() * 2))
        
        if owner.HasEnoughGold():
            
            owner.GetFSM().ChangeState(state_manager['miner_deposit'])
        
    def exit(self, owner):
        owner.Announce("Leaving the mine with my pockets full of gold")

class Miner_Home_Dinner(State):
    def enter(self, owner):
        owner.Announce("Home sweet home.  Time for dinner.")
        owner.ChangeLocation('miner_home')
        message_dispatcher.ScheduleMessage(Message(owner, owner.wife, 'imhome', 0, None, world=owner.world))
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce("Man I'm hungry.  When's that stew gonna get done?")
    
class Miner_Home_Eating(State):
    def enter(self, owner):
        owner.Announce("Gotta love a good home-cooked meal")
        owner.ChangeLocation('miner_home')
                
    def execute(self, owner):
        owner.Announce("*Munch* *Chew* *Gulp*")
        owner.attributes['hunger'] -= int(random() * 8)
        owner.attributes['thirst'] -= int(random() * 8)
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()
        
    
class Miner_Home_Sleep(State):
    def enter(self, owner):
        owner.Announce("I'm going to bed.")
        owner.ChangeLocation('miner_home')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce("ZZZZZZZZZZZ")
        owner.attributes['fatigue'] -= int(random() * 8)
        if owner.IsFatigueSatisfied():
            owner.GetFSM().ReleaseGlobal()
    
    
class Miner_Saloon(State):
    def enter(self, owner):
        owner.Announce('Going to the saloon.  I really need a drink')
        owner.ChangeLocation('saloon')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce('Gulp')
        owner.attributes['thirst'] -= int(random() * 8)
        owner.attributes['bladder'] += int(random() * 4)
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()

class Miner_Bank(State):
    def enter(self, owner):
        owner.Announce('Depositing my earnings')
        owner.ChangeLocation('bank')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        original = owner.attributes['wealth']
        gain = owner.items['gold'].attributes['value'] * owner.items['gold'].attributes['quantity']
        owner.attributes['wealth'] += gain
        owner.Announce('Original wealth was $%d.  %d units of gold at $%d each deposited for wealth gain of $%d.  Current wealth is now $%d' % (original, owner.items['gold'].attributes['quantity'], owner.items['gold'].attributes['value'], gain, owner.attributes['wealth']))
        
        owner.items['gold'].attributes['quantity'] = 0
        
        owner.GetFSM().ReleaseGlobal()
        
class Miner_Seek_Bladder_Relief(State):
    def enter(self, owner):
        owner.Announce("Time to visit the little boy's room")
        owner.ChangeLocation('miner_home')
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
        
    def execute(self, owner):
        owner.attributes['bladder'] -= int(random() * 8)
        owner.Announce('All that drinking is getting to me')
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
        
    def exit(self, owner):
        owner.Announce('I feel a lot better')