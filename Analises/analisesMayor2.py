# -*- coding: utf-8 -*-
import os,re,sys
import json
import math
from pprint import pprint
from datetime import datetime
import matplotlib as mpl 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import sem, t
from scipy import mean
mpl.use('agg')


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
confidence = 0.05

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
		arq.write("Local,Categoria,P,Trocas,R,Disputa,Check-ins")
		arq.write("\n")
		saida.sort(reverse=True)

		for s in saida:
			if s[2].encode('utf-8') == "Canonicalurl': U'Https:":
				continue
			# print(s)
			arq.write(str(s[2].encode('utf-8')) + ',' + str(s[6])) # Local - Categoria
			arq.write(",")
			arq.write(str(s[1]) ) # Quantidade de trocas
			arq.write(",")
			arq.write(str(s[0]) ) # Calculo da formula para P
			arq.write(",")
			arq.write(str(s[4]) ) # Quantidade de reaparicoes
			arq.write(",")
			arq.write(str(s[3]) ) # Calculo da formula para R
			arq.write(",")
			arq.write(str(s[5]) ) # Soma check-ins
			arq.write(",")
			arq.write("\n")

		arq.close()
		
		resultCats.sort()
		
		# print(resultCats)
		# exit(0)
		
		# vetor auxiliar com categorias unicas
		res = []
		for r in resultCats:
			res.append(r[0])
		res = remove_repetidos(res)
		
		checkinsCat=[]
		data_to_plot=[]
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

			n = len(agrupCat) 		# Tamanho Lista
			m = mean(agrupCat) 		# Mediana
			std_err = sem(agrupCat) # Erro
			h = std_err * t.ppf((1 + confidence) / 2, n - 1) # Desvio
			# print(str(r) + ' - ' + str(agrupCat) + ' - len:' + str(n))

			start = m - h
			end = m + h

			if (math.isnan(h)):
				continue

			data_to_plot.append([
				m, # Media Checkins
				agrupCat,
				r
			])

			checkinsCat.append([
				pd.Series(agrupTrocas).median(),
				pd.Series(agrupReap).median(),
				pd.Series(agrupCat).mean(),
				r,
				start,
				end
			])
		# print(data_to_plot)
		# exit(0)

		data_to_plot.sort(reverse=True)
		
		# arqBox = open('Curitiba_boxPlot.txt', 'w')
		arqBox = open('Chicago_boxPlot.txt', 'w')
		
		data_to_plot2=[]
		data_cat=[]
		aux = 0
		for data in data_to_plot:
			if (aux == 50):
				break
			arqBox.write(data[2]) # categoria 
			arqBox.write(',')
			arqBox.write(str(round(data[0],2))) # media check-ins
			arqBox.write(',')
			arqBox.write(str(data[1])) #lista com check-ins
			arqBox.write('\n')
			aux += 1

			data_to_plot2.append([data[2],data[1]])

		arqBox.close()
		
		data_to_plot3=[]
		data_to_plot2.sort()
		for d in data_to_plot2:
			data_cat.append(d[0])
			data_to_plot3.append([d[1]])

		# Create a figure instance
		fig = plt.figure(1, figsize=(20, 10))

		# Create an axes instance
		ax = fig.add_subplot(111)

		# Save the figure
		bp = ax.boxplot(data_to_plot3, patch_artist=True)

		## Custom x-axis labels
		ax.set_xticklabels(data_cat,rotation=90)
		ax.set_ylabel('Quantidade de check-ins',rotation=90)

		width = 2
		# Configuracao de cores
		for box in bp['boxes']:
		    box.set( color='#5a5b5b', linewidth=width)
		    box.set( facecolor = '#3f30ff' )

		for whisker in bp['whiskers']:
		    whisker.set(color='#171626', linewidth=width)

		for cap in bp['caps']:
		    cap.set(color='#171626', linewidth=width)

		for median in bp['medians']:
		    median.set(color='#72b239', linewidth=width)

		for flier in bp['fliers']:
		    flier.set(marker='o', color='#000000', alpha=5)
		# Create the boxplot
		# fig.savefig('Curitiba_boxPlot.png', bbox_inches='tight')
		fig.savefig('Chicago_boxPlot.png', bbox_inches='tight')

		exit(0)

		arqCat.write("Categoria,Media Check-ins,Mediana Trocas,Mediana Disputa")
		arqCat.write("\n")
		
		numCategs = 0
		catsMax = 50
		checkinsCat.sort(reverse=True)

		for cat in checkinsCat:

			if (math.isnan(cat[4])):
				arqCat.write(str(0))
				arqCat.write('	')
				arqCat.write(str(0))
			else:
				arqCat.write(str(round(cat[4],2)).replace(".",","))
				arqCat.write('	')
				arqCat.write(str(round(cat[3],2)).replace(".",","))
			arqCat.write('	')
			arqCat.write(	str(round(cat[2],2)).replace(".",",") ) # media check-ins
			arqCat.write('	')
			arqCat.write(	str(round(cat[0],2)).replace(".",",") ) # Trocas
			arqCat.write('	')
			arqCat.write(str(round(cat[1],2)).replace(".",",") ) # Reap
			arqCat.write('\n')
			numCategs += 1

			if numCategs == catsMax:
				break
	
		arqCat.close()

	print("Fim arquivo " + arqAnalise + '\n\n')


def main():

	# analisaDados('curitibaWithName.json', 'CWB_resultado')
	analisaDados('chicagoWithName.json', 'CHICAGO_resultado')
	# analisaDados('saoPauloWithName.json', 'SP_resultado')
	

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
