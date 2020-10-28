import pymongo as mongo
import yaml
import json
import sys
import os


def chooseTheScene(log, simconnection):
    try:
        CONFIG_FILE_NAME = "./config.yaml"
        Loader = yaml.FullLoader
        config = yaml.load(open(CONFIG_FILE_NAME), Loader=Loader)
    except BaseException:
        log.error("Loading configuration failed...")
        print("Loading configuration failed...")
        return

    log.info('Loading MongoDB configuration ...')

    host = config['configuration']['MongoDB']['host']
    port = config['configuration']['MongoDB']['port']
    db = config['configuration']['MongoDB']['database']
    collection = config['configuration']['MongoDB']['collection']

    client = mongo.MongoClient(host=host, port=port)
    log.info('MongoDB Configuration finished !')

    print("1.Check all the scenes[ default ]")
    print("2.Search scenes by keywords")
    choice = input("Please enter your option : ")
    if choice == "2":

        print("Note: Searching scene name according to regular expression rules")
        key_words = input("Please enter key word : ")

        collection = client.get_database(db).get_collection(collection)
        result = collection.find(
            {"_id": {'$regex': ".*"+key_words+".*", "$options": "-i"}}).sort("_id", 1)
        result_num = collection.count(
            {"_id": {'$regex': ".*"+key_words+".*", "$options": "-i"}})
        temp = result.clone()

        if result_num == 0:
            print()
            print("No relevant scene !")
            print()
            return

        print("Here is(are) scene(s) according to rules : ")
        print("*--------------------------------------------*")
        m = 1
        for i in result:
            print("\t\t"+str(m)+". " + i['_id'])
            m += 1
        print("*--------------------------------------------*")

        scene_number = input(
            "Please choose the scene number (input 'all' to download all scenes): ")
        if scene_number == "all":

            result = collection.find(
                {"_id": {'$regex': ".*"+key_words+".*", "$options": "-i"}}).sort("_id", 1)
            for i in result:
                json_path = "./json/"  # 文件保存路径，如果不存在就会被重建
                if not os.path.exists(json_path):  # 如果路径不存在
                    os.makedirs(json_path)

                with open(json_path + i['_id'] + '.json', 'w') as f:
                    f.write(json.dumps(i))
                    f.close()
                print("The scene [ " + i['_id'] + " ] is saved in " +
                      './json/' + i['_id'] + '.json')
                log.info("The scene [ " + i['_id'] + " ] is saved in " +
                         './json/' + i['_id'] + '.json')

            print("All scenes are downloaded")
            log.info("All scenes are downloaded")

            return

        scene_number = int(scene_number)
        if scene_number > 0 and scene_number <= temp.count():

            scene_name = temp[scene_number - 1]
            print("The scene [ " + scene_name['_id'] + " ] is choosed")
            log.info("The scene [ " + scene_name['_id'] + " ] is choosed")

            json_file = collection.find({"_id": scene_name['_id']})

            json_path = "./json/"  # 文件保存路径，如果不存在就会被重建
            if not os.path.exists(json_path):  # 如果路径不存在
                os.makedirs(json_path)

            with open(json_path + scene_name['_id'] + '.json', 'w') as f:
                f.write(json.dumps(json_file[0]))
                f.close()

            if scene_name['_id'] != "":
                simconnection.address = json_path + scene_name['_id'] + '.json'
                simconnection.scene_name = scene_name['_id']

                print("The scene [ " + scene_name['_id'] + " ] is saved in " +
                      './json/' + scene_name['_id'] + '.json')
                log.info("The scene [ " + scene_name['_id'] + " ] is saved in " +
                         './json/' + scene_name['_id'] + '.json')

            else:
                print("Failed to choose the scene ... Please get back to step.1")
                log.error(
                    "Failed to choose the scene ... Please get back to step.1")
                return

        else:
            print("The scene number is invalid, please check the scene number !")
            log.warning("The scene number is invalid !")

    else:
        collection = client.get_database(db).get_collection(collection)
        result = collection.find({}, {"_id": 1}).sort("_id", 1)
        temp = result.clone()
        m = 1
        print("Here are scenes : ")
        print("*--------------------------------------------*")
        for i in result:
            print("\t\t"+str(m)+". " + i['_id'])
            m += 1
        print("*--------------------------------------------*")

        scene_number = input(
            "Please choose the scene number (input 'all' to download all scenes): ")

        if scene_number == "all":

            result = collection.find({}).sort("_id", 1)
            for i in result:
                json_path = "./json/"  # 文件保存路径，如果不存在就会被重建
                if not os.path.exists(json_path):  # 如果路径不存在
                    os.makedirs(json_path)

                with open(json_path + i['_id'] + '.json', 'w') as f:
                    f.write(json.dumps(i))
                    f.close()
                print("The scene [ " + i['_id'] + " ] is saved in " +
                      './json/' + i['_id'] + '.json')
                log.info("The scene [ " + i['_id'] + " ] is saved in " +
                         './json/' + i['_id'] + '.json')

            print("All scenes are downloaded")
            log.info("All scenes are downloaded")

            return

        scene_number = int(scene_number)
        if scene_number > 0 and scene_number <= temp.count():

            scene_name = temp[scene_number - 1]
            print("The scene [ " + scene_name['_id'] + " ] is choosed")
            log.info("The scene [ " + scene_name['_id'] + " ] is choosed")

            json_file = collection.find({"_id": scene_name['_id']})

            json_path = "./json/"  # 文件保存路径，如果不存在就会被重建
            if not os.path.exists(json_path):  # 如果路径不存在
                os.makedirs(json_path)

            with open(json_path + scene_name['_id'] + '.json', 'w') as f:
                f.write(json.dumps(json_file[0]))
                f.close()

            if scene_name['_id'] != "":
                simconnection.address = json_path + scene_name['_id'] + '.json'
                simconnection.scene_name = scene_name['_id']

                print("The scene [ " + scene_name['_id'] + " ] is saved in " +
                      './json/' + scene_name['_id'] + '.json')
                log.info("The scene [ " + scene_name['_id'] + " ] is saved in " +
                         './json/' + scene_name['_id'] + '.json')

            else:
                print("Failed to choose the scene ... Please get back to step.1")
                log.error(
                    "Failed to choose the scene ... Please get back to step.1")
                return

        else:
            print("The scene number is invalid, please check the scene number !")
            log.warning("The scene number is invalid !")
    pass
