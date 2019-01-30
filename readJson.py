import json

arq = open('curitiba.txt','r')
#percorre o arquivo linha por linha e separa por virgula cat,url
#for i in arq.readlines():
	#content = json.loads(i)
	#print(content)
	#exit(0)
    #data = json.load(read_file)

	#dta_consulta = data["data consulta"]
	#print (dta_consulta)

with open('curitiba.txt') as json_file:  
    data = json.load(json_file)
    print(data)
    #for p in data['data consulta']:
    #    print('Name: ' + p['name'])