import certifi
import pymongo
import ssl


client = pymongo.MongoClient("mongodb+srv://Anamika:Pass1234@ytscapermd.nk8ewov.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client.test
#client1 = pymongo.MongoClient(connection, tlsCAFile=certifi.where())
print(db)

d={
    "name" : "Anamika",
    "email":"aniverma2006@gmail.com",
    "surname":"sinha"
}

db1=client['mongotest']
coll =db1['test']
coll.insert_one(d)