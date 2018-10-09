import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from OpenSSL import SSL
import idna
from socket import socket
import google

def checkLength(url):
	if len(url) < 40:
		return 1
	elif len(url) < 60:
		return 0
	else:
		return -1


def checkIfShortened(url):
	#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'}
	#req = Request(url, headers=headers)
	#req = urlopen(req)
	#response = req.getcode()
	#print(response)
	#if response == 302:
	shorted = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
					'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
					'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
					'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
					'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
					'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
					'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
	if shorted:
		return 1
	else:
		return -1
	#else:
	#	return -1

def isIpAddress(url):
	ip4 = re.match('([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])$', url)
	ip6 = re.match('([0-9A-Fa-f]{1,4}\:){1,7}[0-9A-Fa-f]{1,4}$|([0-9A-Fa-f]{1,4}\:){1,7}\:$', url)
	if ip6 or ip4:
		return -1
	else:
		return 1

def hasDoubleSlashes(url):
	if url.rfind('//') > 6:
		return -1
	else:
		return 1

def hasAtSymbol(url):
	if re.search('@', url):
		return -1
	else:
		return 1

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
		return 'no'

# IMPORTANT
def prefixSuffix(domain):
	if re.search('-', domain):
		return -1
	else:
		return 1


# IMPORTANT
def checkSubdomains(domain):
	'''if len(domain.split('.')) > 3:
		return -1
	elif len(domain.split('.')) == 3:
		return 0
	else:
		return 1'''
	return len(domain.split(.))

# IMPORTANT
def checkSSL(hostname, port):
	hostidna = idna.encode(hostname)
	s = socket()
	s.connect(hostname, port)
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
    return cert #something idk what really tbh

def checkDomainLife(url):
	#later
	pass

def checkFavicon(url):
	#do we really need it?
	pass

def checkPorts(url):
	#i have no idea
	pass

def checkHTTPSinURL(url):
	if re.search('https', url.lower()):
		return -1
	else:
		return 1

def getSoup(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'}
	req = Request(url, headers=headers)
	req = urlopen(req)
	soup = BeautifulSoup(req, 'html.parser')
	return soup


# IMPORTANT
def checkAnchors(url, soup, domain):
	no = ['#', 'javascript', 'mailto']
	yes = [domain, url]
	ls = soup.find_all('a', href=True)
	mal = 0
	if len(ls) == 0:
		return 1
	for a in ls:
		for i in no:
			if i in a['href'].lower():
				mal += 1
		for i in yes:
			if i not in a['href']:
				mal += 1
	danger = (mal/len(ls))*100
	if danger < 31.0:
		return 1
	elif danger <= 67.0:
		return 0:
	else:
		return -1

def checkTags(url, soup, domain):
	yes = [domain, url]
	mal = 0
	y = 0
	ls = soup.find_all('link', href=True)
	if not len(ls) == 0:
		for i in ls:
			if i not in yes:
				mal += 1
	y += len(ls)
	ls = soup.find_all('script', src=True)
	if not len(ls) == 0:
		for i in ls:
			if i not in yes:
				mal += 1
	y += len(ls)
	ls = soup.find_all('meta')
	if not len(ls) == 0:
		for i in ls:
			if i not in yes:
				mal += 1
	y += len(ls)
	danger = (mal/y)*100
	if danger < 17.0:
		return 1
	elif danger <= 81.0:
		return 0:
	else:
		return -1

def checkServerForm(url, soup, domain):
	ls = soup.find_all('form', action=True)
	for i in ls:
		if i['action'] =="" or i['action'] == "about:blank" :
         	return -1
        if domain not in i['action'] or url not in i['action']:
        	return 0
    return 1

def checkMailto(url, soup, domain):
	ls = soup.find_all('form', action=True)
	for i in ls:
		if 'mailto' in i['action'].lower():
			return -1
	return 1

def getDomainAge(domain):
	created = domain.creation_date
	expires = domain.expiration_date
	age = abs((expires-created).days)
	if age//30 < 6:
		return -1
	else:
		return 1

def checkPhishIPstats(url, hostname):
	url_match = re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
	try:
		ip = socket.gethostbyname(hostname)
	except:
		pass
		#something?
	
	ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                       '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                       '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                       '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                       '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                       '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip)
	
	if url_match or ip_match:
		return -1
	else:
		return 1


# IMPORTANT
def checkGoggleIndex(url):
	if url in google.search(url, 5):
		return 1
	else:
		return -1

def checkDNS(url):
	#later
	pass

def hostInURL(url, hostname):
	if re.search(hostname, url):
		return -1
	else:
		return 1


# IMPORTANT
def checkAWSRankings(url):
	lnk = 'https://www.alexa.com/siteinfo/'+url
	rc = BeautifulSoup(urllib.urlopen(lnk), 'html.parser')
	val = html.find(lambda tag: tag.name == 'strong' and tag['class'] == 'metrics-data align-vmiddle')
	return val

def main(url):
	soup = getSoup(url)
	domain = getDomain(url)

	#get hostname somehow
	#get port somehow. Probably 443.

	checks = []

	checks.append(checkLength(url))
	checks.append(checkIfShortened(url))
	checks.append(hasDoubleSlashes(url))
	checks.append(isIpAddress(url))
	checks.append(hasAtSymbol(url))
	checks.append(prefixSuffix(domain))
	checks.append(checkSubdomains(domain))
	checks.append(checkHTTPSinURL(url))

	checks.append(checkServerForm(url, soup, domain))
	checks.append(checkTags(url, soup, domain))
	checks.append(checkAnchors(url, soup, domain))
	checks.append(checkMailto(url, soup, domain))

