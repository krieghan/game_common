from State import *
from random import random
from BaseGameEntity import *

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
    def enter(self, owner):
        owner.Announce('Wow.  Think I drank a bit too much coffee')
        owner.ChangeLocation('miner_home')
        owner.GetFSM().LockGlobal()
        owner.LockInteraction()
    
    def execute(self, owner):
        owner.attributes['bladder'] -= int(random() * 8)
        owner.Announce(' Dribble Drabble ')
        if owner.IsBladderSatisfied():
            owner.GetFSM().ReleaseGlobal()
            owner.ReleaseInteraction()
        
    def exit(self, owner):
        owner.Announce('Whew.  That feels better')
    
class Wife_Drink_Coffee(State):
    def enter(self, owner):
        owner.Announce('Sure am thirsty.  Some coffee will quench my thirst.')
        owner.ChangeLocation('miner_home')
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        owner.Announce('** Gulp **')
        owner.attributes['thirst'] -= int(random() * 8)
        if owner.IsThirstSatisfied():
            owner.GetFSM().ReleaseGlobal()

    def exit(self, owner):
        owner.Announce('Mmmmmm, good coffee')
            
class Wife_Putter_About(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce("Well, as long as I'm not doing anything else...")
    
    def execute(self, owner):
        owner.Announce('Reading a magazine')
        
    def exit(self, owner):
        owner.Announce('That was a good read, but time to get to something else')
        
class Wife_Cook_Meal(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce('Putting the stew in the oven')
        message_dispatcher.ScheduleMessage(Message(owner, owner, 'stewdone', 15, None, owner.world))
        self.cooking_now = 1
        owner.GetFSM().LockGlobal()

class Wife_Eat_Stew(State):
    def enter(self, owner):
        owner.ChangeLocation('miner_home')
        owner.Announce('My, my, that stew sure is hot!')
        message_dispatcher.ScheduleMessage(Message(owner, owner.location, 'stewdone', 0, None, owner.world))
        owner.GetFSM().LockGlobal()
    
    def execute(self, owner):
        if owner.IsHungerSatisfied():
            owner.GetFSM().ReleaseGlobal()
        else:
            owner.Announce('That stew sure is tasty :)')
            owner.attributes['hunger'] -= int(random() * 8)
            owner.attributes['thirst'] -= int(random() * 8)
            
class Wife_Sleep(State):
    def enter(self, owner):
        owner.Announce('Sure am tired.  Time to get some sleep')
        owner.ChangeLocation('miner_home')
        owner.GetFSM().LockGlobal()
        
    def execute(self, owner):
        owner.Announce('ZZZZZZZZZZZ')
        owner.attributes['fatigue'] -= int(random() * 8)
        
        if owner.IsFatigueSatisfied():
            owner.GetFSM().ReleaseGlobal()
            