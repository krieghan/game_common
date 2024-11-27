from zope.interface import Interface, verify

from . import interfaces

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
                 current_state=None,
                 global_state=None,
                 name=None):
        verify.verifyObject(
            interfaces.Observable,
            owner)
        self.owner = owner
        self.name = name
        self.current_state = current_state
        self.global_state = global_state
        
    def start(self):
        if self.current_state:
            self.current_state.enter(self.owner)
        
    def change_state(self,
                    newState):
        verify.verifyClass(IState, newState)
        try:
            if self.current_state:
                self.current_state.exit(self.owner)
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
                self.current_state = newState
                for observer in self.owner.getObservers():
                    observer.notifyStateChange(self)
        
    def update(self):
        global_state = self.global_state
        if global_state:
            global_state.execute(self.owner)
        if self.current_state:
            self.current_state.execute(self.owner)
        
