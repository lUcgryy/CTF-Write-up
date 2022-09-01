# **FPTU Hacking CTF 2022 Writeup của team [FI?] (Crptography)**

Đây là cuộc thi CTF dành riêng cho các bạn hiện đang học tại các cơ sở của đại học FPT. Tất cả các challenge trong cuộc thi lần này đều do team 0ni0n ra đề. Dưới đây là các challenges crptography mà team mình đã làm được.

Do team mình chỉ làm được ba câu liên quan đến RSA nên team trước hết sẽ nói về những điều cơ bản về loại mã hóa này

#### **Các tham số cơ bản**
- p và q: Hai số nguyên tố được chọn (thường là rất lớn)
- n = $p*q$: Modulus
- phi: Hàm phi Euler của n $$phi = (p - 1)*(q - 1)$$
- e: Số mũ mã hóa (thường sẽ là 65537)
- d: Số mũ giải mã (là số thỏa mãn điều kiện $e*d \bmod phi = 1$ )
- msg: Message (ở đây là flag)
- c: Message đã được chuyển qua dạng số và đã được mã hóa

#### **Các bước mã hóa cơ bản**
- Chuyển msg về dạng số
```python
flag_enc = flag.encode()
msg = bytes_to_long(flag_enc)
# bytes_to_long lấy từ module Crypto.Util.Number (pip3 install pycryptodome)
```
- Xác định e, tìm p, q và tính n:
```python
e = 65537
p = getprime(512)
q = getprime(512)
n = p*q
```
- Tính c:
```python
c = pow(msg, e, n)
```
#### **Các bước giải mã cơ bản**
- Tìm p,q (mình thường dùng [factordb](http://factordb.com) hoặc [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) để tìm)
- Tính phi
```python
phi = (p - 1)*(q - 1)
```
- Tính d
```python
d = inverse(e, phi)
# inverse lấy từ module Crypto.Util.number
```
- Tính ra msg (tức là flag) và decode lại
```python
msg = pow(c, d, n)
# đây là cách mình decode
msg_hex = hex(msg)[2:-1]
print(bytes.fromhex(msg_hex).decode('utf-8'))
```

Dưới đây là các thử thách RSA mà mình đã giải được
### **1. RRSSAA**
Câu hỏi:

![Question](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/RRSSAA/Question.png)

File mã hóa: [enc.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/RRSSAA/enc.py)

Output của file trên (message đã được mã hóa): [out.txt](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/RRSSAA/output.txt)

Dựa vào hai file trên thì ta thấy rằng flag bị chia làm 2 phần, mỗi phần được cung cấp các số là c, e và n

Mình sử dụng [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool) để giải mã từng phần một:

Phần một:
```zsh
python3 RsaCtfTool.py -n 6490575414546753422169557924726633698938840342804007877593140124713933084247239272632050468659186332284597365791524523203890501075477199471733446503331287392773585633905281136028592442460859381818517915584152977506750156812875265542004792964515179303151752533661952619290383021701963596253894613400006395933540184308383205582620641667831066786941489460633668241024642868786169958309890455670637684750726393954761545971579402229970767454083426068165630397383861060884335031186141866257202083321618111563513626855089058455000733251707282966148763783562830207713984490916122334630807846682310867739481868099531604199361 --uncipher 1371759048149611040770011921418215274402106876461640344401671404760028350471019509755594539076613816766603306047375261901377330195783332158141855247009473212134079930634738546463366062005611533899217760683884243552925137820869416006162234259026748413289532952661691110428194702340622114401978375464352186350704087241652696132238723998349724100265841522875869638348652264210710788722315420766378666865380442669403058098363185242109346451512352300814495546093790945666900753896675597726653142708523272375106881144319062453373966096109696111579547829616782570851839672780482070134871669403035987583702072195847608957359 -e 65537 --attack all
```
- Kết quả:

![Part1](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/RRSSAA/Part1.png)

Phần 2:
```zsh
python3 RsaCtfTool.py -n 13908131502186888224364262080833432482112861581791111042080173649970166026500874345460017841288071475736405123781852190183413966703850124472840235945014409259347227565898256371761534183506997838619648382565719683809192690932704492409765399588791914002222178163703645294336900346832278341843927619793929067019394635129701010101745788281692696408082738016096835941283027842912901321468805256876430916029359283952631637587185030521085502993312596951304076920403362682120118569535468210808087497348286199962361033672950036309555605765599177178688696972244879328867379830135765957335666748015324124120372593527528004246553 --uncipher 13328797044862662040031336230712258541783627901094587775876771299742074083680668896746399241086714119830688395349669302694505303651730534145158997674920873640772428508628089236079960707540568179840256034900463343673430411467530242996605459278602091508195203902676963982374006581722502811925835672334973207193807537155840718929964442943000099917015241745382770009470964464459371708987908791454965936419120107641347519737033356242627992230599067761853501335939840610231285729885833878366987477004347128006121486442078361960058397114501698227903288899815398102056944015302283951908059548073442330608775519166795679207096 -e 65537 --attack all
```
- Kết quả

![Part2](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/RRSSAA/Part2.png)

Ghép 2 phần lại ta sẽ được flag:
``` 
FPTUHacking{Us3_0f_s1ngl3_pr1m3_4nd_cl0se_prim3s_w3r3_w4st3_0f_c0mput3r_Cycl35}
```

### **2. characters**
Câu hỏi

![Question](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/characters/Question.png)

File mã hóa: [enc.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/characters/enc.py)

Output của file trên (message đã được mã hóa): [out.txt](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/characters/out.txt)

Câu này cũng như câu trước nhưng mà flag bị chia làm nhiều phần, mỗi phần một kí tự và mã hóa từng kí tự của flag rồi bỏ các kết quả đó trong một list ct.
```python
ct = []
for i in flag:
    ct.append( pow(  bytes_to_long(i.encode()),e,n) )
```
Vấn đề này thì mình chỉ cần viết code xử lí từng con số trong mảng rồi ghép chúng lại. Đầu tiên ta vẫn phải tìm p và q. Mình dùng [factordb](http://factordb.com) để tìm ra hai số trên.

![factordb](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/characters//factordb.png)

Sau khi có hai số rồi thì mình viết script để xử lí list ct trên:
```python
flag = ''
for i in range(len(ct)):
    flag += chr(pow(ct[i], d, n))
print(flag)
```
Script đầy đủ: [dec.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Script/characters.py)

Flag:
```
FPTUHacking{3ncRYpt1ng_34ch_ch4r_ainT_G0nn4_h3lp}
```
### **3. keyRSA**
Câu hỏi

![Question](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/keyRSA//Question.png)

File mã hóa: [enc.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/keyRSA/enc.py)

Đầu tiên, ta hãy nhìn vào file [enc.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/keyRSA/enc.py) thì ta thấy có tham số x khá là lạ
```python
x = p % (n//2)
```

Từ biểu thức trên mình suy ra: $$p = k*{n-1 \over 2} + x$$  với k là số nguyên.

Mình thấy k chỉ có thể bằng 0 vì nếu $k < 0$ thì $p < 0$ (vì khi mình chạy để xem x như thế nào thì thấy x nó rất nhỏ so với n/2), còn k = 1 thì $p > n/2 \Longrightarrow q < 2$, điều này vô lí vì q cũng là số nguyên tố

Chạy lại file kiểm tra lại nhận định của mình, dùng [factordb](http://factordb.com), tính ```n % p```  thì thấy nhận định của mình là đúng rồi.

Tiếp tục đọc [enc.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Src_code/keyRSA/enc.py) thì mình thấy dòng này
```python
user_d = int(input("\nEnter your key : \n"))
    if user_d != d:
        if pow(ct,user_d,n) == pow(ct,d,n):
            print(flag)
```
Hmm, có vẻ như nó kêu mình nhập một số nào đó lưu vào biến ```user_d``` rồi kiểm tra nếu ```user_d``` thỏa mãn hai điều kiện là
- $user\_d \ne d$
- $ct^{user\_d}\bmod n = ct^d\bmod n$

Mình phải tìm ra tính chất nào đó của ```user_d``` để đơn giản hóa vấn đề. Sau một hồi Google thì phát hiện ra tính chất này (nguồn: https://vi.wikipedia.org/wiki/S%E1%BB%91_h%E1%BB%8Dc_m%C3%B4_%C4%91un#S%E1%BB%91_m%C5%A9):
![Tính chất](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/images/keyRSA/Math.png)

Vì vậy, mình chỉ cần cho $user\_d = d + 2*phi$ là được

Cuối cùng, mình viết script sử dụng pwntools để tương tác với server của thử thách. Nếu làm tay sẽ gần như không làm đc vì nếu để lâu quá thì server sẽ không chạy nữa (mình mất rất lâu mới nhận ra vấn đề này :( )

Đây là script để giải thử thách này: [dec.py](/V%C3%B2ng%20lo%E1%BA%A1i/Cryptography/Script/keyRSA.py)

Flag: 
```
FPTUHacking{Y0u_kn0w_t0_CR34t3_y0ur_0wn_k3y!!!}
```
