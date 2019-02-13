# -*- coding: utf-8 -*-
#import matplotlib.pyplot as plt
import os
import re
import json
from pprint import pprint

#######################################################################################
################################    M A I N    ########################################
#######################################################################################

# Curitiba OK
# NY OK
# Chicago OK
# SP OK
# Tokyo


saver = open("nyShort.json", "w")
file = open('new_york.txt', 'r')

saver.write('{"all":[')
saver.write("\n")

aux = 0
for tudo in file.readlines():
	try:

		data = re.search(r"({u'data consulta':\D+\d+-\d+-\d+')", tudo).groups()
		data = ''.join(data[0])
		data = data+","

		data = data.replace("u'", '"')
		data = data.replace("':", '":')
		data = data.replace("',", '",')
		#print(data)

		try:
			mayor = re.search(r"u'mayor[\W\w].*?}{2}", tudo).group()

			mayor = mayor.replace("u'", '"')
			mayor = mayor.replace("':", '":')
			mayor = mayor.replace("',", '",')
			mayor = mayor.replace("'}", '"}')
			mayor = mayor.replace(".jpg'", '.jpg"')
			mayor = mayor.replace("False", '0')
			mayor = mayor.replace("True", '1')
			mayor = mayor.replace('u"Doctor\'s Offices"', '"Doctors Offices"')
			mayor = mayor.replace('u"Doctor\'s Office"', '"Doctors Office"')
			mayor = mayor.replace('\xe9', 'e')
			mayor = mayor.replace('\xdc', 'l')
			mayor = mayor.replace('\U0001f637', 'Ken')
			mayor = mayor.replace('\xe1', 'e')
			mayor = mayor.replace('\xfa', 'a')
			mayor = mayor.replace('\xe3', 'a')
			mayor = mayor.replace(' \u2705', '')
			mayor = mayor.replace('\xfc', 'a')
			mayor = mayor.replace('\xe7', 'c')
			mayor = mayor.replace('u"Women\'s Stores"', '"Womens Stores"')
			mayor = mayor.replace('u"Women\'s Store"', '"Womens Store"')
			mayor = mayor.replace('u"Dentist\'s Offices"', '"Dentists Offices"')
			mayor = mayor.replace('u"Dentist\'s Office"', '"Dentists Office"')
			mayor = mayor.replace('u"O\'Connor"', '"OConnor"')
			mayor = mayor.replace('u"O\'Keefe"', '"OKeefe"')
			mayor = mayor + "}"
			#print(mayor)
		except:
			mayor = '"mayor": {"count": 0, "user": 0}'

		category = re.search(r"u'categories[\W\w].*?}{2}", tudo).group()
		category = category.replace("u'", '"')
		category = category.replace("':", '":')
		category = category.replace("',", '",')
		category = category.replace("False", '0')
		category = category.replace("True", '1')
		category = category.replace(".png'", '.png"')
		category = category.replace('"categories": []', '"categories": [{')
		category = category + "]" + "}"
		#print(category)

		json = data + mayor + "," + category + ","
		
		saver.write(json)
		saver.write("\n")
		
		print(aux)
		aux +=1
	except:
		pass



saver.write(']}')



# "######## DATA ########"

# 	({u'data consulta':\D+\d+-\d+-\d+')


# u' => "
# ': => ":
# ', => "


# "######## MAYOR ########"

# 	u'mayor[\W\w].*?}{2}


# u' => "
# ': => ":
# ', => ",
# .jpg' => .jpg"

# acrescentar 2x } fim do arquivo