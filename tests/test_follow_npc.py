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

class Test_BorregasAve_1npc_egofollownpc(unittest.TestCase):
  def test_ego_follow_npc_collision(self): 
    with SimConnection(seconds=100, scene="BorregasAve", error_message=None, load_scene=True) as sim:
      npc1,waypoints = self.setup_npc1(sim,"Sedan", lgsvl.AgentType.NPC)
      ego = self.setup_ego(sim, "Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO,"10.78.4.163", 'Borregas Ave')
      collisions = []
      def on_collision(agent1, agent2, contact):
        collisions.append([agent1, agent2, contact])
        sim.stop()
      ego.on_collision(on_collision)
      npc1.on_collision(on_collision)
      npc1.follow(waypoints)
      sim.run(60)
      #self.assertGreater(len(collisions), 0)
      #self.assertInBetween(collisions[0][2], collisions[0][0].state.position, collisions[0][1].state.position, "Ego Collision")
      #self.assertTrue(collisions[0][0].name == "Lincoln2017MKZ (Apollo 5.0)" or collisions[0][1].name == "Lincoln2017MKZ (Apollo 5.0)")
      #self.assertTrue(True)


  #define ego car and connect apollo
  def setup_ego(self, sim, ego_name, agent_type,BRIDGE_HOST,HDmap_name): 
    spawns = sim.get_spawn()
    state = lgsvl.AgentState()
    state.transform = spawns[0]
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    right = lgsvl.utils.transform_to_right(spawns[0])
    ego = sim.add_agent(ego_name, agent_type, state)
    #print(sim.get_agents())
    ego.connect_bridge(BRIDGE_HOST, 9090)
    dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
    dv.set_hd_map(HDmap_name)
    dv.set_vehicle('Lincoln2017MKZ LGSVL')
    modules = []
    modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']
    destination = state.position + 250* forward
    dv.setup_apollo(destination.x, destination.z, modules)
    return ego
  
  #define npc car
  # NPC, 10 meters ahead
  def setup_npc1(self,sim,npc1_name,agent_type):
    spawns = sim.get_spawn()
    state = lgsvl.AgentState()
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    right = lgsvl.utils.transform_to_right(spawns[0])
    state.transform.position = spawns[0].position + 10 * forward
    state.transform.rotation = spawns[0].rotation
    npc1 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

    # This block creates the list of waypoints that the NPC will follow
    # Each waypoint is an position vector paired with the speed that the NPC will drive to it
    waypoints = []
    x_max = 2
    z_delta = 12

    layer_mask = 0
    layer_mask |= 1 << 0 # 0 is the layer for the road (default)

    for i in range(20):
      speed = 24# if i % 2 == 0 else 12
      px = 0
      pz = (i + 1) * z_delta
      # Waypoint angles are input as Euler angles (roll, pitch, yaw)
      angle = spawns[0].rotation
      # Raycast the points onto the ground because BorregasAve is not flat
      hit = sim.raycast(spawns[0].position + px * right + pz * forward, lgsvl.Vector(0,-1,0), layer_mask) 

      # Trigger is set to 10 meters for every other waypoint (0 means no trigger)
      tr = 0
      if (i % 2):
        tr = 15 
      wp = lgsvl.DriveWaypoint(position=hit.point, speed=speed, angle=angle, idle=0, trigger_distance=tr)
      waypoints.append(wp)
    return npc1,waypoints












#past version

# sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "10.78.4.163"), 8083)
# BRIDGE_HOST = os.environ.get("BRIDGE_HOST", "10.78.4.163")

# if sim.current_scene == "BorregasAve":
#   sim.reset()
# else:
#   sim.load("BorregasAve")

# spawns = sim.get_spawn()

# # EGO

# spawns = sim.get_spawn()
# state = lgsvl.AgentState()
# state.transform = spawns[0]
# forward = lgsvl.utils.transform_to_forward(spawns[0])
# right = lgsvl.utils.transform_to_right(spawns[0])
# ego = sim.add_agent("Lincoln2017MKZ (Apollo 5.0)", lgsvl.AgentType.EGO, state)
# destination = state.position + 50* forward



# # NPC, 10 meters ahead
# state = lgsvl.AgentState()
# state.transform.position = spawns[0].position + 10 * forward
# state.transform.rotation = spawns[0].rotation
# npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state)

# vehicles = {
#   ego: "EGO",
#   npc: "Sedan",
# }

# ego.connect_bridge(BRIDGE_HOST, 9090)

# dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
# dv.set_hd_map('Borregas Ave')
# dv.set_vehicle('Lincoln2017MKZ LGSVL')
# modules = []
# modules = ['Localization', 'Transform', 'Routing','Prediction', 'Planning','Control','Storytelling','Perception','Traffic Light','Camera']

# dv.setup_apollo(destination.x, destination.z, modules)


# # Executed upon receiving collision callback -- NPC is expected to drive through colliding objects
# def on_collision(agent1, agent2, contact):
#   name1 = vehicles[agent1]
#   name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
#   print("{} collided with {}".format(name1, name2))

# ego.on_collision(on_collision)
# npc.on_collision(on_collision)

# # This block creates the list of waypoints that the NPC will follow
# # Each waypoint is an position vector paired with the speed that the NPC will drive to it
# waypoints = []
# x_max = 2
# z_delta = 12

# layer_mask = 0
# layer_mask |= 1 << 0 # 0 is the layer for the road (default)

# for i in range(20):
#   speed = 24# if i % 2 == 0 else 12
#   px = 0
#   pz = (i + 1) * z_delta
#   # Waypoint angles are input as Euler angles (roll, pitch, yaw)
#   angle = spawns[0].rotation
#   # Raycast the points onto the ground because BorregasAve is not flat
#   hit = sim.raycast(spawns[0].position + px * right + pz * forward, lgsvl.Vector(0,-1,0), layer_mask) 

#   # Trigger is set to 10 meters for every other waypoint (0 means no trigger)
#   tr = 0
#   if (i % 2):
#     tr = 10 
#   wp = lgsvl.DriveWaypoint(position=hit.point, speed=speed, angle=angle, idle=0, trigger_distance=tr)
#   waypoints.append(wp)

# When the NPC is within 0.5m of the waypoint, this will be called
# def on_waypoint(agent, index):
#   print("waypoint {} reached".format(index))

# The above function needs to be added to the list of callbacks for the NPC
# npc.on_waypoint_reached(on_waypoint)

# The NPC needs to be given the list of waypoints. 
# A bool can be passed as the 2nd argument that controls whether or not the NPC loops over the waypoints (default false)
# npc.follow(waypoints)



# sim.run()
