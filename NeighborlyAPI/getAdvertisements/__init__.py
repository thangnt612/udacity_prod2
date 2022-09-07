import azure.functions as func
import pymongo
import json
from bson.json_util import dumps

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        url = 'mongodb://thang123:UViw24r10Fgj9PDNd56aS66NgzIE3Jk8wZb21CdA2UcpzCxJ4KzUiUJHBtiX7HE6nA1tInnRQt1g8LdhSCIr5w==@thang123.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@thang123@' # TODO: Update with appropriate MongoDB connection information
        client = pymongo.MongoClient(url)
        database = client['Note']
        collection = database['advertisements']


        result = collection.find({})
        result = dumps(result)

        return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
    except:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)

