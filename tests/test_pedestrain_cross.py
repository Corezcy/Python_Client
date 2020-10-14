#!/usr/bin/env python3
#
# Copyright (c) 2019 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import os
import lgsvl
import math
import time


# class Test_BorrageAVe_pedestrain_cross(unittest.TestCase):
#   def test_ego_follow_npc_collision(self): 
#     with SimConnection(seconds=100, scene="BorregasAve", error_message=None, load_scene=True) as sim:
      
#       ego = self.setup_ego(sim, "Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO,"10.78.4.163", 'Borregas Ave')
#       npc1,waypoints = self.setup_npc1(sim,"Sedan", lgsvl.AgentType.NPC)
#       collisions = []
#       def on_collision(agent1, agent2, contact):
#         collisions.append([agent1, agent2, contact])
#         sim.stop()
#       ego.on_collision(on_collision)
#       npc1.on_collision(on_collision)
#       npc1.follow(waypoints)
#       sim.run()
#       self.assertGreater(len(collisions), 0)
#       self.assertInBetween(collisions[0][2], collisions[0][0].state.position, collisions[0][1].state.position, "Ego Collision")
#       self.assertTrue(collisions[0][0].name == "Lincoln2017MKZ (Apollo 5.0)" or collisions[0][1].name == "Lincoln2017MKZ (Apollo 5.0)")
#       self.assertTrue(True)


#   #define ego car and connect apollo
#   def setup_ego(self, sim, ego_name, agent_type,BRIDGE_HOST,HDmap_name): 
#     spawns = sim.get_spawn()
#     state = lgsvl.AgentState()
#     state.transform = spawns[0]
#     forward = lgsvl.utils.transform_to_forward(spawns[0])
#     right = lgsvl.utils.transform_to_right(spawns[0])
#     ego = sim.add_agent(ego_name, agent_type, state)
#     print(sim.get_agents())
#     ego.connect_bridge(BRIDGE_HOST, 9090)
#     dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
#     dv.set_hd_map(HDmap_name)
#     dv.set_vehicle('Lincoln2017MKZ LGSVL')
#     modules = []
#     modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
#     destination = state.position + 200* forward
#     dv.setup_apollo(destination.x, destination.z, modules)
#     return ego
  
#   #define npc car
#   # NPC, 10 meters ahead
#   def setup_npc1(self,sim,npc1_name,agent_type):
#     spawns = sim.get_spawn()
#     state = lgsvl.AgentState()
#     forward = lgsvl.utils.transform_to_forward(spawns[0])
#     right = lgsvl.utils.transform_to_right(spawns[0])
#     state.transform.position = spawns[0].position + 10 * forward
#     state.transform.rotation = spawns[0].rotation
#     npc1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)






sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 9194)
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "10.78.4.163")

if sim.current_scene == "BorregasAve":
  sim.reset()
else:
  sim.load("BorregasAve")

layer_mask = 0
layer_mask |= 1 << 0 

#ego define
spawns = sim.get_spawn()
state = lgsvl.AgentState()
state.transform = spawns[0]
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])
ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
print(sim.get_agents())

ego.connect_bridge(BRIDGE_HOST, 9090)

dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
dv.set_hd_map('Borregas Ave')
dv.set_vehicle('Lincoln2017MKZ LGSVL')
modules = []
modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
destination = state.position + 50* forward
dv.setup_apollo(destination.x, destination.z, modules)

#pedestrian define

radius = 4
count = 20
wp = []
for i in range(count):
  #x = radius * math.cos(i * 2 * math.pi / count)
  #z = radius * math.sin(i * 2 * math.pi / count)
  # idle is how much time the pedestrian will wait once it reaches the waypoint
  idle = 1 if i < count//2 else 0
  #wp.append(lgsvl.WalkWaypoint(spawns[0].position + (2 + x) * right + z * forward, idle))
  wp.append(lgsvl.WalkWaypoint(spawns[0].position + (4 - i) * right + 20 * forward, 0,10))

state = lgsvl.AgentState()
state.transform = spawns[1]
state.transform.position = wp[0].position

p = sim.add_agent("Pamela", lgsvl.AgentType.PEDESTRIAN, state)

def on_waypoint(agent, index):
  print("Waypoint {} reached".format(index))

p.on_waypoint_reached(on_waypoint)

# This sends the list of waypoints to the pedestrian. The bool controls whether or not the pedestrian will continue walking (default false)
#p.follow(wp, True)

input("Press Enter to run")

sim.run()

