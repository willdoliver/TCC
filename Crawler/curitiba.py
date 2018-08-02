#-*- coding: utf-8 -*-
import json
import requests
import pymongo
from pymongo import MongoClient

import time
from datetime import date
import re
import random
import smtplib

#info para email
destinatario = 'william@alunos.utfpr.edu.br'
texto = 'Sucesso na execucao do Crawler de Curitiba'

params = dict(
  client_id='JPPSFUBOFCATOBDMFZC013CMEVMJTYOPEPJ3AXHRASYB320A',
  client_secret='KFOZHELXV3AJLPKENB1PCNSHJUZASJ3SDX13YW4NVZRVOBU4',
  v='20170801',
  #ll='-25.5662655951,-49.3168304175',
  #query='coffee',
  limit=1
)


client = MongoClient()
db = client.curitiba
ini = time.time()
today = str(date.today())

arq = open('/home/sda3/william/id_curitiba.txt','r')
requests_num = 0
#percorre o arquivo linha por linha e separa por virgula cat,url
for i in arq.readlines():
	#se categoria = termo inserido na entrada
	words = i.split('	')
	id_place = words[0]

	#print id_place
	url = 'https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm'
	print url
	break
	
	limit = 0
	resp = ''
	while resp == '':
		try:
			resp = requests.get(url=url, params=params)
			requests_num += 1
		except:
			print ('Erro de Request')
			time.sleep(15)

	try:
		print (requests_num)
		#print (id_place)
	except:
		print  ('\n pulou \n')
	
	date = {'data consulta':today}
	
	try:
		data = json.loads(resp.text)
		data.update(date)
	except:
		data = ''
	
	try:
		posts = db.curitiba
		post_id = posts.insert_one(data).inserted_id
	except:
		print ('Erro ao inserir no banco')

	#sleep randomico
	aux2 = random.randint(1,20)
	if aux2 == 10:
		print ('sleep rand = 10')
		time.sleep(30)
	#sleep para cada iteracao
	aux = random.randint(10,30)
	print ('sleep = ', aux, '\n')
	time.sleep(aux)

fim = time.time()

#logando no email
remetente = 'william@alunos.utfpr.edu.br'
senha = 'Fzr07br!'
#mensagem do corpo do email
msg = '\r\n'.join([
    '%s' % texto + ' ' + today,
    '%s' % id_place
    ])
#enviando email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(remetente,senha)
server.sendmail(remetente,destinatario,msg)
server.quit()
