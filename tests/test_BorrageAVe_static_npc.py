#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import unittest

import os
import lgsvl
import math
from .common import SimConnection,spawnState
import time

class Test_BorregasAve_1npc_egofollownpc(unittest.TestCase):
    def test_consistency(self): 
        for i in range(100):
            with SimConnection(seconds=100, scene="BorregasAve", error_message=None, load_scene=True) as sim:
                npc1 = self.setup_npc1(sim)
                a,destination = self.setup_ego(sim)
                collisions = []
                def collision(agent1, agent2, contact):
                    collisions.append([agent1, agent2, contact])
                    sim.stop()
                a.on_collision(collision)
                npc1.on_collision(collision)
                while True:
                    sim.run(1)
                    ego_state = lgsvl.Agent(a.uid,sim)
                    ego_state_now = ego_state.state
                    delt = destination.x - ego_state_now.position.x
                    #print(ego_state)
                    if delt <5:
                        time.sleep(3)
                        break
                ego_state_end = lgsvl.Agent(a.uid,sim)
                ego_end_position = ego_state_end.state.position
                delt_forward = destination.x - ego_end_position.x
                delt_right = destination.z - ego_end_position.z
                print(delt_forward,delt_right)
                #sim.remote.finish()
                sim.stop()
                
                #self.assertGreater(len(collisions), 0)
                #self.assertInBetween(collisions[0][2], collisions[0][0].state.position, collisions[0][1].state.position, "Ego Collision")
                #self.assertTrue(collisions[0][0].name == "Lincoln2017MKZ (Apollo 5.0)" or collisions[0][1].name == "Lincoln2017MKZ (Apollo 5.0)")
                #self.assertTrue(True)


  #define ego car and connect apollo
    def setup_ego(self, sim): 
        spawns = sim.get_spawn()
        state = lgsvl.AgentState()
        state.transform = spawns[0]
        forward = lgsvl.utils.transform_to_forward(spawns[0])
        right = lgsvl.utils.transform_to_right(spawns[0])
        state.transform.position = spawns[0].position
        ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
        print(sim.get_agents())
        ego.connect_bridge("10.78.4.163", 9090)
        dv = lgsvl.dreamview.Connection(sim, ego, "10.78.4.163")
        dv.set_hd_map('Borregas Ave')
        dv.set_vehicle('Lincoln2017MKZ LGSVL')
        modules = []
        modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
        destination = state.position + 200* forward
        dv.setup_apollo(destination.x, destination.z, modules)

        return ego,destination
  
  #define npc car
  # NPC, 10 meters ahead
    def setup_npc1(self,sim):
        spawns = sim.get_spawn()
        state = lgsvl.AgentState()
        forward = lgsvl.utils.transform_to_forward(spawns[0])
        right = lgsvl.utils.transform_to_right(spawns[0])
        state.transform.position = spawns[0].position + 100 * forward
        state.transform.rotation = spawns[0].rotation
        npc1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC,state)

        return npc1
