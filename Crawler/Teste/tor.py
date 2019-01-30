import requests
from TorCrawler import TorCrawler
import os
import commands
import time

proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

# sudo /etc/init.d/tor restart
def main():

    crawler = TorCrawler()

    url = 'https://api.foursquare.com/v2/venues/502aa937e4b0be57fd4cac73?m=swarm'
    data = crawler.get(url)
    print(data)
    print(crawler.ip)

    #os.system("sudo su")
    #os.system("asdf321")
    os.system("/etc/init.d/tor restart")
    #os.system("su willdoliver")
    time.sleep(10)
    print(crawler.ip)


    #crawler.rotate()
    #print(crawler.ip)

if __name__ == '__main__':
    main()

