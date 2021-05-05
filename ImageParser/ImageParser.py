from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests


urlBase = 'https://hokiesports.com/'
html = urlopen('https://hokiesports.com/sports/mens-soccer/roster')
bs = BeautifulSoup(html, 'html.parser')
#print(bs)
images = bs.findAll('img', {'data-src':re.compile('.jpg')})
print(len(images))
# images = [x['src'] for x in bs.find_all('img', {'class': 'lazyload'})]
for image in images:
    print(urlBase + image['data-src'])
    #download_imag = url
    #if("data-src" in image):
    #print("hello " + image.get('data-src'))


urlBase2 = 'https://hokiesports.com/'
html2 = requests.get('https://hokiesports.com/sports/mens-soccer/roster')
bs = BeautifulSoup(html2.text, 'html.parser')
#print(bs)
images = bs.findAll('img', {'data-src':re.compile('.jpg')})
print(len(images))
# images = [x['src'] for x in bs.find_all('img', {'class': 'lazyload'})]
for image in images:
    print(urlBase + image['data-src'] )
    #download_imag = url
