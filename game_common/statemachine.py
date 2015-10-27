from zope.interface import Interface, verify

class IState(Interface):
   
    def enter(owner):
        pass
    
    def execute(owner):
        pass
    
    def exit(owner):
        pass

class StateChangeFailed(Exception):
    pass

class StateMachine(object):
    
    def __init__(self,
                 owner,
                 currentState,
                 globalState=None,
                 name=None):
        
        self.owner = owner
        self.currentState = currentState
        self.globalState = globalState
        self.name = name
        
    def start(self):
        if self.currentState:
            self.currentState.enter(self.owner)
        
    
    def changeState(self,
                    newState):
        verify.verifyClass(IState, newState)
        if self.currentState:
            try:
                self.currentState.exit(self.owner)
            except StateChangeFailed:
                for observer in self.owner.getObservers():
                    observer.notifyStateChangeFailed(self)
            else:
                try:
                    newState.enter(self.owner)        
                except StateChangeFailed:
                    for observer in self.owner.getObservers():
                        observer.notifyStateChangeFailed(self)
                else:
                    self.currentState = newState
                    for observer in self.owner.getObservers():
                        observer.notifyStateChange(self)
        
    def update(self):
        globalState = self.globalState
        if globalState:
            globalState.execute(self.owner)
        if self.currentState:
            self.currentState.execute(self.owner)
        
