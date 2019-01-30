from pymongo import MongoClient

client = MongoClient()
db = client['curitiba']

cursor = db.curitiba.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
					 
saida = open("curitiba.txt","w")

for document in cursor:
    saida.write(str(document)+'\n')