# -*- coding: utf-8 -*-
#import matplotlib.pyplot as plt
import os,re
import json
import math
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

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
dates = []
nome_categ = []
results = []
results.append([])


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def calc_reaparicao(mayor):
	size = len(mayor)
	total = 0
	#print(mayor)

	if size < 2 :
		return 0

	# for info,value in enumerate(mayor):
	# 	print("[%s]= %s" % (info, value))
	# exit(0)

	for info,value in enumerate(mayor):
		current = mayor[info]

		aux = 0
		while (aux <= size-2):
			# print( str(aux) +' <> '+ str(size) )
			try:
				# print(current +' - '+ mayor[aux+2])
				if (current == mayor[aux+2] and current != mayor[aux+1]):
					# print( "total: " + str(total) )
					total += 1
					aux += 1
					del mayor[0]
					continue
				aux += 1
			except:
				return total

	return total

# Loop para coletar categorias unicas
with open('Req200/cwbShort.json', 'r') as f:
	data = json.load(f)
	n = json.dumps(data)
	o = json.loads(n)


	for i in o["all"]:
		nome_categ.append(i["categories"][0]["name"])
	nome_categ = remove_repetidos(nome_categ)
	# print(nome_categ)


with open('Req200/cwbShort.json', 'r') as f:
	data = json.load(f)
	n = json.dumps(data)
	o = json.loads(n)


	for cat in nome_categ:
		janela = 0
		qtd_dias = 0
		resultMax = 0
		trocaMax = 0
		reapMax = 0
		dateMax = ''
		mayors = []
		total = []
		people = []
		control = 0

		for item in o["all"]:

			# if cat == "Shopping Mall" and item["categories"][0]["name"] == "Shopping Mall":
			if cat == item["categories"][0]["name"]:
				
				dates.append(item["data consulta"])

				qtd_dias = abs((datetime.strptime(dates[0], '%Y-%m-%d') - datetime.strptime(dates[-1], '%Y-%m-%d')).days)
				#print(qtd_dias)
				
				# Percorre a janela de 30 dias
				if qtd_dias < 30:
					if control == 0:
						janela += 1
						total.append(item["mayor"]["count"])
						try:
							people.append(item["mayor"]["user"]["id"])
						except:
							continue
					
				# Quando fecha a janela dos 30 dias
				else:
					control = 1
					# print( str(dates[0]) +' - '+ str(dates[-1]) )
					# print( sum(total) )
					# print( len(people) )
					
					del dates[0]
					# del dates[1]
					if total:
						del total[0]
						total.append(item["mayor"]["count"])
					if people:
						del people[0]
						try:
							people.append(item["mayor"]["user"]["id"])
						except:
							continue

					num_locais = math.floor(janela/30)

					del mayors[:]
					# Pegar variaveis P e R para formula de cada local
					for i, v in enumerate(people):
						try:
							if i % num_locais == 0:
								#print("lista[%s] = %s" % (i, v))
								mayors.append(v)
						except:
							continue
					print(mayors)

					reapPrefs = calc_reaparicao(mayors)
					trocaPrefs = len(list(set(mayors)))
					# resultTroca = round(trocaPrefs * (math.log( sum(total)+1 )),2)
					resultTroca = round(reapPrefs * (math.log( sum(total)+1 )),2)

					if resultTroca > resultMax:
						resultMax = resultTroca
						dateMax = str(dates[0]) +' - '+ str(dates[-1])
						trocaMax = trocaPrefs
						reapMax = reapPrefs	
			else:
				continue
		try:
			if trocaMax > 1:
				results.append([resultMax, cat, dateMax, trocaMax, reapMax])

		except:
			continue	


print("-------------------")
print("RESULTADOS")
print("-------------------")
results.sort(reverse=True)

for res in results:
	# print(res[])
	print(res[1]) # Categoria
	print( "P = " + str( res[3]) ) # quantidade de trocas
	print( "X1: " + str(res[0]) ) # ResultMax - numero maximo para o periodo calculado
	print( res[2] ) # data do periodo
	print( "R = " + str(res[4]) ) # numero de reaparicoes
	print("-------------------")

					# FAZER O MESMO PARA OS DEMAIS LOCAIS ---------------



					# Calculo para categoria em geral
					# for indice, valor in enumerate(people):
					# 	print("lista[%s] = %s" % (indice, valor))
					
					# print("Data fim: " + str(data_fim))
					# print("total - " + str(total))
					# print("janela - " + str(janela))
					# break
		

		# print(nome_categ + ' - '+ str(count))
		
		# if nome_categ in categories_count.keys():
		# 	categories_count[nome_categ] += count
		# else:
		# 	categories_count[nome_categ] = count

		# categories.append(nome_categ)
		# people.append(item["mayor"]["count"])
		# people.append(item["mayor"][0]["user"]["gender"])

	# print(categories_count)

	# ordened = {}
	# for item in sorted(categories_count, key = categories_count.get):	
	# 	total += categories_count[item]
	# 	ordened[item] = categories_count[item]
	# 	print(item + ' - '+ str(categories_count[item]))










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



	
# 		x.append(item)
# 		y.append(categories_count[item])

		
# plt.plot(x, y)
# plt.title('Grafico Curitiba')
# plt.ylabel("Media")
# plt.xlabel("Cidade")
# plt.xticks(x, rotation='vertical') # Imprimir eixo x na vertical
# wm = plt.get_current_fig_manager() # Para imprimir em tela cheia
# wm.window.state('zoomed') # Tipo da saida do grafico
# plt.show()





