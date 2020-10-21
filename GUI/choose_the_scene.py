import pymongo as mongo
import yaml
import json


def chooseTheScene(log):
    try:
        CONFIG_FILE_NAME = "../config.yaml"
        Loader = yaml.FullLoader
        config = yaml.load(open(CONFIG_FILE_NAME), Loader=Loader)
    except:
        log.error("Loading configuration failed...")
        print("Loading configuration failed...")

    log.info('Loading MongoDB configuration ...')

    host = config['configuration']['MongoDB']['host']
    port = config['configuration']['MongoDB']['port']
    db = config['configuration']['MongoDB']['database']
    collection = config['configuration']['MongoDB']['collection']

    client = mongo.MongoClient(host=host, port=port)
    log.info('MongoDB Configuration finished !')

    collection = client.get_database(db).get_collection(collection)
    result = collection.find({},{"_id":1}).sort("_id",1)
    temp = result.clone()

    print("Here are scenes : ")
    for i in result:
        print(i['_id'])

    scene_number = int(input("Please choose the scene number : "))

    if scene_number > 0 and scene_number <= temp.count():

        scene_name = temp[scene_number - 1]
        print("The scene [ "+scene_name['_id']+" ] is choosed" )
        log.info("The scene [ "+scene_name['_id']+" ] is choosed")

        json_file = collection.find({"_id":scene_name['_id']})

        with open( './json/'+scene_name['_id']+'.json', 'w') as f:
            f.write(json.dumps(json_file[0]))
            f.close()

        return './json/'+scene_name['_id']+'.json'

    else:
        print("The scene number is invalid, please check the scene number !")
        log.warning("The scene number is invalid !")

    pass