import lgsvl
import time
import os
from pynput.keyboard import Listener
from pynput import keyboard
from absl import flags


def startSimulation(log, simconn, time_limit):

    print("*---------       Simulation        ----------*")
    log.info(time_limit)

    all_key = []

    def on_press(key):
        pass

    def on_release(key):
        all_key.append(str(key))
        # print(all_key)
        if "'s'" in all_key:
            # print("stop")
            log.warning("simulation is stopped !")
            # simconn.sim.stop()
            # all_key.clear()

        if "'r'" in all_key:
            # print("run")
            log.info("simulation is running !")
            # simconn.sim.run()
            all_key.clear()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    report_path = "./report/"  # 文件保存路径，如果不存在就会被重建
    if not os.path.exists(report_path):  # 如果路径不存在
        os.makedirs(report_path)

    print("1.Simulating the scene choosed in step.1[ default ]")
    print("2.Simulating all scenes in /json ?")
    choice = input("Please enter your option : ")
    if choice == "2":
        '''
        1、获取文件下数据数目

        2、设置simconn的路径
        '''
        path = './json'
        filenum = len([lists for lists in os.listdir(path)
                       if os.path.isfile(os.path.join(path, lists))])
        print('filenum :', filenum)

        file_address = []

        scenarios = []
        for fileName in os.listdir(path):
            fileName = os.path.splitext(fileName)[0]
            scenarios.append(fileName)

        for lists in os.listdir(path):
            sub_path = os.path.join(path, lists)
            file_address.append(sub_path)
            print(sub_path)

        print("Start simulating all scenes !")
        range_number = int(input("Please enter simulation times："))
        print("ps. r(un),s(top)")
        for m in range(range_number):
            for i in range(filenum):
                simconn.address = file_address[i]
                with simconn as a:
                    sim = a[0]
                    ego = a[1]
                    npc_ls = a[2]
                    ped_ls = a[3]
                    npc_waypoints_ls = a[4]
                    ped_waypoints_ls = a[5]
                    destination = a[6]
                    vehicles = a[7]

                    event_collision = list()
                    event_destination = list()
                    event_overspeed = list()
                    event_brakelight = list()
                    result = list()

                    def collision(agent1, agent2, contact):
                        name1 = vehicles[agent1]
                        name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
                        contact_position = lgsvl.agent.Agent(
                            ego.uid, sim).state.position
                        log.error(u"{} collided with {} at {}".format(
                            name1, name2, contact_position))
                        event_collision.append("{} collided with {} at {}".format(
                            name1, name2, contact_position))
                        print("simulation finished,please check the test report")
                        sim.stop()

                    def destination_reached(kind):
                        if kind == "destination_reached":
                            event_destination.append("destination_reached")
                            print(
                                "destination_reached,simulation finished,test report is generating")
                            time.sleep(3)
                            sim.stop()
                        pass

                    def over_speed(kind):
                        if kind == "over_speed":
                            event_overspeed.append(
                                "over speed when simulation start {} s later n/".format(time.time() - t0))

                    def brake_light(kind):
                        if kind == "brake_light":
                            event_brakelight.append(
                                "brake light when simulation start {} s later n/".format(time.time() - t0))

                    ego.on_collision(collision)
                    ego.on_custom(destination_reached)
                    ego.on_custom(over_speed)
                    ego.on_custom(brake_light)

                    # 让npc和行人开始动作
                    for npc in npc_ls:
                        if npc_waypoints_ls[npc]:
                            npc_ls[npc].follow_waypoints_jsonfile(
                                npc_waypoints_ls[npc])

                    for ped in ped_ls:
                        if ped_waypoints_ls[ped]:
                            ped_ls[ped].follow_waypoints_jsonfile(
                                ped_waypoints_ls[ped])

                    # 判断是否到达终点---临时方案
                    t0 = time.time()
                    delt_t = 0
                    while True:
                        if "'s'" in all_key:
                            pass
                        else:
                            sim.run(0.5)
                            ego_state = lgsvl.agent.Agent(ego.uid, sim)
                            ego_state_now = ego_state.state
                            delt_forward = destination.x - ego_state_now.position.x
                            delt_right = destination.z - ego_state_now.position.z
                            # if delt_forward < 5 and delt_right < 5:
                            #     time.sleep(3)
                            #     event_destination.append("destination_reached")
                            #     print(
                            #         "destination reached,simulation finished,test report is generating")
                            #     sim.stop()
                            #     break
                            t1 = time.time()
                            delt_t = t1 - t0
                            if delt_t > time_limit:
                                print(
                                    "{}s reached,simulation finished,test report is generating".format(delt_t))
                                sim.stop()
                                break
                            if event_collision:
                                break
                            if event_destination:
                                break
                    ego_state_end = lgsvl.agent.Agent(ego.uid, sim)
                    ego_end_position = ego_state_end.state.position

                    if event_collision == [] and event_overspeed == [] and event_brakelight == [] and event_destination != []:
                        result.append("PASS")
                    else:
                        result.append("FAIL")

                    print("report generated")
                    print("simulation result:", result)

                    file_path = "./report/report_{}_{}.txt".\
                        format(scenarios[i], time.strftime(
                            '%Y-%m-%d_%H:%M:%S', time.localtime(time.time())))
                    with open(file_path, 'w', encoding='utf8') as report:
                        report_contents = \
                            " *---------------------------------------------------------------------------------------------------------------------------------*" \
                            " *                                                      \n" \
                            " *             scenario name:{}                         \n\n" \
                            " *             simulation result:{}                     \n\n" \
                            " *             destination reached:{}                   \n\n" \
                            " *             collsion:{}                              \n\n" \
                            " *             over speed:{}                            \n\n" \
                            " *             brake light:{}                           \n\n" \
                            " *             sim time:{}                              \n\n" \
                            " *             stop position:{}                         \n\n" \
                            " *                                                      \n" \
                            " *---------------------------------------------------------------------------------------------------------------------------------*"\
                            .format(report.name,
                                    result,
                                    event_destination,
                                    event_collision,
                                    event_overspeed,
                                    event_brakelight,
                                    delt_t,
                                    ego_end_position
                                    )
                        report.write(report_contents)

        pass
    else:
        if simconn.address == "":
            print("Address is NULL, please get back to stpe.1 to check or run all scenes")
            log.warning(
                "Address is NULL, please get back to stpe.1 to check or run all scenes")
            return
        range_number = int(input("Please enter simulation times："))
        print("ps. r(un),s(top)")
        for i in range(range_number):
            print("simulation num:", i + 1)
            with simconn as a:
                sim = a[0]
                ego = a[1]
                npc_ls = a[2]
                ped_ls = a[3]
                npc_waypoints_ls = a[4]
                ped_waypoints_ls = a[5]
                destination = a[6]
                vehicles = a[7]
                scenario_name = a[8]

                event_collision = list()
                event_destination = list()
                event_overspeed = list()
                event_brakelight = list()
                result = list()

                def collision(agent1, agent2, contact):
                    name1 = vehicles[agent1]
                    name2 = vehicles[agent2] if agent2 is not None else "OBSTACLE"
                    contact_position = lgsvl.agent.Agent(
                        ego.uid, sim).state.position
                    log.error(u"{} collided with {} at {}".format(
                        name1, name2, contact_position))
                    event_collision.append("{} collided with {} at {}".format(
                        name1, name2, contact_position))
                    print("simulation finished,please check the test report")
                    sim.stop()

                def destination_reached(kind):
                    if kind == "destination_reached":
                        event_destination.append("destination_reached")
                        print("simulation finished,test report is generating")
                        time.sleep(3)
                        sim.stop()
                    pass

                def over_speed(kind):
                    if kind == "over_speed":
                        event_overspeed.append(
                            "over speed when simulation start {} s later n/".format(time.time() - t0))

                def brake_light(kind):
                    if kind == "brake_light":
                        event_brakelight.append(
                            "brake light when simulation start {} s later n/".format(time.time() - t0))

                ego.on_collision(collision)
                ego.on_custom(destination_reached)
                ego.on_custom(over_speed)
                ego.on_custom(brake_light)

                # 让npc和行人开始动作
                for npc in npc_ls:
                    if npc_waypoints_ls[npc]:
                        npc_ls[npc].follow_waypoints_jsonfile(
                            npc_waypoints_ls[npc])

                for ped in ped_ls:
                    if ped_waypoints_ls[ped]:
                        ped_ls[ped].follow_waypoints_jsonfile(
                            ped_waypoints_ls[ped])

                # 判断是否到达终点---临时方案
                t0 = time.time()
                delt_t = 0
                while True:
                    if "'s'" in all_key:
                        pass
                    else:
                        sim.run(0.5)
                        ego_state = lgsvl.agent.Agent(ego.uid, sim)
                        ego_state_now = ego_state.state
                        delt_forward = destination.x - ego_state_now.position.x
                        delt_right = destination.z - ego_state_now.position.z
                        # if delt_forward < 5 and delt_right < 5:
                        #     time.sleep(3)
                        #     event_destination.append("destination_reached")
                        #     print()
                        #     print(
                        #         "destination reached,simulation finished,test report is generating")
                        #     sim.stop()
                        #     break
                        t1 = time.time()
                        delt_t = t1 - t0
                        if delt_t > time_limit:
                            print()
                            print(
                                "{}s reached,simulation finished,test report is generating".format(delt_t))
                            sim.stop()
                            break
                        if event_collision:
                            break
                        if event_destination:
                            break
                        pass

                ego_state_end = lgsvl.agent.Agent(ego.uid, sim)
                ego_end_position = ego_state_end.state.position
                if event_collision == [] and event_overspeed == [
                ] and event_brakelight == [] and event_destination != []:
                    result.append("PASS")
                else:
                    result.append("FAIL")

                print("report generated")
                print("simulation result:", result)

                file_path = "./report/report_{}_{}.txt".\
                    format(scenario_name, time.strftime(
                        '%Y-%m-%d_%H:%M:%S', time.localtime(time.time())))
                with open(file_path, 'w', encoding='utf8') as report:
                    report_contents = \
                        " *---------------------------------------------------------------------------------------------------------------------------------*" \
                        " *                                                      \n" \
                        " *             scenario name:{}                         \n\n" \
                        " *             simulation result:{}                     \n\n" \
                        " *             destination reached:{}                   \n\n" \
                        " *             collsion:{}                              \n\n" \
                        " *             over speed:{}                            \n\n" \
                        " *             brake light:{}                           \n\n" \
                        " *             sim time:{}                              \n\n" \
                        " *             stop position:{}                         \n\n" \
                        " *                                                      \n" \
                        " *---------------------------------------------------------------------------------------------------------------------------------*"\
                        .format(report.name,
                                result,
                                event_destination,
                                event_collision,
                                event_overspeed,
                                event_brakelight,
                                delt_t,
                                ego_end_position
                                )
                    report.write(report_contents)

            # 如果使用proxy
            # sim.remote.finish()
    pass
