# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import json
from pprint import pprint

#######################################################################################
################################    M A I N    ########################################
#######################################################################################

json_data = open('1.json').read()
print(json_data)
json_novo = json.loads(json_data)
print(json_novo)

exit(0)
json_file = open('curitibaV1.json', 'r')
for line in json_file.readlines():
	j = json.load(line)
	data = j['data consulta']
	#mayor = j['response']['mayor']['user']['firstName']

	print(data)
	#print(mayor)
	exit(0)
	#print(row)
#	x.append(row[0])
#	y.append(row[1])
#		
#plt.plot(x, y)
#plt.title('Grafico Curitiba')
#plt.ylabel("Media")
#plt.xlabel("Cidade")
#plt.xticks(x, rotation='vertical') # Imprimir eixo x na vertical
#wm = plt.get_current_fig_manager() # Para imprimir em tela cheia
#wm.window.state('zoomed') # Tipo da saida do grafico
#plt.show()




