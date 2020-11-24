import os
import math
import signal
import json
import yaml

from lgsvl.geometry import Vector, BoundingBox, Transform
from lgsvl.simulator import Simulator
from lgsvl.agent import AgentType, AgentState, VehicleControl, Vehicle, EgoVehicle, NpcVehicle, Pedestrian, DriveWaypoint, WalkWaypoint, WaypointTrigger, TriggerEffector, NPCControl, Agent
from lgsvl.controllable import Controllable
from lgsvl.dreamview import Connection
import lgsvl.utils


# 用户定义仿真次数 等
# range_number = int(input("请输入测试次数："))


class TestTimeout(Exception):
    pass


class TestException(Exception):
    pass


# 定义基类
class SimConnection:
    def __init__(
            self,
            seconds=100,
            scene="BorregasAve",
            error_message=None,
            load_scene=True,
            address="",
            log=None):
        if error_message is None:
            error_message = 'test timed out after {}s.'.format(seconds)
        try:
            CONFIG_FILE_NAME = "./config.yaml"
            Loader = yaml.FullLoader
            config = yaml.load(open(CONFIG_FILE_NAME), Loader=Loader)
        except BaseException:
            print("Loading configuration failed...")
            return
        self.seconds = seconds
        self.error_message = error_message
        self.scene = scene
        self.load_scene = load_scene
        self.address = address
        self.port = config['configuration']['Simulation']['port']
        self.host = config['configuration']['Simulation']['host']
        self.apollo_host = config['configuration']['Simulation']['apollo_host']
        self.apollo_port = config['configuration']['Simulation']['apollo_port']
        self.scene_name = ""

    def handle_timeout(self, signum, frame):
        raise TestTimeout(self.error_message)

    # 定义enter函数
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
        # 连接simulator
        self.sim = Simulator(os.environ.get(
            "SIMULATOR_HOST", self.host), self.port)

        # 读取场景数据
        with open(self.address, 'r', encoding='utf8') as data:
            data = json.load(data)
            map_name = data["map"]["name"]
            agents = data["agents"]
            # 下载地图环境
            self.scene = map_name
            if self.load_scene:
                if self.sim.current_scene == self.scene:
                    self.sim.reset()
                    signal.alarm(self.seconds - 20)
                else:
                    self.sim.load(self.scene)
            print("current scene:", self.sim.current_scene)

            # self.ego_ls = {}
            # self.ego_waypoints_ls = {}
            self.npc_ls = {}
            self.npc_waypoints_ls = {}
            self.ped_ls = {}
            self.ped_waypoints_ls = {}
            self.vehicles = {}

            for i in range(len(agents)):
                agent = agents[i]
                # agent_uid = agent["uid"]
                agent_variant = agent["variant"]
                agent_type = agent["type"]
                agent_state = lgsvl.agent.AgentState()
                agent_state.transform.position = lgsvl.geometry.Vector(
                    agent["transform"]["position"]["x"],
                    agent["transform"]["position"]["y"],
                    agent["transform"]["position"]["z"])
                agent_state.transform.rotation = lgsvl.geometry.Vector(
                    agent["transform"]["rotation"]["x"],
                    agent["transform"]["rotation"]["y"],
                    agent["transform"]["rotation"]["z"])
                waypoints = agent["waypoints"]

                if agent_type == 1:
                    self.ego = self.sim.add_agent(
                        agent_variant, lgsvl.agent.AgentType.EGO, agent_state)

                    # apollo的host
                    self.ego.connect_bridge(self.apollo_host, self.apollo_port)
                    self.vehicles[self.ego] = "EGO"
                    dv = lgsvl.dreamview.Connection(
                        self.sim, self.ego, self.apollo_host)

                    # 后续将Apollo端和LG端的地图名称统一后，这里可以传入json中的map_name
                    dv.set_hd_map('Borregas Ave')
                    # 需Apollo,lg两端统一后，才能从json传入，暂时先写死
                    dv.set_vehicle('Lincoln2017MKZ LGSVL')
                    modules = [
                        'Localization',
                        'Transform',
                        'Routing',
                        'Prediction',
                        'Planning',
                        'Control',
                        'Storytelling']
                    forward = lgsvl.utils.transform_to_forward(
                        agent_state.transform)
                    self.destination = agent_state.position + \
                        200 * forward  # 目前拿到的json文件都没有ego车的目的点信息
                    dv.setup_apollo(
                        self.destination.x, self.destination.z, modules)
                    # 发送目的点坐标给simulator
                    self.ego.destination_set(self.destination)

                elif agent_type == 2:
                    self.npc_i = self.sim.add_agent(
                        agent_variant, lgsvl.agent.AgentType.NPC, agent_state)
                    self.vehicles[self.npc_i] = agent_variant
                    self.npc_ls["npc_{}".format(i)] = self.npc_i
                    self.npc_waypoints_ls["npc_{}".format(i)] = waypoints

                else:
                    self.pedestrain_i = self.sim.add_agent(
                        agent_variant, lgsvl.agent.AgentType.PEDESTRIAN, agent_state)
                    self.vehicles[self.pedestrain_i] = agent_variant
                    self.ped_ls["ped_{}".format(i)] = self.pedestrain_i
                    self.ped_waypoints_ls["ped_{}".format(i)] = waypoints

        # 定义信号灯的策略
        traffic_signals = self.sim.get_controllables("signal")
        control_policy = "green=30;yellow=3;red=2;loop"
        # Control this traffic light with a new control policy
        # traffic_signal.control(control_policy)
        for i in range(len(traffic_signals)):
            traffic_signals[i].control(control_policy)
            # print("trafiice signal policy:",traffic_signals[i].control_policy)
            i += 1

        return_list = list()
        return_list.append(self.sim)
        return_list.append(self.ego)
        return_list.append(self.npc_ls)
        return_list.append(self.ped_ls)
        return_list.append(self.npc_waypoints_ls)
        return_list.append(self.ped_waypoints_ls)
        return_list.append(self.destination)
        return_list.append(self.vehicles)
        return_list.append(self.scene_name)

        return return_list
    # 定义exit函数

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        # agents = self.sim.get_agents()
        # for a in agents:
        #   self.sim.remove_agent(a)
        # sim.remote.finish()  #使用代理连接simulator时需要加这行代码
        self.sim.close()
