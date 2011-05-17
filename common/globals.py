from EntityManager import EntityManager, AgentManager, ItemManager, LocationManager, StateManager
from Machines import MessageDispatcher

entity_manager = EntityManager()
agent_manager = AgentManager()
item_manager = ItemManager()
location_manager = LocationManager()
state_manager = StateManager()
message_dispatcher = MessageDispatcher()
globalRegistry = {}
