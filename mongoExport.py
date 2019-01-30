from pymongo import MongoClient

client = MongoClient()
dbCuritiba = client['curitiba']
dbSaoPaulo = client['sao_paulo']
dbChicago = client['chicago']
dbTokyo = client['tokyo']
dbNY = client['new_york']

cursor1 = dbCuritiba.curitiba.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
cursor2 = dbSaoPaulo.sao_paulo.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
cursor3 = dbChicago.chicago.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
cursor4 = dbTokyo.tokyo.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
cursor5 = dbNY.new_york.find({},{"response.venue.id":1,"data consulta":1,"response.venue.mayor":1,"response.venue.location.city":1})
					 
saida1 = open("curitiba.txt","w")
saida2 = open("sao_paulo.txt","w")
saida3 = open("chicago.txt","w")
saida4 = open("tokyo.txt","w")
saida5 = open("new_york.txt","w")

for document in cursor1:
    saida1.write(str(document)+'\n')

for document in cursor2:
    saida2.write(str(document)+'\n')

for document in cursor3:
    saida3.write(str(document)+'\n')

for document in cursor4:
    saida4.write(str(document)+'\n')

for document in cursor5:
    saida5.write(str(document)+'\n')