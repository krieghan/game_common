
class State:
          
    def enter(self, owner):
        pass

    def precondition(self, owner):
        return True
    
    def execute(self, owner):
        pass
        
    def exit(self, owner):
        pass   

class Unconditional_Global_State(State):
   def execute(self, owner):
      pass