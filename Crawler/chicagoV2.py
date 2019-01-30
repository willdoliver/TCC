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


# local =====>> sda3/william
# scp Desktop/2018.2/TCC2/Crawler/chicagoV2.py william@200.134.10.26:/home/sda3/william

#info para email
destinatario = 'william@alunos.utfpr.edu.br'
texto = 'Crawler de Chicago '


params = dict(
  client_id='LQJBCDWICJ1WYMC20DTHBLVTGCMJBQBFPS2CJHUOWNPP4A5E',
  client_secret='XSLGVMTFDNMJHEQHYNCOAVDO3IPLFHKRXJCFO1CBGU35RWDP',
  v='20180323',
  limit=1
)


client = MongoClient()
db = client.chicago

today = str(date.today())
date = {'data consulta':today}

arq = open('/home/sda3/william/id_chicago.txt','r')
#arq = open('id_chicago.txt','r')
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
			resp = requests.get(url=url, params=params)
		except:
			#print ('Erro de Request')
			pass
	
	try:
		data = json.loads(resp.text)
		data.update(date)
		http_code = data['meta']['code']
		if http_code == 200:
			sucess += 1
			posts = db.chicago
			post_id = posts.insert_one(data).inserted_id
		else:
			break
	except:
		print ('Nao inserido no banco')
		pass

	#sleep para cada iteracao
	sleep = random.randint(2,20)
	print ('sleep = '+ str(sleep) + ' sucess = ' + str(sucess))
	time.sleep(sleep)

#logando no email
remetente = 'william@alunos.utfpr.edu.br'
senha = 'Fzr07br!'

#mensagem do corpo do email
msg = '\r\n'.join([
    '%s' % texto + str(sucess) + ' - ' + str(today)
    ])

#enviando email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(remetente,senha)
server.sendmail(remetente,destinatario,msg)
server.quit()
