<div align='center'>

## **Homemade OTP Revenge (Author Writeup)**

</div>

Ý tưởng ban đầu: Sẽ nhập username khác sao cho nếu chọn command `get_flag` thì `Generate command data` sẽ trả về OTP chính xác nếu dùng username là `admin` 

Khi hàm `bytes_to_long` được gọi với message với $\overline{u_nu_{n-1} \ldots u_1u_0}$ thì sẽ trả về giá trị là $u_n \cdot 256^n + u_{n-1} \cdot 256^{n-1} + \ldots + u_1 \cdot 256^1 + u_0 \cdot 256^0$. Do đó đối với trường hợp này, ta có thể tách phần `command data` thành 3 phần: `"user": "`, username sẽ nhập vào $\overline{u_{l-1}u_{l-2}...u_1u_0}$, và phần còn lại (luôn là chuỗi cố định (`", "command": "get_flag"...`)). Có thể biểu diễn điều này bằng công thức: 

```math
data = 256^a * (256^l*m_0 + \sum_{i=0}^{l-1} 256^i*u_i) + c
```

với a là độ dài của phần thứ 3 của data (phần còn lại)

Do đó, ta sẽ tìm $\overline{u_l u_{l-1} \ldots u_1 u_0}$ sao cho $256^a*(256^l*m_0 + 256^{l-1}*u_{l-1} + 256^{l-2}*u_{l-2} + \ldots + 256^0*u_0) + c \equiv 256^a*v + c (mod p)$ tương đương với $256^{l-1}*u_{l-1} + 256^{l-2}*u_{l-2} + \ldots + 256^0*u_0 - (256^l*m_0 - v) \equiv 0 \text{ (mod p)}$

Với bài toán này, ta có thể dùng thuật toán Lenstra–Lenstra–Lovász (LLL). `LLL` sẽ cố gắng tìm "nghiệm gần với 0 nhất". Để thuận tiện hơn, ta sẽ đặt $x_i = u_i - 109$ để khiến $\(x_i \in [-12, 13] \) $