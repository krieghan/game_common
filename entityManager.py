class EntityManager:
   def __init__(self, owner=None):
      self.owner = owner
      self.container = {}
      
   def __getitem__(self, name):
      return self.container[name]
        
   def __setitem__(self, name, value):
      self.container[name] = value
      
   def __delitem__(self, name):
      del self.container[name]
   
   def __add__(self, othermanager):
      return list(othermanager.container.values()) + list(self.container.values())
    
   def GetOwner(self):
      return self.owner
    
   def GetType(self):
      pass
    
   def GetValues(self):
      return self.container.values()
   
   def GetKeys(self):
      return self.container.keys()
   def HasKey(self, element):
      return self.container.has_key(element)
      
      
class ItemManager(EntityManager):
    def GetType(self):
        return type(ItemManager())
       
    def __setitem__(self, itemname, value):
        if self.container.has_key(itemname):
            self.container[itemname].attributes['quantity'] += value.attribute['quantity']
        else:
            self.container[itemname] = value
        if 'attributes' in dir(self.owner):
            self.owner.attributes['encumberance'] += value.quantity * value.weight
    
class AttributeManager(EntityManager):
    def GetType(self):
        return type(AttributeManager())

class AgentManager(EntityManager):
    def GetType(self):
        return type(AgentManager())
        
class LocationManager(EntityManager):
    def GetType(self):
        return type(self)   
   
class StateManager(EntityManager):
   def GetType(self):
      return type(self)        