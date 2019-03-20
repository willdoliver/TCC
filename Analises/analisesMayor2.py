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
	resultado = 0
	#print(mayor)

	if size < 2 :
		return 0


	for info,value in enumerate(mayor):
		current = mayor[info]

		aux = 0
		while (aux <= size-2):
			# print( str(aux) +' <> '+ str(size) )
			try:
				# print(current +' - '+ mayor[aux+2])
				if (current == mayor[aux+2] and current != mayor[aux+1]):
					# print( "resultado: " + str(resultado) )
					resultado += 1
					aux += 1
					del mayor[0]
					continue
				aux += 1
			except:
				return resultado

	return resultado

def analisaDados(arqAnalise,arqSaida):
	# Loop para coletar categorias unicas
	with open('Req200/'+arqAnalise, 'r') as f:
		print("Analisando categorias...")
		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)

		nome_categ = []
		for i in o["all"]:
			nome_categ.append(i["categories"][0]["name"])
		nome_categ = remove_repetidos(nome_categ)
		# print(nome_categ)

	with open('Req200/'+arqAnalise, 'r') as f:

		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)

		print("Analisando JSON...")
		for cat in nome_categ:

			qtd_dias = 0
			resultMax = 0
			trocaMax = 0
			reapMax = 0
			mayors = []
			total = []
			people = []
			nome_local = []
			locais = 0

			for item in o["all"]:
				# if cat == "Shopping Mall" and item["categories"][0]["name"] == "Shopping Mall":
				if cat == item["categories"][0]["name"]:
					if item["nomeLocal"] not in nome_local:
						nome_local.append(item["nomeLocal"])
						locais += 1
					# NAO TEM COMO CALCULAR P E R PARA CATEGORIAS NO GERAL, PREFEITOS NAO SERAO OS MESMOS PRA LOCAIS DISTINTOS
					total.append(item["mayor"]["count"])
					try:
						people.append(item["mayor"]["user"]["id"])
					except:
						continue

					for i, v in enumerate(people):
						try:
							#print("lista[%s] = %s" % (i, v))
							mayors.append(v)
						except:
							continue

					reapPrefs = calc_reaparicao(people)
					trocaPrefs = len(list(set(people)))

					checkins = round(sum(total)/locais ,2)
						
					trocas = round(trocaPrefs * (math.log( checkins+1 )),2)
					disputa = round(reapPrefs * (math.log( checkins+1 )),2)

				else:
					continue
			if trocaPrefs > 0:
				results.append([locais, trocas, cat, trocaPrefs, disputa, reapPrefs, checkins])
			

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
			arq.write(res[2]) # Categoria
			arq.write("\n")
			# arq.write( "P = " + str( res[2]) ) # quantidade de trocas
			# arq.write("\n")
			arq.write( "Check-ins = " + str( res[6]) ) # quantidade de check-ins por categoria
			arq.write("\n")
			# arq.write( "Trocas: " + str(res[0]) ) # ResultMax - numero maximo para o periodo calculado
			# arq.write("\n")
			# arq.write( "Disputa: " + str(res[3]) )
			# arq.write("\n")
			# arq.write( "R = " + str(res[4]) ) # numero de reaparicoes
			# arq.write("\n")
			arq.write( "Num locais = " + str(res[0]) ) # numero de reaparicoes
			arq.write("\n")
			arq.write("-------------------")
			arq.write("\n")
		except:
			pass
	arq.close()
	print("Fim arquivo " + arqAnalise + '\n\n')



def main():

	analisaDados('curitibaWithName.json', 'CWB_resultado')
	# analisaDados('chicagoWithName.json', 'CHICAGO_resOrderBy')
	# analisaDados('spShort.json', 'SP_resOrderBy')
	

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





