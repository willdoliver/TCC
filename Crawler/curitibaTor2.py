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

from TorCrawler import TorCrawler
import os
import commands

from fake_useragent import UserAgent


params1 = dict(
  client_id='JPPSFUBOFCATOBDMFZC013CMEVMJTYOPEPJ3AXHRASYB320A',
  client_secret='KFOZHELXV3AJLPKENB1PCNSHJUZASJ3SDX13YW4NVZRVOBU4',
  v='20170801',
  limit=1
)

params2 = dict(
  client_id='J2WIR1ZG0PJKYJNSCQRA2EM55DIY1CV0HWFBIL2Y5OP2QNJV',
  client_secret='NXEBSQVV4XT24MZ0J3SGV4N35S0WKO22YHJ1DOT14D4F02M1',
  v='20180323',
  limit=1
)

params3 = dict(
  client_id='W3SIDQWLHWCWUZQG2EZ4FN5LXYDTACLNFX4JITNIBBUHRNSB',
  client_secret='MGPZLD1SDNCTTMQRRFCY0RFD4VOTQ5LQDIYIC2XFBXDYUPXR',
  v='20170801',
  limit=1
)

params4 = dict(
  client_id='ABCVRVTNTZ1NRRC0MA135PCVWVFNSUXGZCGIXBZ4PX2AEFML',
  client_secret='SOY50432MXCT0YLYAFNDTPUFFP2ICD1HZN2OSUQ1H5FBWEUN',
  v='20180323',
  limit=1
)

params5 = dict(
  client_id='W3K2WFYXXNW5DZIIOSQHOAGS4WVGHEQILLZMK10KKQ0Q3H4A',
  client_secret='0O52YL2LI4ZZVTV1EJ1NRUIXTU35LYN24DUSU2PSVRQFJE3W',
  v='20180323',
  limit=1
)

params6 = dict(
  client_id='T5H1DGJAVQPKQNPHKSEYXVXRFQGZRMLCLBC5X0KXQKN2XHFZ',
  client_secret='4DEZN2E4HPDZAKYJG2T3ATH3LQKEEPAIPVPQ1WEIDT4BAK11',
  v='20180323',
  limit=1
)

vetParams = [params3, params2, params1, params4, params5, params6]

crawler = TorCrawler()
#client = MongoClient()
#db = client.curitiba
today = str(date.today())
date = {'data consulta':today}

def verificaLastID():
	try:
		opened = open('lastIDCuritiba.txt', 'r')
		id_saved = opened.readline()
		return id_saved
	except:
		return 1


#sleep randomico
def sleep():
	t1 = random.randint(1,20)
	if t1 == 10:
		print ('sleep = 10')
		time.sleep(30)
	#sleep para cada iteracao
	t2 = random.randint(10,30)
	print ('sleep = '+ str(t2))
	#time.sleep(t2)


def sendEmail(today, qtde):
	destinatario = 'william@alunos.utfpr.edu.br'
	texto = 'Crawler de Curitiba '

	#logando no email
	remetente = 'william@alunos.utfpr.edu.br'
	senha = 'Fzr07br!'
	#mensagem do corpo do email
	msg = '\r\n'.join([
	    '%s' % texto + str(today) + str(qtde)])
	#enviando email
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(remetente,senha)
	server.sendmail(remetente,destinatario,msg)
	server.quit()

#ua = UserAgent()
def getURL(url):
	resp = ''

	while resp == '':
		try:
			#headers = {'User-Agent': ua.random}
			print(crawler.ip)
			os.system("/etc/init.d/tor restart")
			#crawler.rotate()
			print('IP ROTETED')
			print(crawler.ip)
			exit(0)
			resp = crawler.get(url=url, params=vetParams[0])
			data = json.loads(resp.text)
	    	
			http_code = data['meta']['code']
			print(url + ' - ' +str(http_code))
			if http_code != 200:
				#headers = {'User-Agent': ua.random}
				#print(crawler.ip)
				del vetParams[0]
				#continue
			else:
				return data
		except:
			continue


def main():

	#arq = open('/home/sda3/william/id_curitiba.txt','r')
	arq = open('id_curitiba.txt','r')
	sucess = 0
	#percorre o arquivo linha por linha e separa por virgula cat,url
	pulou = 0
	for i in arq.readlines():
		#se categoria = termo inserido na entrada
		words = i.split('	')
		id_place = words[0]

		data = getURL('https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm')

		continue

		try:
			data.update(date)
			sucess += 1
		except:
			try:
				# Para nao perder o id que deu erro 429
				data = getURL('https://api.foursquare.com/v2/venues/' + id_place + '?m=swarm')
				data.update(date)
				sucess += 1
			except:
				#print ('Erro na requisicao, nao inserido no banco')
				pass

		#try:
		#	posts = db.curitiba
		#	post_id = posts.insert_one(data).inserted_id
		#except:
		#	print ('Erro ao inserir no banco')

		#sleep()
		print(sucess)
	sendEmail(today, sucess)




if __name__ == '__main__':
    main()
