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
    def enter(self, owner):
        owner.ChangeLocation('lake')
        owner.Announce('Heading down to the lake with my fishing pole')
        
    def execute(self, owner):
        quantity = int(random() * 4)
        if quantity <= 2:
            owner.Announce('I must have scared them off')
        else:
            owner.Announce("Wow.  They're really biting")
        owner.items['fish'].AddQuantity(quantity)
        
        
        
    def exit(self, owner):
        owner.Announce("Putting down my fishing pole and tackle box")
        
class Fisherman_Deposit(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce('Caught as much fish as I can carry.  Off to give them to mom')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce('Looking for Mom so I can give her these fish')
        message_dispatcher.ScheduleMessage(Message(owner, agent_manager['miner_wife'], 'givefish', 0, owner.items['fish'].attributes['quantity'], owner.world))

    def exit(self, owner):
        owner.GetFSM().ReleaseGlobal()
        owner.Announce('Sure feel better after giving those fish to Mom')

class Fisherman_Saloon(State):
    def enter(self, owner):
        owner.ChangeLocation('saloon')
        owner.Announce('Fishing is thirsty work')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce('Down the hatch')
        owner.attributes['thirst'] -= int(random() * 6)
        owner.attributes['bladder'] += int(random() * 4)
        
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()
            
class Fisherman_Home_Dinner(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce('Mom.  Make me some dinner')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce('This is taking too long')
        
class Fisherman_Home_Eating(State):
    def enter(self, owner):
        owner.Announce('Mmmmmmm.  That smells really good')
        owner.ChangeLocation('miner_home')
        
    def execute(self, owner):
        owner.Announce('Hungrier than I thought')
        owner.attributes['hunger'] -= int(random() * 6)
        owner.attributes['thirst'] -= int(random() * 6)
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()
        
class Fisherman_Home_Sleep(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce('Been a busy day.  Time to get some shut-eye')
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        owner.Announce('ZZZZZZZZ')
        owner.attributes['fatigue'] -= int(random() * 8)
        if owner.IsFatigueSatisfied():
            owner.GetFSM().ReleaseGlobal()
            
    def exit(self, owner):
        owner.Announce('*Stretch*.  Time to greet the day')
    
class Fisherman_Seek_Bladder_Relief(State):
    def enter(self, owner):
        owner.ChangeLocation('lake')
        owner.Announce("All this water has strange effects on a man's body")
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
        
    def execute(self, owner):
        owner.Announce('I take the fish out and give water back')
        owner.attributes['bladder'] -= int(random() * 8)
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
            
    def exit(self, owner):
        owner.Announce('That feels better')
        
        