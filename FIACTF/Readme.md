# FIA CTV CTF Write-up
Đây là một thử thách CTF nhỏ dành cho các cộng tác viên (CTV) của FPT Information Assurance Club (FIA) liên quan đến các kiến thức cơ bản liên quan đến hệ điều hành Linux trên nền tảng Tryhackme. Link room: https://tryhackme.com/room/fiactf

Room này gồm có 10 thử thách. Chúng ta hãy xem qua các thử thách:

## 1) Getting Started!
Câu hỏi:

![Question](/FIACTF/images/Task1.1.png)

Ở đây chúng ta được yêu cầu đăng nhập vào máy chủ ssh sử dụng username và password như ở câu hỏi. Chúng ta sẽ sử dụng câu lệnh sau:

```console
ssh [username]
```
Đối với máy mình thì: 
```console
ssh guest@10.10.103.121
```
Khi nhập xong, nó sẽ yêu cầu mình nhập mật khẩu, nhập FIAWelcome.

![Step1](/FIACTF/images/Task1/Step1.png)

Thế là chúng ta đã truy cập được vào máy chủ rồi. Dùng `cat flag1` để lấy flag đầu tiên.

![Step2](/FIACTF/images/Task1/Step2.png)
## 2) Hide and Seek
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task2/Task2.png)

Câu lệnh `ls -a` sẽ cho chúng ta biết thêm tất cả các file và thư mục ẩn trong thư mục (bắt đầu bởi dấu . )

![Step1](/FIACTF/images/Task2/Step1.png)

Chúng ta thấy thư mục .hidden có vẻ kì lạ. Vậy ta sẽ xem thử trong đó có gì

![Step2](/FIACTF/images/Task2/Step2.png)

Ồ, flag2 đây rồi nhá, `cat` ra thôi!
## 3) Crytography and Compression
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task3/Task3.png)
Có vẻ thử thách này liên quan đến việc giải nén và mã hóa. Vậy, đầu tiên ta sẽ dùng lệnh `file` để xem thử file "flag3" là loại file gì.

![Step1](/FIACTF/images/Task3/Step1.png)

Đây là file gunzip, vậy ta sẽ đổi tên file bằng lệnh:
```console
mv Flag3 Flag3.gz
```
Rồi giải nén nó:
```console
gunzip Flag3.gz
```
Cứ tiếp tục quá trình `file`, đổi tên, giải nén như thế với các định dạng file khác nhau:

Tar (định dạng .tar):
```console
tar -xf Flag3.tar
```
Bzip2 (định dạng .bz2):
```console
bzip2 -d Flag3.bz2
```
Cuối cùng, ta sẽ được một file text nhưng vẫn còn vấn đề nữa: nội dung đã bị mã hóa.

![Step2](/FIACTF/images/Task3/Step2.png)

Có nhiều phương pháp để giải mã. Ở đây, chúng ta sử dụng base64 để tìm ra flag:
```console
cat flag3 | base64 -d
```
## 4) The Power of the Owner
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task4/Task4.png)
Khi ta thử chạy hay xem nội dung ở file "flag4" thì chúng ta không thể làm được.

![Step1](/FIACTF/images/Task4/Step1.png)

Vậy chắc hẳn là do chúng ta không có đủ quyền để làm việc với file này. Kiểm tra bằng lệnh `ls -l flag4`:

![Step2](/FIACTF/images/Task4/Step2.png)

Như đã thấy, chúng ta chỉ có quyền thực thi (execute) file này thôi. Vì vậy, chúng ta phải cấp thêm quyền bằng câu lệnh sau:
```console
chmod 777 flag4
```
Câu lệnh trên sẽ cho chúng ta thêm quyền đọc nội dung file (read) và chỉnh sửa file (write)

![Step3](/FIACTF/images/Task4/Step3.png)

Mặc dù chúng ta không phải là root user, nhưng miễn là chúng ta sở hữu file, chúng ta có thể chỉnh sửa quyền hạn của file đó theo ý mình muốn, `cat flag4` để lấy flag thôi.
## 5) The Chasing game
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task5/Task5.png)

Theo câu hỏi thì đầu tiên chúng ta sẽ sử dụng lệnh `find` để tìm file flag5 với cú pháp sau:
```console
find [nơi bắt đầu tìm] -name [tên file]
```
Ta sẽ bắt đầu tìm ở thư mục gốc (/) bởi vì nó sẽ tìm hết ở tất cả các thư mục trong máy chủ này.
```console
find / -name flag5
```
Tuy nhiên, chúng lại ra các kết quả như thế này:

![Step1](/FIACTF/images/Task5/Step1.png)

Đó là bởi vì có những thư mục chúng ta không có quyền truy cập vào. Chúng ta sẽ loại bỏ các dòng không mong muốn trên bằng cách thêm vào lệnh trên câu `2>/dev/null`. Câu này có tác dụng loại bỏ các dòng "lỗi" khi thực hiện lệnh (Google STDERR để biết thêm chi tiết)

```console
find / -name flag5 2>/dev/null
```

![Step2](/FIACTF/images/Task5/Step2.png)

Và chúng ta đã biết được file "flag5" để ở đâu rồi đó, `cat` ra thôi.

Bonus: Nếu chúng ta có tài khoản adminstrator (sử dụng được lệnh `sudo`), chúng ta có thể sử dụng lệnh `locate` thì nó ra luôn vị trí của file đó.
## 6) Environmental Movement
Câu hỏi

![Câu hỏi](/FIACTF/images/Task6/Task6.png)

Nhìn vào tựa đề thì thử thách này liên quan đến biến môi trường. Sử dụng lệnh `printenv` sẽ cho chúng ta tất cả các biến môi trường trong máy chủ này và flag6 sẽ nằm ở đó

![Step1](/FIACTF/images/Task6/Step1.png)
## 7) Screppy Greppy Webby
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task7/Task7.png)

Đầu tiên, nếu chúng ta thử `cat flag7` thì nó sẽ ra 1 loạt dòng chữ vô nghĩa và sẽ không bào giờ tìm thấy flag. Vì thế, chúng ta chỉ cần tìm ra dòng text mình muốn bằng câu lệnh `grep` và một chút regex (để ý rằng flag luôn có format là "FIA{}"):
```console
cat flag7 | grep FIA{.*}
```
Bonus: hãy thử `cat flag7 | grep FIA` :).
## 8) Bourne Again SH
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task8/Task8.png)

Đầu tiên, chúng ta chạy thử file "exec_me" nào

![Step1](/FIACTF/images/Task8/Step1.png)

Đến khúc này mình thấy có gì đó kì lạ nên mình `cat` thử xem file này có gì thì mình phát hiện ra đây chỉ là file shell script và mình chú ý tới dòng này:

![Step2](/FIACTF/images/Task8/Step2.png)

Điều đó có nghĩa là flag8 sẽ nằm ở biến "THIS_IS_NOT_A_FLAG". Như vậy, mình chỉ cần truy xuất cái biến đó là được.
```console
echo $THIS_IS_NOT_A_FLAG
```
Bonus: Hãy thử làm theo yêu cầu của file trên (giả bộ như chưa xem source code) để xem thử nó ra kết quả gì.
## 9) Malformed Editor
Câu hỏi:

![Câu hỏi](/FIACTF/images/Task9/Task9.png)

Hint:

![Hint](/FIACTF/images/Task9/Hint.png)

Dựa vào hint, mình sẽ sử dụng text editor (vim và nano) xem thử như thế nào và phát hiện ra điều này:

![Step1](/FIACTF/images/Task9/Step1.png)

Có vẻ như `nano` có vấn đề. Chúng ta đi đến /usr/bin/nano xem thử như thế nào:

![Step2](/FIACTF/images/Task9/Step2.png)

Có vẻ như file "nano" này là OPENSSH PRIVATE KEY. Sau một hồi tìm hiểu thì mình biết là máy chủ ssh còn có thể đăng nhập bằng KEY như trên. Vì vậy, mình copy nội dung file này cho nó tiện sử dụng
```console
cp /usr/bin/nano ~/id_rsa
```
Mình cần biết username là gì (có vẻ là kush)

![Step3](/FIACTF/images/Task9/Step3.png)

Cấp quyền 400 (r--------) cho file "id_rsa" (Vì nhiều quyền quá thì không đăng nhập được)
```console
chmod 400 id_rsa
```
Đăng nhập vào máy chủ ssh của kush nào:
```console
ssh -i id_rsa kush@10.10.103.121
```
Đăng nhập được rồi, tuy nhiên flag9 vẫn chưa có

![Step4](/FIACTF/images/Task9/Step4.png)

Đến đây, mình đã xin thêm gợi ý và nhận ra ra file này vẫn chưa rõ là file gì nên cần phải tải file này về máy của mình để xem thử nó như thế nào (mình đã copy file "id_rsa" vào máy mình và setup quyền cho nó rồi):
```console
scp -i [file key] [username]:[file cần tải về] [nơi chứa file tải về]
```
```console
scp -i id_rsa kush@10.10.103.121:~/flag9 ~
```
Mình dùng `file flag9` thì thấy đây chỉ là file ảnh thôi

![Step5](/FIACTF/images/Task9/Step5.png)

Sử dụng `eog flag9` để xem ảnh và đó chính là flag cần tìm.

Bonus: Muốn ngầu hơn thì ta cũng có thể sử dụng `tesseract` để in ra flag luôn
```console
tesseract flag9 out ; cat out.txt
```
## 10) "Least Privileges Model" Haha good jokes
Câu hỏi: 

![Câu hỏi](/FIACTF/images/Task10/Task10.png)

Hint:

![Hint](/FIACTF/images/Task10/Hint.png)

Ở đây, chúng ta được cho cái file .zip. Hãy giải nén nào (mật khẩu là flag 9)
```console
unrar e wordlist.rar
```
Ta sẽ được một cái file tên là "wordlist.txt". Dựa vào cái tựa đề và cái tên file này thì nhiều khả năng là chúng ta sẽ brute force vào tài khoản root trong máy chủ ssh. Vậy chúng ta thử xem sao

Sau một lúc thì mình phát hiện ra chúng ta có thể truy cập vào /etc/shadow ở máy chủ ssh và có tài khoản root luôn. Shadow là 1 file chứa mật khẩu đã bị mã hóa của mỗi tài khoản.

![Step1](/FIACTF/images/Task10/Step1.png)

Như vậy, cùng với wordlist được cho, mình sẽ sử dụng John the Ripper để brute force lên root qua các bước sau

Copy thông tin của root ở 2 file /etc/shadow và /etc/passwd vào 2 file:

![Step2](/FIACTF/images/Task10/Step2.png)

![Step3](/FIACTF/images/Task10/Step3.png)

Unshadow 2 file trên:
```console
unshadow passwd.txt shadow.txt > unshadowed.txt
```
Brute force nào:
```console
john --wordlist=~/wordlist.txt unshadowed.txt
```
Và xong, chúng ta đã tìm ra mật khẩu của tài khoản root là *6E2TyvD11wm9v-*

![Step4](/FIACTF/images/Task10/Step4.png)

Có mật khẩu rồi thì truy cập bằng `su root` thôi

![Step5](/FIACTF/images/Task10/Step5.png)

Vậy là chúng ta đã hoàn thành hết thử thách rồi.
