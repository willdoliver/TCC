from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

import requests
import time
import random

from bs4 import BeautifulSoup

from stem import Signal
from stem.control import Controller

# initialize some
# holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# how many IP addresses
# through which to iterate?
nbrOfIpAddresses = 3

# seconds between
# IP address checks
secondsBetweenChecks = 5

PROXY = "127.0.0.1:8118" # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=/home/saulo/.config/google-chrome/")
#opcao de proxy parece nao estar funcionando, e necessario forcar manualmente o proxy do Chrome via configuracoes do browser
chrome_options.add_argument('--proxy-server=%s' % PROXY)

driver = webdriver.Chrome(chrome_options=chrome_options)

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        #Mudar o password conforme oq foi configurado durante o tutorial
        controller.authenticate(password = 'password1234')
        controller.signal(Signal.NEWNYM)
        controller.close()

def mudar_ip():
    global newIP
    global oldIP

    for i in range(0, nbrOfIpAddresses):

        # if it's the first pass
        if newIP == "0.0.0.0":
            # renew the TOR connection
            renew_connection()
            # obtain the "new" IP address
            newIP = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'}).text.strip()
        # otherwise
        else:
            # remember the
            # "new" IP address
            # as the "old" IP address
            oldIP = newIP
            # refresh the TOR connection
            renew_connection()
            # obtain the "new" IP address
            newIP = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'}).text.strip()

        # zero the 
        # elapsed seconds    
        seconds = 0

        # loop until the "new" IP address
        # is different than the "old" IP address,
        # as it may take the TOR network some
        # time to effect a different IP address
        while oldIP == newIP:
            # sleep this thread
            # for the specified duration
            time.sleep(secondsBetweenChecks)
            # track the elapsed seconds
            seconds += secondsBetweenChecks
            # obtain the current IP address
            newIP = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'}).text.strip()
            # signal that the program is still awaiting a different IP address
            # print ("%d seconds elapsed awaiting a different IP address." % seconds)
    # output the
    # new IP address
    # print ("newIP: %s" % newIP)

if __name__ == "__main__":

    response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
    print("IP detectado usando biblioteca requests: ",response.text.strip())

    driver.get('http://icanhazip.com/')
    wait = WebDriverWait(driver, 5)
    time.sleep(random.uniform(1, 3))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    print("IP detectado usando Selenium: ",soup.find('body').get_text().strip())

    print("Mudando IP")
    mudar_ip()

    response = requests.get('http://icanhazip.com/', proxies={'http': '127.0.0.1:8118'})
    print("IP detectado usando biblioteca requests: ",response.text.strip())

    driver.get('http://icanhazip.com/')
    wait = WebDriverWait(driver, 5)
    time.sleep(random.uniform(1, 3))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    print("IP detectado usando Selenium: ",soup.find('body').get_text().strip())

    driver.close()