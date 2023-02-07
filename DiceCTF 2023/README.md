<div align='center'>

# **WRITE UP DICECTF 2023 PROVABLY SECURE 1+2**

</div>

## **1. Provably Secure**

### **1.1. Câu hỏi**

![](./img/Provably%20Secure/1.png)

Source code: [server.py](./src/Provably%20Secure/server.py)

Đây là thử thách về IND-CCA2, cơ bản là như sau

-   Phía server cho ta các public-key, thuật toán được sử dụng để mã hóa
-   Chúng ta được phép sử dụng thuật toán `encrypt` và `decrypt` của server tùy ý. Tuy nhiên, chúng ta không được phép `decrypt` lại ciphertext mà server đã gửi cho ta khi đã sử dụng chức năng `encrypt`.
-   Đầu tiên, chúng ta gửi 2 plaintext khác sau. Server sẽ chọn ngẫu nhiên 1 trong 2 plaintext và `encrypt` nó và cho ta ciphertext `C`.
-   Nhiệm vụ của chúng ta là xác định ra `C` được `encrypt` từ plaintext nào.

Tham khảo thêm tại [đây](https://kodu.ut.ee/~lipmaa/teaching/MTAT.07.006/2005/slides/S5.Bogdanov.indcca2.pdf)

### **1.2. Phân tích**

Ở chức năng `decrypt`, thực tế server không có kiểm tra lại ciphertext mà chúng ta đã `encrypt` trước đó do lỗi code. Điều này cho phép chúng ta có thể `decrypt` lại ciphertext mà server đã gửi cho ta và ra trực tiếp luôn plaintext (do `in_ct` là kiểu bytes còn `seen_ct` là hex string).

```python
if in_ct in seen_ct:
print("Cannot query decryption on seen ciphertext!")
exit(0)
``` 

### **1.3. Lời giải**

Chúng ta chỉ cần gửi 2 plaintext khác nhau và `decrypt` lại ciphertext mà server đã gửi cho ta là xác định được plaintext nào được mã hóa.

Script: [solve.py](./script/Provabl%20Secure/dec.py)

Flag: 
```
dice{yeah_I_lost_like_10_points_on_that_proof_lmao}
```

## **2. Provably Secure 2**

### **2.1. Câu hỏi**

![](./img/Provably%20Secure%202/2.png)

Source code: [server.py](./src/Provably%20Secure%202/server.py)

### **2.2. Phân tích**

Sau khi rút kinh nghiệm từ bài trước, server đã sửa lỗi và không cho phép chúng ta `decrypt` lại ciphertext mà server đã gửi cho ta.

Nhìn vào source code, ta thấy

-   Thuật toán mã hóa được sử dụng là RSA-OAEP
-   Chúng ta chỉ có 8 lần mã hóa và 8 lần giải mã
-   Độ dài của plaintext là 16 bytes. Độ dài của ciphertext là 512 bytes
-   Server tạo 2 cặp public-key và private-key khác nhau gọi là `pk0`, `key0` và `pk1`, `key1`. Server cấp cho chúng ta 2 public-key là `pk0` và `pk1`.
-   Khi mã hóa, server sẽ sử dụng 2 public-key khác nhau để mã hóa. Public-key thứ nhất sẽ mã hóa chuỗi 16 bytes ngẫu nhiên `r` được tạo ra từ hàm `os.urandom(16)`. Public-key thứ hai sẽ mã hóa chuỗi $r \ \oplus plaintext$. Kết quả là 2 ciphertext C1 và C2 kết hợp lại tạo nên chuỗi 512 bytes.
-   Khi giải mã, server nhận chuỗi 512 bytes `C`, chia đôi nó ra thành 2 chuỗi 256 bytes `c1` và `c2`. Sau đó, server sẽ giải mã 2 chuỗi này bằng 2 private-key tương ứng là `key0` và `key1`. Kết quả là 2  `r` và $r \ \oplus plaintext$. Cuối cùng, server sẽ xor 2 kết quả trên rồi trả về lại plaintext cho chúng ta. 

Do có public-key, chúng ta có thể tự `encrypt` một chuỗi bất kì mà không cần phải thông qua server (gọi là offline encryption). Thêm vào đó, mặc dù không thể `decrypt` lại ciphertext mà server đã gửi cho ta, nhưng do server đã chia đôi chuỗi ciphertext ra thành 2 chuỗi 256 bytes rồi `decrypt` từng chuỗi này, chúng ta có thể lấy nửa đầu của ciphertext `C1` kết hợp nửa kia của ciphertext `C2` rồi `decrypt`. Chúng ta có thể hình dung được kết quả mà server sẽ trả về cho chúng ta là gì.

Vì vậy, chúng ta sẽ sử dụng một chuỗi thứ 3 làm trung gian để có thể gián tiếp `decrypt` ra message ban đầu.

### **2.2. Lời giải**

Với 2 public-key, chúng ta sẽ tự `encrypt` plaintext `d`. Chúng ta được d1 và d2

Gửi 2 plaintext khác nhau `m0` , `m1` cho server. Server chọn `m = m0` hoặc `m1` rồi `encrypt`, chúng ta được ciphertext `C`, chia đôi thành `c1` và `c2` 

Tạo ra 2 chuỗi `c1d2` và `d1c2` rồi gửi lên cho server `decrypt`. Chuỗi `c1d2` sẽ cho ra kết quả là $r1 = r \oplus d$. Chuỗi `d1c2` sẽ cho ra kết quả là $r2 = d \oplus (r \oplus m)$.

Cuối cùng, ta lấy $r1 \oplus r2$ sẽ cho ra kết quả là m.

Script: [dec.py](./script/Provably%20Secure%202/dec.py)

Flag:

```
dice{my_professor_would_not_be_proud_of_me}
```