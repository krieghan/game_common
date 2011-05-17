import math
import random
import numpy
import sys

from zope.interface import implements, verify

from ai import interfaces

from twodee.geometry import (vector,
                         calculate,
                         convert)
import wander, avoidobstacles, avoidwalls, seek, flee, arrive, pursue, evade, interpose, hide, followpath, pursueoffset, align, cohere, separate, flock

class SteeringController:
    
    def __init__(self, 
                 agent):
        
        verify.verifyObject(interfaces.Steerable, agent)
        
        self.agent = agent
        self.force_reservoir = agent.getMaxForce()
                
        #Wander Behavior
        self.wanderRadius = 20
        self.wanderDistance = 30
        self.wanderJitter = .03
        self.centerToWanderTarget = (0, 0)
        
        #Evasion behaviors
        self.evadeDistanceSquared = None
        
        #Arrive Behavior
        self.decelerationFactor = .9

        #FollowPath Behavior
        self.path = None
        self.waypointSquaredDistance = 100000
        
        self.steeringFunctions = {'seek' : seek.seek,
                                  'flee' : flee.flee,
                                  'arrive' : arrive.arrive,
                                  'pursue' : pursue.pursue,
                                  'wander' : wander.wander,
                                  'evade' : evade.evade,
                                  'avoidobstacles' : avoidobstacles.avoidobstacles,
                                  'avoidwalls' : avoidwalls.avoidwalls,
                                  'interpose' : interpose.interpose,
                                  'hide' : hide.hide,
                                  'followpath' : followpath.followpath,
                                  'pursueoffset' : pursueoffset.pursueoffset,
                                  'separate' : separate.separate,
                                  'alignment' : align.align,
                                  'cohesion' : cohere.cohere,
                                  'flock' : flock.flock}
        
        self.weight = {'seek' : 3,
                       'flee' : 3,
                       'arrive' : 3,
                       'pursue' : 1,
                       'evade' : 3,
                       'wander' : 1,
                       'avoidobstacles' : 10,
                       'avoidwalls' : 10,
                       'interpose' : 3,
                       'hide' : 3,
                       'followpath' : 3,
                       'pursueoffset' : 3,
                       'separate' : 3,
                       'alignment' : 3,
                       'cohesion' : 3,
                       'flock' : 3}
        
        #Steering keywords key into a list of tuples.  Each tuple represents the set of 
        #arguments into one behavior.  If there is more than one tuple in the list,
        #it means that more than one of that type of behavior is being executed.
        self.actions = {'avoidwalls' : None,
                        'avoidobstacles' : None,
                        'hide' : None,
                        'interpose' : None,
                        'evade' : None,
                        'pursue' : None,
                        'flee' : None,
                        'seek' : None,
                        'arrive' : None,
                        'followpath' : None,
                        'pursueoffset' : None,
                        'separate' : None,
                        'alignment' : None,
                        'cohesion' : None,
                        'flock' : None,
                        'wander' : None}
        
        self.keywords = ['avoidwalls', 
                         'avoidobstacles',
                         'evade',
                         'flee', 
                         'hide', 
                         'interpose', 
                         'pursue',
                         'seek', 
                         'arrive', 
                         'followpath', 
                         'pursueoffset', 
                         'separate', 
                         'alignment', 
                         'cohesion', 
                         'flock',
                         'wander']
        
    
    def activate(self, 
                 actionkey, 
                 *arguments):
        self.actions[actionkey] = arguments
    
    def deactivate(self, actionkey):
        self.actions[actionkey] = None
    
    def isActive(self,
                 actionkey):
        return bool(self.actions[actionkey])
    
    def getTarget(self):
        pursueArguments = self.actions['pursue']
        if pursueArguments is not None:
            return pursueArguments[0]
        
    
    def getAgent(self):
        return self.agent
    
    def plotPath(self, 
                 points,
                 closed):
        self.path = followpath.Path(points=points,
                                    closed=closed)
    
    def getPath(self):
        return self.path

    
    def calculate(self):
        return self.prioritizedRunningSum()
    
    def weightedTruncatedSum(self):
        force = (0, 0)
        action_list = self.action_list
        for behavior in self.keyword_list:
            if self.on(behavior):
                forceForBehavior = calculate.multiplyVectorAndScalar(action_list[behavior].getWeight(),
                                                                     action_list[behavior].executeFunction())
                force = calculate.addVectors(force,
                                             forceForBehavior)

        force = vector.truncate(force,
                                self.parent_agent.getMaxForce())
        return force
        
    def prioritizedRunningSum(self):
        force = (0, 0)
       
        remaining_reservoir = self.force_reservoir
        
        for behaviorKeyword in self.keywords:
            action = self.actions[behaviorKeyword]
            if action is None:
                continue
            arguments = (self.agent,) + action
            behaviorFunction = self.steeringFunctions[behaviorKeyword]
            weight = self.weight[behaviorKeyword]
            forceForBehavior = calculate.multiplyVectorAndScalar(behaviorFunction(*arguments),
                                                                 weight)
            forceForBehavior = vector.truncate(forceForBehavior,
                                               remaining_reservoir)
           
            magnitudeForBehaviorForce = vector.getMagnitude(forceForBehavior)

            remaining_reservoir -= magnitudeForBehaviorForce
            force = calculate.addVectors(force,
                                         forceForBehavior)
            if remaining_reservoir <= 0:   
                break 
        
        force = vector.truncate(force,
                                self.agent.getMaxForce())
        return force
        
    
    def prioritizedDithering(self):
        raise Exception("Prioritized Dithering Not Implemented")


    
