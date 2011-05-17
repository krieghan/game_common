from EntityManager import *
from Machines import *

class DispatchesMessages:
   message_dispatcher = MessageDispatcher()
   
   def GetDispatcher(self):
      return self.__class__.message_dispatcher
      
   def ScheduleMessage(self, message):
      return self.__class__.message_dispatcher.ScheduleMessage(message)

     
class HasAgents:
   agent_manager = AgentManager()   
   
class HasState:
   state_manager = StateManager()
   
class HasLocation:
   location_manager = LocationManager()
   
   location = None
   
   def GetLocationManager(self):
      return self.__class__.location_manager
   
   def ChangeLocation(self, new_location):
      if type(new_location) == str:
         new_location = self.location_manager[new_location]

      if self.location_manager.HasKey(self.name):
         self.location.popitem(self.name)
         
      self.location = new_location
      self.location[self.name] = self

      #self.location_manager[self.location.name][self.name] = self   