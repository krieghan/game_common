

class EntityManager:
    def __init__(self, owner=None):
        self.owner = owner
        self.container = {}
        self.observers = {}
      
    def __getitem__(self, name):
        return self.container[name]
        
    def __setitem__(self, key, value):
        self.container[key] = value
        self.NotifyObservers(key, value)
        
      
    def __delitem__(self, name):
        del self.container[name]
   
    def __add__(self, othermanager):
        return list(othermanager.container.values()) + list(self.container.values())
    
    def update(self, **kwds):
        self.container.update(**kwds)
    
    def GetOwner(self):
        return self.owner
    
    def GetType(self):
        return type(self)
    
    def GetValues(self):
        return self.container.values()
   
    def GetKeys(self):
        return self.container.keys()
      
    def HasKey(self, element):
        return self.container.has_key(element)
    
      
    def Register(self, key, observer):
        if not self.observers.has_key(key):
            self.observers[key] = [observer]
        else:
            self.observers[key].append(observer)
   
    def NotifyObservers(self, key, value):
        if self.observers.has_key(key):
            for observer in self.observers[key]:
                observer.update(value=value)
      
    def Add(self, key, entity=None):
        entity.key = key
        self[key] = entity
        
        
        
class ItemManager(EntityManager):
    def GetType(self):
        return type(ItemManager())
       
    def __setitem__(self, key, value):
        if self.container.has_key(key):
            self.container[key].attributes['quantity'] += value.attribute['quantity']
        else:
            self.container[key] = value
        self.NotifyObservers(key, self.container[key])
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
  
class StatusManager(EntityManager):
    def GetType(self):
        return type(self)