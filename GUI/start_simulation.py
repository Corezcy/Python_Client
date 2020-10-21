import lgsvl
import time

def startSimulation(log,sim):
    with sim as a:
        sim = a[0]
        ego = a[1]
        npc_ls = a[2]
        ped_ls = a[3]
        npc_waypoints_ls = a[4]
        ped_waypoints_ls = a[5]
        destination = a[6]
        # 定义碰撞函数
        collisions = []


        def collision(agent1, agent2, contact):
            collisions.append([agent1, agent2, contact])
            print("ego 车发生碰撞")
            # lgsvl.dreamview.Connection.disable_apollo(destination.x, destination.z, modules)
            sim.stop()


        def destination_reached():
            if kind == "destination_reached":
                # lgsvl.dreamview.Connection.disable_apollo(destination.x, destination.z, modules)
                sim.stop()


        ego.on_collision(collision)
        ego.on_custom(destination_reached)

        # 定义判断Apollo是否正常运行的函数
        # controlReceived = False
        # def on_control_received(agent, kind, context):
        #     global controlReceived
        #     # There can be multiple custom callbacks defined, this checks for the appropriate kind
        #     if kind == "checkControl":
        #         # Stops the Simulator running, this will only interrupt the first sim.run(30) call
        #         sim.stop()
        #         controlReceived = True
        # #先判断Apollo是否启动成功
        # ego.on_custom(on_control_received)
        # sim.run(30)
        # #If a Control message was not received, then the AD stack is not ready and the scenario should not continue
        # if not controlReceived:
        #     raise Exception("AD stack is not ready after 30 seconds")
        #     sys.exit()
        # 让npc和行人开始动作
        for npc in npc_ls:
            npc_ls[npc].follow(npc_waypoints_ls[npc])

        # 判断是否到达终点---临时方案
        while True:
            sim.run(0.5)
            ego_state = lgsvl.Agent(ego.uid, sim)
            ego_state_now = ego_state.state
            delt_forward = destination.x - ego_state_now.position.x
            delt_right = destination.z - ego_state_now.position.z
            # print(ego_state)
            if delt_forward < 5 and delt_right < 5:
                time.sleep(3)
                break
        ego_state_end = lgsvl.Agent(ego.uid, sim)
        ego_end_position = ego_state_end.state.position
        delt_forward = destination.x - ego_end_position.x
        delt_right = destination.z - ego_end_position.z
        print(delt_forward, delt_right)
        sim.stop()

        #如果使用proxy
        #sim.remote.finish()
    pass