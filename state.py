from Behaviors import *

class State(DispatchesMessages, HasState, HasLocation, HasAgents):
       
    def enter(self, owner):
        pass
    
    def execute(self, owner):
        pass
        
    def exit(self, owner):
        pass   

class Unconditional_Global_State(State):
   def execute(self, owner):
      pass