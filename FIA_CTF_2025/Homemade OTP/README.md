<div align='center'>

## **Homemade OTP (Author Writeup)**

</div>

Ý tưởng chính: Với `HMAC`, nếu `key` quá dài thì HMAC sẽ tính lại `key` bằng cách lấy mã hash của `key` làm `key` mới (Ref: https://en.wikipedia.org/wiki/HMAC). Do đó chỉ cần tính hash của `key` là có thể bypass được check sử dụng lại key cũ.

Solve script: [solv.py](solv.py)
