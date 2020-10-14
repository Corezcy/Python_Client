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

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 8083)
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
state.transform = spawns[1]
forward = lgsvl.utils.transform_to_forward(spawns[1])
right = lgsvl.utils.transform_to_right(spawns[1])
ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
print(sim.get_agents())

ego.connect_bridge(BRIDGE_HOST, 9090)

dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
dv.set_hd_map('Borregas Ave')
dv.set_vehicle('Lincoln2017MKZ LGSVL')
modules = []
modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
destination = state.position + 200* forward
dv.setup_apollo(destination.x, destination.z, modules)

#npc define
spawns = sim.get_spawn()
state = lgsvl.AgentState()
state.transform = spawns[1]

state.transform.position += 5*forward
state.transform.position -= 3.5*right

npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

npc.follow_closest_lane(True, 11.1)
hit = sim.raycast(state.position+forward*70, lgsvl.Vector(0,-1,0), layer_mask) 
wp = lgsvl.DriveWaypoint(hit.point, speed, angle, 1)
waypoints.append(wp)


npc.change_lane(True)

  
 #define callbacks 
  
vehicles = {
  ego: "EGO",
  npc: "Sedan",
}

# Executed upon receiving collision callback -- NPC is expected to drive through colliding objects
def on_collision(agent1, agent2, contact):
  name1 = vehicles[agent1]
  name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
  print("{} collided with {}".format(name1, name2))

ego.on_collision(on_collision)
npc.on_collision(on_collision)
npc.on_waypoint_reached(npc.change_lane(True))
input("Press Enter to run")

sim.run()

