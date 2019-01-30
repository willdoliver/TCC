#-*- coding: utf-8 -*-
from datetime import date
import re
import os
import smtplib

today = str(date.today())

#info para email
destinatario = 'william@alunos.utfpr.edu.br'
texto = 'Teste de Crawler '

#logando no email
remetente = 'william@alunos.utfpr.edu.br'
senha = 'Fzr07br!'
#mensagem do corpo do email
msg = '\r\n'.join([
    '%s' % texto + ' - ' + str(today)
    ])

#enviando email
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(remetente,senha)
server.sendmail(remetente,destinatario,msg)
server.quit()
