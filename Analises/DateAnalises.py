# -*- coding: utf-8 -*-
#import matplotlib.pyplot as plt
import os
import json
from pprint import pprint

#######################################################################################
################################    M A I N    ########################################
#######################################################################################


datas = {}
fileNY = open('Req200/new_york.txt', 'r')
fileCWB = open('Req200/curitiba.txt', 'r')
fileCH = open('Req200/chicago.txt', 'r')
fileSP = open('Req200/sao_paulo.txt', 'r')
fileTK = open('Req200/tokyo.txt', 'r')

for line in fileTK.readlines():
	n = json.dumps(line)
	o = json.loads(n)
	#print(o)
	#print(type(o))
	if (o[21:31] in datas):
		datas[o[21:31]] += 1
	else:
		datas[o[21:31]] = 1


print(datas)
print(len(datas))





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




