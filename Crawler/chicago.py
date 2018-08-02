#-*- coding: utf-8 -*-
import json
import requests
import pymongo
from pymongo import MongoClient
import urllib2
import time
from datetime import date
import re
import random

#https://developer.foursquare.com/docs/api/venues/details

params = dict(
  client_id='JPPSFUBOFCATOBDMFZC013CMEVMJTYOPEPJ3AXHRASYB320A',
  client_secret='KFOZHELXV3AJLPKENB1PCNSHJUZASJ3SDX13YW4NVZRVOBU4',
  v='20170801',
  #ll='-25.5662655951,-49.3168304175',
  #query='coffee',
  limit=1
)
params2 = dict(
  client_id='W3SIDQWLHWCWUZQG2EZ4FN5LXYDTACLNFX4JITNIBBUHRNSB',
  client_secret='MGPZLD1SDNCTTMQRRFCY0RFD4VOTQ5LQDIYIC2XFBXDYUPXR',
  v='20170801',
  limit=1
)


client = MongoClient()
db = client.chicago
#ini = time.time()
today = str(date.today())

arq = open('id_chicago.txt','r')
requests_num = 0
#percorre o arquivo linha por linha e separa por virgula cat,url
for i in arq.readlines():
	#se categoria = termo inserido na entrada
	words = i.split('	')
	id_place = words[0]

	#print id_place
	url = 'https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm'
	#print url

	limit = 0
	resp = ''
	while resp == '':
		try:
			resp = requests.get(url=url, params=params)
			requests_num += 1
		except:
			try:
				resp = requests.get(url=url, params=params2)
				requests_num += 1
				print resp, 'Param2'
			except:
				print 'Erro de Request'
				time.sleep(15)

	try:
		print requests_num
		print id_place
	except:
		print '\n pulou \n'

	date = {'data consulta':today}
	
	try:
		data = json.loads(resp.text)
		data.update(date)
	except:
		data = ''

	try:
		posts = db.chicago
		post_id = posts.insert_one(data).inserted_id
	except:
		print 'Erro ao inserir no banco'

#	#sleep randomico
#	aux2 = random.randint(1,30)
#	if aux2 == 10:
#		print 'sleep rand = 10'
#		time.sleep(20)
#	#sleep para cada iteracao
#	aux = random.randint(7,17)
#	print 'sleep = ', aux, '\n'
#	time.sleep(aux)
print 'Tempo de Execucao', (fim-ini)/60