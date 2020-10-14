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

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 8181)
BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "10.78.4.163")
for i in range(100):

  if sim.current_scene == "BorregasAve":
    sim.reset()
  else:
    sim.load("BorregasAve")

  spawns = sim.get_spawn()

  state = lgsvl.AgentState()
  state.transform = spawns[0]
  print(state)

  forward = lgsvl.utils.transform_to_forward(spawns[0])

 
  #state.velocity = 20 * forward
  a = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
  ego_state = lgsvl.Agent(a.uid,sim)
  ego_state_now = ego_state.state
  print(ego_state)

#connect with apollo dreamview
  a.connect_bridge(BRIDGE_HOST, 9090)

  dv = lgsvl.dreamview.Connection(sim, a, BRIDGE_HOST)
  dv.set_hd_map('Borregas Ave')
  dv.set_vehicle('Lincoln2017MKZ LGSVL')
  modules = []
  modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
  destination = state.position + 200*forward
  print(destination)
  dv.setup_apollo(destination.x, destination.z, modules)

  
 
#define callbacks 
  
  def on_stop_point(agent):
    print(agent.name, "reached stop line at",sim.current_time)

  stop_point = state.position +190*forward
  print(stop_point)
  delt = stop_point.x - ego_state_now.position.x
  while True:
    sim.run(1)
    ego_state = lgsvl.Agent(a.uid,sim)
    ego_state_now = ego_state.state
    delt = stop_point.x - ego_state_now.position.x
    #print(ego_state)
    if delt <10:
      break

  sim.stop()

  print("run number:",i)





