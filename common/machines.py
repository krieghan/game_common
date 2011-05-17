class MessageDispatcher:
    def __init__(self):
        self.__class__.schedule = []
    
    def __add__(self, message):
        self.ScheduleMessage(message)
        
    def GetSchedule(self):
        return self.__class__.schedule
        
    def SetSchedule(self, newschedule):
        self.__class__.schedule = newschedule
    
    def ScheduleMessage(self, message):
        if len(self.GetSchedule()) == 0 or message.dispatchTime > self.GetSchedule()[-1].dispatchTime:
            self.__class__.schedule.append(message)
            return True
        for index in range(len(self.GetSchedule())):
            if message.dispatchTime < self.GetSchedule()[index].dispatchTime:
                self.__class__.schedule.insert(index, message)
                return True

        self.__class__.schedule.append(message)
    
    def DispatchMessages(self, time):
        while(True):
            if len(self.GetSchedule()) < 1:
                return
            firstElement = self.GetSchedule()[0]
            if firstElement.GetDispatchTime() <= time:
                self.schedule.remove(firstElement)
                if type(firstElement.destination) != list:
                    firstElement.destination.HandleMessage(firstElement)
                else:
                    for dest in firstElement.destination:
                        dest.HandleMessage(firstElement)
                
            else:
                return
    
    

         
class StateMachine:
    def __init__(self, owner=None, currentState=None, globalState=None, unconditional_global_state=None):
        self.owner = owner
        self.currentState = currentState
        self.previousState = None
        self.globalState = globalState
        self.unconditional_global_state = unconditional_global_state
        self.executing_global = 1
    
    def LockGlobal(self):
        self.executing_global = 0
    
    def ReleaseGlobal(self):
        self.executing_global = 1
    
    def update(self):
        if self.currentState.precondition(self.owner):
            self.currentState.execute(self.owner)
            
        self.unconditional_global_state.execute(self.owner)
        if self.executing_global:
            self.globalState.execute(self.owner)
        
        
    def ChangeState(self, newState):
        if newState == self.currentState:
            return False
        self.currentState.exit(self.owner)
        self.currentState = newState
        self.currentState.enter(self.owner)
        return self.currentState
    
    def SetGlobalState(self, globalstate):
        self.globalState = globalstate              