import os
import io
import sys
import json
import urllib2
import cookielib
import re
import requests
from bs4 import BeautifulSoup
from PIL import Image

keyword = sys.argv[1]
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}

for sgn in range(0,2):
	if sgn == 0:
		query = 'not ' + keyword
	else:
		query = keyword
	url = 'https://www.google.co.in/search?q=' + query.replace(' ', '%20') + '&source=lnms&tbm=isch'
	soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')
	directory = os.path.join('lib', keyword, str(sgn))
	if not os.path.exists(directory):
		os.makedirs(directory)
	pos = 0
	for a in soup.find_all('div', {'class':'rg_meta'}):
		link = json.loads(a.text)['ou']
		typee = json.loads(a.text)['ity']
		if typee == '':
			typee = 'jpg'
		try:
			request = urllib2.Request(link, headers=header)
			byte = urllib2.urlopen(request).read()
		except Exception as e:
			continue
		image = Image.open(io.BytesIO(byte))
		image = image.resize((256,256))
		image = image.convert('RGB')
		image.save(os.path.join(directory, str(pos) + '.jpg'), 'JPEG')
	#	filee = open(os.path.join(directory, str(pos) + '.' + typee), 'wb')
	#	filee.write(byte)
	#	filee.close()
		pos += 1

