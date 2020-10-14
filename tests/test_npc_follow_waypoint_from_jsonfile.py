#!/usr/bin/env python3


import os
import lgsvl
import math
import time
import json

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 9193)
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

#npc define
state = lgsvl.AgentState()
state.transform.position = spawns[0].position + 10 * forward
state.transform.rotation = spawns[0].rotation
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

with open('/home/sunjianlei/sunjianlei/Pythonapi-new/test.json','r',encoding='utf8') as waypointsdata:
    waypoints_data = json.load(waypointsdata)
    waypoints = waypoints_data["agents"][1]["waypoints"]
    #print('json data of waypoints for agent 1 in file:',waypoints)

input("Press Enter to run")

npc.follow_waypoints_jsonfile(waypoints)   #creat function follow_waypoints_jsonfile in class NpcVehicle

#define callbacks
ego_state = lgsvl.Agent(ego.uid,sim)
ego_state_now = ego_state.state
stop_point = state.position +190*forward
print(stop_point)
delt = stop_point.x - ego_state_now.position.x
while True:
    sim.run(0.1)
    ego_state = lgsvl.Agent(ego.uid,sim)
    ego_state_now = ego_state.state
    delt = stop_point.x - ego_state_now.position.x
    #print(ego_state)
    if delt <10:
        time.sleep(5)
        break

sim.stop()