import pymongo as mongo
import yaml

CONFIG_FILE_NAME = "../config.yaml"
config = yaml.load(open(CONFIG_FILE_NAME))

def chooseTheScene(log):
    log.info('Loading configuration')

    host = config['configuration']['MongoDB']['host']
    port = config['configuration']['MongoDB']['port']

    client = mongo.MongoClient(host=host, port=port)
    log.info('Configuration ')

    db = client.mydb
    collection = db.test
    result = collection.find({},{"_id":1})
    for i in result:
        print(i['_id'])

    scene_number = input("Please choose the scene number : ")
    print(result)


    pass