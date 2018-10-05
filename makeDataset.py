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

def checkGoggleIndex(url):
	if url in google.search(url, 5):
		return 1
	else:
		return -1

def checkAWSRankings(url):
	lnk = 'https://www.alexa.com/siteinfo/'+url
	try:
		rc = BeautifulSoup(urlopen(lnk), 'html.parser')
		val = rc.find('strong', class_= 'metrics-data align-vmiddle').text
	except:
		val = '-'
	print(val)
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

def checkPrefixSuffix(domain):
	if re.search('-', domain):
		return -1
	else:
		return 1

def checkSSLnewnew(url):
	lnk = 'https://www.sslshopper.com/ssl-checker.html#hostname='+url
	browser = webdriver.Chrome(executable_path='C:/chromedriver.exe')  
	browser.get(lnk)
	time.sleep(5)
	html_source = browser.page_source  
	browser.quit()

	rc = BeautifulSoup(html_source, 'html.parser')
	try:
		val = rc.find('table', {'class':'checker_messages'})
		res1 = val.findAll('span')[0].text
		restmp = val.findAll('td', {'class':'failed'})
		if restmp == []:
			res2 = 0
		else:
			res2 = 1
		res = [res1, res2]
	except:
		res = ['-1','-1']

	return res

def getDomain(url):
	if re.search('www', url):
		start = url.find('www') + 3
		stop = url[start:].find('/') + start
		return url[start:stop]
	elif re.search('http://', url):
		start = url.find('http://') + 7
		stop = url[start:].find('/') + start
		return url[start:stop]
	elif re.search('https://', url):
		start = url.find('https://') + 8
		stop = url[start:].find('/') + start
		return url[start:stop]
	else:
		return ''



data_df = pd.read_csv('dataset.csv',header= None)
url_names_arr = data_df[0].tolist()

domain_names_arr = list(map(getDomain, url_names_arr))

dots = list(map(checkSubdomains, domain_names_arr))
dots_df = pd.DataFrame(dots,columns=['SubDomains'])

prefixSuffix = list(map(checkPrefixSuffix, domain_names_arr))
prefixSuffix_df = pd.DataFrame(prefixSuffix,columns=['PrefixSuffix'])

#googleKnows = list(map(checkGoggleIndex, url_names_arr))
#googleKnows_df = pd.DataFrame(googleKnows,columns=['Google Index'])

awsRanks = list(map(checkAWSRankings, url_names_arr))
awsRanks_df = pd.DataFrame(awsRanks,columns=['AWS Rank'])


data_df = pd.concat([data_df, dots_df, prefixSuffix_df, awsRanks_df],axis=1, ignore_index=True)

#ssl = (list(map(checkSSLnewnew, url_names_arr[800:1000])))
#ssl_df = pd.DataFrame(ssl,columns=['Expiry Date', 'Failed Cases'])

#ssl_df.to_csv('ssl_checks06.csv')

data_df.to_csv('final_dataset.csv')