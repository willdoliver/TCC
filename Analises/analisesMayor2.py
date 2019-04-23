# -*- coding: utf-8 -*-
#import matplotlib.pyplot as plt
import os,re,sys
import json
import math
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


############ Formulas ############
#
#	X1 = P∗log(N+1)		
#	X2 = R∗log(N+1)
#	
#	P = Troca de Prefeitos
#	R = Reaparicao de Prefeitos
#	N = Numero de checkins ultimos 30 dias

#######################################################################################
################################    M A I N    ########################################
#######################################################################################

nome_local = []
results = []
resultCats = []


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def calc_pref(mayor):
	size = len(mayor)
	resultado = 0

	if size == 1:
		return 0
	
	for info,value in enumerate(mayor):
		current = mayor[info]
		# if cat.encode('utf-8') == 'Universidade Tecnológica Federal Do Paraná Utfpr':
		# 	print(current)
		# 	print(resultado)

		try:
			if current != mayor[info+1]:
				resultado += 1
		except:
			continue
	return resultado


def calc_reaparicao(mayor):
	size = len(mayor)

	mayors = []
	for may in mayor:
		mayors.append(int(may))

	resultado = 0

	if size < 2 :
		return 0

	try:
		# Percorre lista de prefeitos
		for i,v in enumerate(mayors):
			if ( mayors[i] != mayors[i+1] and mayors[i:].count(mayors[i]) > 1):
				resultado += 1
	except:
		return resultado

def sortSecond(val): 
    return val[2]

def analisaDados(arqAnalise,arqSaida):
	# Loop para coletar locais unicas
	with open('Req200/'+arqAnalise, 'r') as f:
		print("Analisando locais...")
		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)

		nome_local = []
		for i in o["all"]:
			nome_local.append(i["nomeLocal"])
		nome_local = remove_repetidos(nome_local)

	# Loop para comparar cada local unico com seus correspondentes no JSON
	with open('Req200/'+arqAnalise, 'r') as f:

		categorias = []
		
		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)

		print("Analisando JSON...")
		# Para cada local distinto
		saida = []
		for loc in nome_local:
			# print(loc)
			resultMax = 0
			trocaMax = 0
			reapMax = 0
			trocaPrefs = 0
			tot = 0
			peo = 0
			mayors = []
			total = []
			people = []
			struct = []

			for item in o["all"]:
				# Para cada local do JSON que for do local em questao
				if loc == item["nomeLocal"]:

					cat = item["categories"][0]["name"].encode('utf-8')	
					tot = item["mayor"]["count"]
					data_atual = item["data consulta"]
					try:
						peo = item["mayor"]["user"]["id"]
					except:
						peo = '0'

					struct.append([data_atual, cat, tot, peo, loc.encode('utf-8')])

			struct.sort(reverse=True, key=sortSecond)

			day_done=[]
			for s in struct:		
				if s[0] in day_done:
					continue
				else:
					day_done.append(str(s[0]))
					results.append([s[0], s[1], s[2], s[3], s[4]])

			del struct[:]
			del day_done[:]

			# results possui o maior valor de check-ins para cada data
			for r in results:
				if loc.encode('utf-8') == r[4]:
					# print(r)
					people.append(r[3])
					total.append(r[2])

				else:
					continue

			# Calculo de trocas
			trocaPrefs = calc_pref(people)

			# Calcula disputa
			reapPrefs = calc_reaparicao(people)
			
			trocas = round(trocaPrefs * (math.log( sum(total)+1 )),2)
			disputa = round(reapPrefs * (math.log( sum(total)+1 )),2)	

			saida.append([trocas, trocaPrefs, loc, disputa, reapPrefs, sum(total), cat])

			resultCats.append([cat, loc, sum(total), trocaPrefs, reapPrefs])

		arq = open(arqSaida+'.txt', 'w')
		print("Escrevendo saida arquivo: "+ arqSaida+'.txt')
		arq.write("-------------------")
		arq.write("\n")
		arq.write("RESULTADOS POR LOCAL")
		arq.write("\n")
		arq.write("-------------------")
		arq.write("\n")
		saida.sort(reverse=True)

		for s in saida:
			if s[2].encode('utf-8') == "Canonicalurl': U'Https:":
				continue
			# print(s)
			arq.write(str(s[2].encode('utf-8')) + ' - ' + str(s[6])) # Local
			arq.write("\n")
			arq.write( "P = " + str( s[1]) ) # quantidade de trocas
			arq.write("\n")
			arq.write( "Trocas: " + str(s[0]) ) # Calculo da formula para P
			arq.write("\n")
			arq.write( "R = " + str(s[4]) ) # quantidade de reaparicoes
			arq.write("\n")
			arq.write( "Disputa: " + str(s[3]) ) # Calculo da formula para R
			arq.write("\n")
			arq.write( "Check-ins = " + str(s[5]) ) # numero de reaparicoes
			arq.write("\n")
			arq.write("-------------------")
			arq.write("\n")

		arq.close()
		
		resultCats.sort()
		
		# print(resultCats)
		# exit(0)
		
		res = []
		for r in resultCats:
			res.append(r[0])
		res = remove_repetidos(res)
		# print(res)
		
		checkinsCat=[]
		for r in res:
			agrupTrocas = []
			agrupReap = []
			agrupCat=[]
			for val in resultCats:	
				if r == val[0]:
					agrupCat.append(val[2])
					agrupTrocas.append(val[3])
					agrupReap.append(val[4])
				else:
					continue

			checkinsCat.append([
				pd.Series(agrupTrocas).mean(),
				pd.Series(agrupReap).mean(),
				pd.Series(agrupCat).median(),
				r,
				len(agrupCat),
				pd.Series(agrupCat).std(), # Desvio padrao
				agrupCat
			])
		print(checkinsCat)
		# exit(0)
		checkinsCat.sort(reverse=True)
		# print(checkinsCat)
		arqCat = open(arqSaida+'Cats.txt', 'w')
		
		arqCat.write("categorias,Media Check-ins,Fórmula Trocas,Fórmula Disputa,Count,Desvio Padrao, Elements")
		arqCat.write("\n")
		
		numCategs = 0
		catsMax = 50
	
		for cat in checkinsCat:
			arqCat.write(str(cat[3]))
			arqCat.write('	')
			arqCat.write(str(cat[2]))
			arqCat.write('	')
			arqCat.write(str(round(cat[0],2)))
			arqCat.write('	')
			arqCat.write(str(round(cat[1],2)))
			arqCat.write('	')
			arqCat.write(str(cat[4]))
			arqCat.write('	')
			arqCat.write(str(round(cat[5],2)))
			arqCat.write('	')
			arqCat.write(str(cat[6]))
			arqCat.write('\n')
			numCategs += 1

			if numCategs == catsMax:
				break
	
		arqCat.close()

	print("Fim arquivo " + arqAnalise + '\n\n')


def main():

	# analisaDados('curitibaWithName.json', 'CWB_resultado')
	# analisaDados('chicagoWithName.json', 'CHICAGO_resultado')
	analisaDados('saoPauloWithName.json', 'SP_resultado')
	

if __name__ == '__main__':
	main()


# {
# 	"data consulta": "2018-03-20",
# 	"mayor": {
# 		"count": 2,
# 		"user": {
# 			"lastName": "Motti",
# 			"gender": "male",
# 			"id": "14614044",
# 			"firstName": "Flavio"
# 		}
# 	},
# 	"categories": [{
# 		"pluralName": "Banks",
# 		"primary": 1,
# 		"name": "Bank",
# 		"shortName": "Bank"
# 	}]
# }
