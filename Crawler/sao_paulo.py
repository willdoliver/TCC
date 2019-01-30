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
texto = 'Crawler de Sao Paulo '

params5 = dict(
  client_id='T5H1DGJAVQPKQNPHKSEYXVXRFQGZRMLCLBC5X0KXQKN2XHFZ',
  client_secret='4DEZN2E4HPDZAKYJG2T3ATH3LQKEEPAIPVPQ1WEIDT4BAK11',
  v='20180323',
  limit=1
)

client = MongoClient()
db = client.sao_paulo

today = str(date.today())
date = {'data consulta':today}

arq = open('/home/sda3/william/id_sao_paulo.txt','r')
#arq = open('id_sao_paulo.txt','r')
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
			resp = requests.get(url=url, params=params5)
		except:
			try:
				time.sleep(21)
				resp = requests.get(url=url, params=params5)
			except:
				#print ('Erro de Request')
				pass
	
	try:
		data = json.loads(resp.text)
		data.update(date)
		http_code = data['meta']['code']
		if http_code == 200:
			sucess += 1
			posts = db.sao_paulo
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
