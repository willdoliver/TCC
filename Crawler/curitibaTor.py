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

import requests
from TorCrawler import TorCrawler
import os
import commands
import time

from TorCrawler import TorCrawler

#info para email
destinatario = 'william@alunos.utfpr.edu.br'
texto = 'Crawler de Curitiba '

params = dict(
  client_id='J2WIR1ZG0PJKYJNSCQRA2EM55DIY1CV0HWFBIL2Y5OP2QNJV',
  client_secret='NXEBSQVV4XT24MZ0J3SGV4N35S0WKO22YHJ1DOT14D4F02M1',
  v='20180323',
  limit=1
)


def verificaLastID():
	try:
		opened = open('lastIDCuritiba.txt', 'r')
		id_saved = opened.readline()
		return id_saved
	except:
		return 1

def getURL(url):
	print(url)
	http_code = ''	
	resp = ''
	while resp == '':
		try:
			resp = requests.get(url=url, params=params)
			data = json.loads(resp.text)
			http_code = data['meta']['code']
			print(http_code)
			if http_code != 200:
				os.system("/etc/init.d/tor restart")
				i += 1
			else:
				return data
			return resp
		except:
			time.sleep(5)
			continue


crawler = TorCrawler()
os.system("/etc/init.d/tor restart")
print(crawler.ip)
#client = MongoClient()
#db = client.curitiba

today = str(date.today())
date = {'data consulta':today}

def main():
	skipped = []
	once = 0
	#arq = open('/home/sda3/william/id_curitiba.txt','r')
	arq = open('id_curitiba.txt','r')
	sucess = 0
	#percorre o arquivo linha por linha e separa por virgula cat,url
	pulou = 0
	for i in arq.readlines():
		#se categoria = termo inserido na entrada
		words = i.split('	')
		id_place = words[0]

		# Continua a partir do ultimo id da execucao anterior, quando recebeu o 429
		cont = verificaLastID()

		if cont != 1:
			while cont != id_place:
				pulou += 1
				print(id_place)
				skipped.append(id_place)
				break
			if cont == id_place:
				os.system("rm lastIDCuritiba.txt")
				cont = 1
				pass
			else:	
				continue

		#print(skipped)
		#print(len(skipped))

		resp = getURL('https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm')
		try:
			data = json.loads(resp.text)
			data.update(date)
			http_code = data['meta']['code']
			if http_code == 200:
				sucess += 1
				#posts = db.curitiba
				#post_id = posts.insert_one(data).inserted_id
			else:
				print(http_code)
				#os.system("/etc/init.d/tor restart")
				file = open('lastIDCuritiba.txt', 'w')
				file.write(id_place)
				file.close()
				exit(0)

		except:
			#print ('Erro na requisicao, nao inserido no banco')
			pass

		
		try:
			data = json.loads(resp.text)
			data.update(date)
		except:
			data = ''
		
		#try:
		#	posts = db.curitiba
		#	post_id = posts.insert_one(data).inserted_id
		#except:
		#	print ('Erro ao inserir no banco')

		#sleep randomico
		aux2 = random.randint(1,20)
		if aux2 == 10:
			print ('sleep = 10')
			time.sleep(30)
		#sleep para cada iteracao
		aux = random.randint(10,30)
		print ('sleep = '+ str(aux))
		#time.sleep(aux)
		print(sucess)

	##logando no email
	#remetente = 'william@alunos.utfpr.edu.br'
	#senha = 'Fzr07br!'
	##mensagem do corpo do email
	#msg = '\r\n'.join([
	#    '%s' % texto + ' ' + today,
	#    '%s' % id_place
	#    ])
	##enviando email
	#server = smtplib.SMTP('smtp.gmail.com:587')
	#server.starttls()
	#server.login(remetente,senha)
	#server.sendmail(remetente,destinatario,msg)
	#server.quit()


if __name__ == '__main__':
    main()
