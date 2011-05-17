from zope.interface import Interface, verify

class IState(Interface):
   
    def enter(owner):
        pass
    
    def execute(owner):
        pass
    
    def exit(owner):
        pass
    
    

class StateMachine(object):
    
    def __init__(self,
                 owner,
                 currentState,
                 globalState=None):
        
        self.owner = owner
        self.currentState = currentState
        self.globalState = globalState
        
    def start(self):
        if self.currentState:
            self.currentState.enter(self.owner)
        
    
    def changeState(self,
                    newState):
        verify.verifyClass(IState, newState)
        if self.currentState:
            self.currentState.exit(self.owner)
        newState.enter(self.owner)        
        self.currentState = newState
        
    def update(self):
        globalState = self.globalState
        if globalState:
            globalState.execute(self.owner)
        if self.currentState:
            self.currentState.execute(self.owner)
        