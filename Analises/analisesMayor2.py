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

nome_local = []
results = []
# results.append([])
resultCats = []


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

def calc_reaparicao(mayor):
	size = len(mayor)
	resultado = 0
	#print(mayor)

	if size < 2 :
		return 0

	# Percorre lista de prefeitos
	for info,value in enumerate(mayor):
		current = mayor[info]

		aux = 0
		while (aux <= size-2):
			try:
				# print(current +' - '+ mayor[aux+2])
				if ( current != mayor[info+1] and current in mayor):
					resultado += 1
					aux += 1
					del mayor[0]
					continue
				aux += 1
			except:
				return resultado

	return resultado

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

		qtde_locais = 0
		categorias = []
		
		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)
		control = 0

		print("Analisando JSON...")
		# Para cada local distinto
		for loc in nome_local:

			resultMax = 0
			trocaMax = 0
			reapMax = 0
			trocaPrefs = 0
			mayors = []
			total = []
			people = []


			for item in o["all"]:
				# Para cada local do JSON que for do local em questao
				if loc == item["nomeLocal"]:
										
					# List com todos os check-ins
					total.append(item["mayor"]["count"])
					try:
						# Todos os prefeitos
						people.append(item["mayor"]["user"]["id"])
					except:
						continue

					# Calcula reaparicao
					reapPrefs = calc_reaparicao(people)
					# Numero de prefeitos diferentes
					trocaPrefs = len(list(set(people)))

					# Comparacao para pegar o maior numero de trocas
					if trocaPrefs > trocaMax:
						reapMax = reapPrefs
						trocaMax = trocaPrefs

					# salvar em estrutura diferente
					# ([categorias][check-ins, qtde_locais])
						
					# Calculo de P e R
					trocas = round(trocaMax * (math.log( sum(total)+1 )),2)
					disputa = round(reapMax * (math.log( sum(total)+1 )),2)					

				else:
					continue
			if trocaPrefs > 0:
				# Lista de saida para locais
				results.append([trocaMax, trocas, loc, disputa, reapMax, sum(total), item["categories"][0]["name"]])
				# resultCats.append([qtde_locais, categorias, sum(total)])
		control += 1
		print(control)

	arq = open(arqSaida+'.txt', 'w')
	print("Escrevendo saida arquivo: "+ arqSaida+'.txt')
	arq.write("-------------------")
	arq.write("\n")
	arq.write("RESULTADOS")
	arq.write("\n")
	arq.write("-------------------")
	arq.write("\n")
	results.sort(reverse=True)

	for res in results:
		# arq.write(res[])
		try:
			arq.write(str(res[2]) + ' - ' + str(res[6])) # Local
			arq.write("\n")
			arq.write( "P = " + str( res[1]) ) # quantidade de trocas
			arq.write("\n")
			arq.write( "Trocas: " + str(res[3]) ) # Calculo da formula para P
			arq.write("\n")
			arq.write( "R = " + str(res[0]) ) # quantidade de reaparicoes
			arq.write("\n")
			arq.write( "Disputa: " + str(res[4]) ) # Calculo da formula para R
			arq.write("\n")
			arq.write( "Check-ins = " + str(res[5]) ) # numero de reaparicoes
			arq.write("\n")
			arq.write("-------------------")
			arq.write("\n")
		except:
			pass
	arq.close()

	# arqCat = open(arqSaida+'Cat.txt', 'w')
	# print("Escrevendo saida arquivo: "+ arqSaida+'Cat.txt')
	# arqCat.write("-------------------")
	# arqCat.write("\n")
	# arqCat.write("RESULTADOS")
	# arqCat.write("\n")
	# arqCat.write("-------------------")
	# arqCat.write("\n")
	# results.sort(reverse=True)

	# for res in resultCats:
	# 	try:
	# 		arqCat.write(res[1]) # Categoria
	# 		arqCat.write("\n")
	# 		arqCat.write( "Qtde Locais = " + str( res[0]) ) # quantidade de locais da categoria
	# 		arqCat.write("\n")
	# 		arqCat.write( "Total Check-ins = " + str(res[3]) ) # Calculo da formula para P
	# 		arqCat.write("\n")
	# 		arqCat.write( "Media = " + str(res[2]) ) # quantidade de reaparicoes
	# 		arqCat.write("\n")
	# 		arqCat.write("-------------------")
	# 		arqCat.write("\n")
	# 	except:
	# 		pass
	# arqCat.close()
	# print(categorias)
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





