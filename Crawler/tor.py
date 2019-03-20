import requests
from TorCrawler import TorCrawler
import time
import os

params = dict(
  client_id='T5H1DGJAVQPKQNPHKSEYXVXRFQGZRMLCLBC5X0KXQKN2XHFZ',
  client_secret='4DEZN2E4HPDZAKYJG2T3ATH3LQKEEPAIPVPQ1WEIDT4BAK11',
  v='20180323',
  limit=1
)



crawler = TorCrawler()

#data = crawler.get("https://api.foursquare.com/v2/venues/502aa937e4b0be57fd4cac73?m=swarm", headers=params)
while 1:
    data = crawler.get("https://www.tudogostoso.com.br/receita/31593-pudim-de-leite-condensado.html")
    print(crawler.ip)
    os.system("/etc/init.d/tor restart")
    time.sleep(1)
    # Make a GET request (returns a BeautifulSoup object unless use_bs=False)


# TorCrawler will, by default, rotate every n_requests.
# If you want to manually rotate your IP, you can do that any time.
# crawler.rotate()



# download do Tor navegador
# sudo apt install linuxbrew-wrapper
# brew install tor
# sudo apt-get install -f tor

# service tor start
# tor --hash-password mypassword
# salvar nova hash no arquivo etc/tor/torrc na linha HashedControlPassword e descomentar ControlPort 9051
# pip install beaufitulsoup4
# sudo apt-get install python-setuptools
# pip install stem
# 