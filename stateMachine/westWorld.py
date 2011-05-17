from random import random
from time import sleep
import sys

from EntityManager import *
from Machines import *
from State import *
from BaseGameEntity import *
from WestWorldAgents import *
from WestWorldStates import *
from World import *
from Globals import (agent_manager, 
                     item_manager, 
                     location_manager, 
                     state_manager, 
                     message_dispatcher)


class WestWorld:
    def __init__(self):
        self.world = World(self)
        
        location_manager['miner_home'] = Location("Miner Bob's Home", world=self.world)
        location_manager['bank'] = Location("First Westworld Bank", world=self.world)
        location_manager['saloon'] = Location("Benny's Saloon", world=self.world)
        location_manager['mine'] = Location("Westworld Mine", world=self.world)
        location_manager['lake'] = Location("Westworld Lake", world=self.world)
        
        
        agent_manager['miner_bob'] = Miner(name='Bob', start_state=Miner_Global(), global_state=Miner_Global(), unconditional_global_state=Miner_UGS(), world=self.world)
        agent_manager['miner_wife'] = Housewife(name='Elsa', start_state=Wife_Global(), global_state=Wife_Global(), unconditional_global_state=Wife_UGS(), world=self.world)
        agent_manager['fisher_dan'] = Fisherman(name='Dan', start_state=Fisherman_Global(), global_state=Fisherman_Global(), unconditional_global_state=Fisherman_UGS(), world=self.world)
        agent_manager['miner_bob'].wife=agent_manager['miner_wife']
        
        
        state_manager['miner_global_state'] = Miner_Global()
        state_manager['miner_ugs'] = Miner_UGS()
        state_manager['miner_mine'] = Miner_Mine()
        state_manager['miner_drink'] = Miner_Saloon()
        state_manager['miner_deposit'] = Miner_Bank()
        state_manager['miner_sleep'] = Miner_Home_Sleep()
        state_manager['miner_dinner'] = Miner_Home_Dinner()
        state_manager['miner_eating'] = Miner_Home_Eating()
        state_manager['miner_seek_bladder_relief'] = Miner_Seek_Bladder_Relief()
        
        state_manager['wife_global_state'] = Wife_Global()
        state_manager['wife_ugs'] = Wife_UGS()
        state_manager['wife_seek_bladder_relief'] = Wife_Seek_Bladder_Relief()
        state_manager['wife_cook_meal'] = Wife_Cook_Meal()
        state_manager['wife_eat_stew'] = Wife_Eat_Stew()
        state_manager['wife_drink_coffee'] = Wife_Drink_Coffee()
        state_manager['wife_putter_about'] = Wife_Putter_About()
        state_manager['wife_sleep'] = Wife_Sleep()
        
        state_manager['fisherman_global_state'] = Fisherman_Global()
        state_manager['fisherman_ugs'] = Fisherman_UGS()
        state_manager['fisherman_fish'] = Fisherman_Fish()
        state_manager['fisherman_drink'] = Fisherman_Saloon()
        state_manager['fisherman_deposit'] = Fisherman_Deposit()
        state_manager['fisherman_sleep'] = Fisherman_Home_Sleep()
        state_manager['fisherman_dinner'] = Fisherman_Home_Dinner()
        state_manager['fisherman_eating'] = Fisherman_Home_Eating()
        state_manager['fisherman_seek_bladder_relief'] = Fisherman_Seek_Bladder_Relief()
        
        message_dispatcher = MessageDispatcher()
        
    def RunSimulation(self):
        while(1):
            self.world.timestep += 1
            for agent in agent_manager.GetValues():
                agent.update()
                message_dispatcher.DispatchMessages(self.world.timestep)
            #sleep(1)
            
    def Announce(self, message):
        print message
        
            
if __name__ == '__main__':
   westworld = WestWorld()
   westworld.RunSimulation()
        