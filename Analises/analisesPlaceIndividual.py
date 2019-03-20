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
name_place = []
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

def analisaDados(arqAnalise,varChoosed,arqSaida):
	# Loop para coletar categorias unicas
	with open('Req200/'+arqAnalise, 'r') as f:
		print("Analisando locais..")
		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)

		name_place = []
		for i in o["all"]:
			name_place.append(i["nomeLocal"])
		name_place = remove_repetidos(name_place)
		# print(name_place)

	with open('Req200/'+arqAnalise, 'r') as f:

		data = json.load(f)
		n = json.dumps(data)
		o = json.loads(n)


		print("Analisando JSON...")
		for cat in name_place:
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
				# print(cat)
				# print(item["nomeLocal"])
				# exit(0)
				if cat == item["nomeLocal"]:

					
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
						#print(mayors)

						reapPrefs = calc_reaparicao(mayors)
						trocaPrefs = len(list(set(mayors)))
						
						if varChoosed == 'P':
							resultTroca = round(trocaPrefs * (math.log( sum(total)+1 )),2)
						if varChoosed == 'R':
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

	arq = open(arqSaida+varChoosed+'.txt', 'w')
	print("Escrevendo saida arquivo: "+ arqSaida+varChoosed+'.txt')
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
			arq.write(res[1]) # Categoria
			arq.write("\n")
			arq.write( "P = " + str( res[3]) ) # quantidade de trocas
			arq.write("\n")
			if (varChoosed == 'P'):
				arq.write( "Trocas: " + str(res[0]) ) # ResultMax - numero maximo para o periodo calculado
			if (varChoosed == 'R'):
				arq.write( "Disputa: " + str(res[0]) ) # ResultMax - numero maximo para o periodo calculado
			arq.write("\n")
			arq.write( res[2] ) # data do periodo
			arq.write("\n")
			arq.write( "R = " + str(res[4]) ) # numero de reaparicoes
			arq.write("\n")
			arq.write("-------------------")
			arq.write("\n")
		except:
			pass
	arq.close()
	print("Fim arquivo " + arqAnalise + '\n\n')



def main():

	# analisaDados('curitibaWithName.json','P', 'CWB_Locais')
	# analisaDados('curitibaWithName.json','R', 'CWB_Locais')

	# analisaDados('saoPauloWithName.json','P', 'SP_Locais')
	# analisaDados('saoPauloWithName.json','R', 'SP_Locais')

	# analisaDados('chicagoWithName.json','P', 'CHICAGO_Locais')
	analisaDados('chicagoWithName.json','R', 'CHICAGO_Locais')
	

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





