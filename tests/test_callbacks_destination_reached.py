#!/usr/bin/env python3


import os
import lgsvl
import math
import time
import json

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 8181)
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
destination = state.position + 200* forward
dv.setup_apollo(destination.x, destination.z, modules)

#define callbacks
def reached_destination(agent):
  print(agent.name, "ego car reached destination")
  sim.stop()

ego.destination_reached(reached_destination)

input("Press Enter to run")

sim.run()