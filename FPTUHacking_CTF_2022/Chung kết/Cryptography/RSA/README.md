# **FPTU Hacking CTF 2022 Writeup vòng chung kết của team [FI?]**
## **I. Cryptography**

### **1. RSA**
File được cung cấp: [task.py](/FPTUHacking_CTF_2022/Chung%20k%E1%BA%BFt/Cryptography/RSA/src/task.py)

Đầu tiên, ta thấy rằng số N được tính ra bởi ba số nguyên tố:
```python
N = p*q*r
```

Tiếp theo, ta chú ý đến ba số a, b, c
```python
A = pow(x*y + p*q, 3*e, N)
B = pow(x*y + p*r, 6*e, N)
C = pow(x*y + q*r, 5*e, N)
```
Điều đó có nghĩa là:
$$a \equiv  (xy + pq)^{3e} \ \ \ (\bmod N)$$
$$b \equiv  (xy + pr)^{6e} \ \ \ (\bmod N)$$
$$c \equiv  (xy + qr)^{5e} \ \ \ (\bmod N)$$

Từ dữ kiện trên, mình tìm ra lời giải như thế này

Với hai số a và b:

- Biến đổi để hai vế phải có cùng mũ
$$a^2 \equiv  (xy + pq)^{6e} \ \ \ (\bmod N)$$
$$b \equiv  (xy + pr)^{6e} \ \ \ (\bmod N)$$
- Trừ hai vế lại với nhau
$$a^2 - b \equiv (xy + pq)^{6e} - (xy + pr)^{6e} = p(q-r)t \ \ \ (\bmod N)$$
với t là một số nguyên nào đó
- Từ đó, ta thấy rằng:
$$a^2 - b = kN + p(q-r)t \ \ \ \vdots \ \ \ p$$
Vì vậy, $p = GCD(N, a^2 - b)$

Tương tự: $q = GCD(N, a^5 - c^3)$ và $r = GCD(N, b^5 - c^6)$

Khi tìm ra ba số nguyên tố p, q, r thì việc còn lại là giải mã là flag thôi

Đây là script để giải thử thách này: [dec.py](/FPTUHacking_CTF_2022/Chung%20k%E1%BA%BFt/Cryptography/RSA/scripts/dec.py)

Flag:
```
FPTU{G4me_0n!!!_Yet_another_baby_RSA_challenge}
```