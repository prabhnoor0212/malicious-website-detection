import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import googlesearch

from OpenSSL import SSL
import idna
from socket import socket

from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
import time

def getHostname(url):
	p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

	m = re.search(p,'http://www.abc.com:123/test')
	return m.group('host')

def getPort(url):
	p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

	m = re.search(p,'http://www.abc.com:123/test')
	if m.group('port') is None:
		return 443
	return m.group('port')

def checkGoggleIndex(url):
	if url in google.search(url, 5):
		return 1
	else:
		return -1

def checkAWSRankings(url):
	lnk = 'https://www.alexa.com/siteinfo/'+url
	rc = BeautifulSoup(urlopen(lnk), 'html.parser')
	val = int(rc.find('strong', class_= 'metrics-data align-vmiddle').text)
	return val

def checkSSL(hostname, port):
	hostidna = idna.encode(hostname)
	s = socket()
	s.connect((hostname, int(port)))
	prname = s.getpeername()
	ctfc = SSL.Context(SSL.SSlv23_METHOD)
	ctfc.check_hostname = False
	ctfc.verify_mode = SSL.VERIFY_NONE
	sock = SSL.Connection(ctfc, s)
	sock.set_connect_state()
	sock.set_tlsext_host_name(hostname_idna)
	sock.do_handshake()
	cert = sock.get_peer_certificate()
	crypto_cert = cert.to_cryptography()
	sock.close()
	s.close()
	return cert

def checkSSLnew(url):
	lnk = 'https://www.sslshopper.com/ssl-checker.html#hostname='+url
	rc = BeautifulSoup(urlopen(lnk), 'html.parser')
	val = rc.find('table', {'class':'checker_messages'})
	#return val.findAll('span')
	return rc

def checkSubdomains(domain):
	return len(domain.split('.'))

def prefixSuffix(domain):
	if re.search('-', domain):
		return -1
	else:
		return 1

def checkSSLnewnew(url):
	lnk = 'https://www.sslshopper.com/ssl-checker.html#hostname='+url
	browser = driver = webdriver.Chrome(executable_path='C:/chromedriver.exe')  
	browser.get(lnk)
	time.sleep(5)
	html_source = browser.page_source  
	browser.quit()

	rc = BeautifulSoup(html_source, 'html.parser')
	try:
		val = rc.find('table', {'class':'checker_messages'})
		res = val.findAll('span')[0].text
	except IndexError:
		res = '0'

	return res

#ye sab baad mein. first we need to collect the expiry dates

'''
domain_names_arr = 
dots = (list(map(checkSubdomains, url_names_arr)))
dots_df = pd.DataFrame(dots,columns=['SubDomains'])
data_df = pd.concat([data_df, dots_df],axis=1, ignore_index=True)
'''

#for checking
#print(checkSSLnewnew('https://info5188fb900177e.000webhostapp.com/payment-update-0.html?fb_source=bookmark_apps&ref=bookmarks&count=0&fb_bmpos=login_failed'))

data_df = pd.read_csv('dataset.csv',header= None)
url_names_arr = data_df[0].tolist()

ssl_expiries = []

#for ojasvi
#for i in range(0, 200):
#	ssl_expiries.append(checkSSLnewnew(url_names_arr[i]))

#for prabhnoor
for i in range(200, 400):
	ssl_expiries.append(checkSSLnewnew(url_names_arr[i]))