import azure.functions as func
import pymongo

def main(req: func.HttpRequest) -> func.HttpResponse:

    request = req.get_json()

    if request:
        try:
            url = 'mongodb://thang123:UViw24r10Fgj9PDNd56aS66NgzIE3Jk8wZb21CdA2UcpzCxJ4KzUiUJHBtiX7HE6nA1tInnRQt1g8LdhSCIr5w==@thang123.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@thang123@' # TODO: Update with appropriate MongoDB connection information
            client = pymongo.MongoClient(url)
            database = client['Note']
            collection = database['advertisements']

            rec_id1 = collection.insert_one(eval(request))

            return func.HttpResponse(req.get_body())

        except ValueError:
            print("could not connect to mongodb")
            return func.HttpResponse('Could not connect to mongodb', status_code=500)

    else:
        return func.HttpResponse(
            "Please pass name in the body",
            status_code=400
        )