import pymongo as mongo


client = mongo.MongoClient(host='0.0.0.0', port=27017)
db = client.mydb
collection = db.test


def checkReport(log):
    pass