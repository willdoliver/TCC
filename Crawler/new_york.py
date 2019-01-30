#-*- coding: utf-8 -*-
import json
import requests
import pymongo
from pymongo import MongoClient
import time
from datetime import date
import re
import os
import random
import smtplib

#info para email
destinatario = 'william@alunos.utfpr.edu.br'
texto = 'Crawler de New York '

params4 = dict(
  client_id='W3K2WFYXXNW5DZIIOSQHOAGS4WVGHEQILLZMK10KKQ0Q3H4A',
  client_secret='0O52YL2LI4ZZVTV1EJ1NRUIXTU35LYN24DUSU2PSVRQFJE3W',
  v='20180323',
  limit=1
)

client = MongoClient()
db = client.new_york

today = str(date.today())
date = {'data consulta':today}

arq = open('/home/sda3/william/id_new_york.txt','r')
#arq = open('id_new_york.txt','r')
sucess = 0

for i in arq.readlines():
	#se categoria = termo inserido na entrada
	words = i.split('	')
	id_place = words[0]
	url = 'https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm'
	#print (url)
	
	resp = ''
	while resp == '':
		try:
			resp = requests.get(url=url, params=params4)
		except:
			try:
				time.sleep(21)
				resp = requests.get(url=url, params=params4)
			except:
				#print ('Erro de Request')
				pass
	
	try:
		data = json.loads(resp.text)
		data.update(date)
		http_code = data['meta']['code']
		if http_code == 200:
			sucess += 1
			posts = db.new_york
			#post_id = posts.insert_one(data).inserted_id
		else:
			break
	except:
		#print ('Erro na requisicao, nao inserido no banco')
		pass

	#sleep para cada iteracao
	sleep1 = random.randint(10,30)
	sleep2 = random.randint(1,4)
	#print ('sleep = '+ str(sleep1*sleep2))
	time.sleep(sleep1*sleep2)

#logando no email
remetente = 'william@alunos.utfpr.edu.br'
senha = 'Fzr07br!'
#mensagem do corpo do email
msg = '\r\n'.join([
    '%s' % texto + str(sucess) + ' - ' + today
    ])

#enviando email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(remetente,senha)
server.sendmail(remetente,destinatario,msg)
server.quit()
