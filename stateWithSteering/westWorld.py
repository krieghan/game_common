from random import random
from time import sleep
import sys
sys.path.append('../StateMachine')
from common.Builders import ScreenCellBuilder
from Machines import *
from State import *
from BaseGameEntity import *
from WestWorldAgents import *
from WestWorldStates import *
from World import *
from Point import Point
from Vector import Vector
from StatusManager import LabelStatusManager
from WestWorldObservers import LabelObserver, LabelItemAttributeObserver
from Location import Location

from GraphicLocations import Lake, Mine, Saloon, MinerHome, Bank, Room
from Globals import agent_manager, item_manager, location_manager, state_manager, message_dispatcher, globalRegistry

class WestWorld:
    def __init__(self, canvas):
        self.world = World(self)
        self.canvas = canvas
        
        globalRegistry['world'] = self.world
        self.world.SetHCells(10)
        self.world.SetWCells(10)
        
        screenCellBuilder = ScreenCellBuilder(height=self.world.GetWorldHeight(), width=self.world.GetWorldWidth(), hcells=10, wcells=10)

        location_manager['screenCells'] = screenCellBuilder.buildScreenCells()
        
        location_manager.Add('lake', Lake(Point(200, 200), name='Westworld Lake', world=self.world))
        location_manager.Add('mine', Mine(Point(600, 600), name='Westworld Mine', world=self.world))
        location_manager.Add('saloon', Saloon(Point(200, 400), name='Westworld Saloon', world=self.world))
        location_manager.Add('miner_home', MinerHome(Point(500, 200), name="Miner's House", world=self.world))
        location_manager.Add('bank', Bank(Point(400, 800), name='Westworld Bank', world=self.world))
        location_manager.Add('bathroom', Room(Point(550, 250), name="Miner's Bathroom", world=self.world))
        location_manager.Add('kitchen', Room(Point(450, 150), name="Miner's Kitchen", world=self.world))
        location_manager.Add('miner_bedroom', Room(Point(550, 150), name="Miner's Bedroom", world=self.world))
        location_manager.Add('fisher_bedroom', Room(Point(450, 250), name="Fisherman's Bedroom", world=self.world))
        location_manager.Add('outside', Location(name='Outside', world=self.world))
        
        
        
        bob_status_manager = LabelStatusManager(action=self.canvas.parent.label_bob_status, gold=self.canvas.parent.label_bob_gold_status)
        elsa_status_manager = LabelStatusManager(action=self.canvas.parent.label_elsa_status, fish=self.canvas.parent.label_elsa_fish_status, gold=self.canvas.parent.label_elsa_gold_status)
        dan_status_manager = LabelStatusManager(action=self.canvas.parent.label_dan_status, fish=self.canvas.parent.label_dan_fish_status, gold=self.canvas.parent.label_dan_gold_status)
        
        agent_manager.Add('miner_bob', Miner(Point(*location_manager['miner_home'].point.GetXAndY()), Vector(0, 0), name='Bob', status_manager=bob_status_manager,  start_state=Miner_Global(), global_state=Miner_Global(), unconditional_global_state=Miner_UGS(), world=self.world))
        agent_manager.Add('miner_wife', Housewife(Point(*location_manager['miner_home'].point.GetXAndY()), Vector(0, 0), name='Elsa', status_manager=elsa_status_manager, start_state=Wife_Global(), global_state=Wife_Global(), unconditional_global_state=Wife_UGS(), world=self.world))
        agent_manager.Add('fisher_dan', Fisherman(Point(*location_manager['miner_home'].point.GetXAndY()), Vector(0, 0), name='Dan', status_manager=dan_status_manager, start_state=Fisherman_Global(), global_state=Fisherman_Global(), unconditional_global_state=Fisherman_UGS(), world=self.world))
        
        agent_manager['miner_bob'].wife=agent_manager['miner_wife']

        #Setup Observers to update labels on screen
        
        agent_manager['miner_bob'].status.Register('status', LabelObserver(self.canvas.parent.label_bob_status))
        agent_manager['miner_bob'].attributes.Register('wealth', LabelObserver(self.canvas.parent.label_bob_gold_status))
        
        agent_manager['miner_wife'].status.Register('status', LabelObserver(self.canvas.parent.label_elsa_status))
        agent_manager['miner_wife'].attributes.Register('wealth', LabelObserver(self.canvas.parent.label_elsa_gold_status))
        agent_manager['miner_wife'].items.Register('fish', LabelItemAttributeObserver(self.canvas.parent.label_elsa_fish_status, 'quantity'))
        
        agent_manager['fisher_dan'].status.Register('status', LabelObserver(self.canvas.parent.label_dan_status))
        agent_manager['fisher_dan'].attributes.Register('wealth', LabelObserver(self.canvas.parent.label_dan_gold_status))
        agent_manager['fisher_dan'].items.Register('fish', LabelItemAttributeObserver(self.canvas.parent.label_dan_fish_status, 'quantity'))

        state_manager.Add('miner_global_state', Miner_Global())
        state_manager.Add('miner_ugs', Miner_UGS())
        state_manager.Add('miner_mine', Miner_Mine())
        state_manager.Add('miner_drink', Miner_Saloon())
        state_manager.Add('miner_deposit', Miner_Bank())
        state_manager.Add('miner_sleep', Miner_Home_Sleep())
        state_manager.Add('miner_dinner', Miner_Home_Dinner())
        state_manager.Add('miner_eating', Miner_Home_Eating())
        state_manager.Add('miner_seek_bladder_relief', Miner_Seek_Bladder_Relief())
        
        state_manager.Add('wife_global_state', Wife_Global())
        state_manager.Add('wife_ugs', Wife_UGS())
        state_manager.Add('wife_seek_bladder_relief', Wife_Seek_Bladder_Relief())
        state_manager.Add('wife_cook_meal', Wife_Cook_Meal())
        state_manager.Add('wife_eat_stew', Wife_Eat_Stew())
        state_manager.Add('wife_drink_coffee', Wife_Drink_Coffee())
        state_manager.Add('wife_putter_about', Wife_Putter_About())
        state_manager.Add('wife_sleep', Wife_Sleep())
        
        state_manager.Add('fisherman_global_state', Fisherman_Global())
        state_manager.Add('fisherman_ugs', Fisherman_UGS())
        state_manager.Add('fisherman_fish', Fisherman_Fish())
        state_manager.Add('fisherman_drink', Fisherman_Saloon())
        state_manager.Add('fisherman_deposit', Fisherman_Deposit())
        state_manager.Add('fisherman_sleep', Fisherman_Home_Sleep())
        state_manager.Add('fisherman_dinner', Fisherman_Home_Dinner())
        state_manager.Add('fisherman_eating', Fisherman_Home_Eating())
        state_manager.Add('fisherman_seek_bladder_relief', Fisherman_Seek_Bladder_Relief())
        
        message_dispatcher = MessageDispatcher()
        
    def RunSimulationIteration(self):

        for agent in agent_manager.GetValues():
            agent.Update(self.canvas.time_elapsed)
            message_dispatcher.DispatchMessages(self.world.timestep)
            
    def Announce(self, message):
        pass
        #self.canvas.DisplayMessage(message)
        
            
if __name__ == '__main__':
   westworld = WestWorld()
   westworld.RunSimulation()
        