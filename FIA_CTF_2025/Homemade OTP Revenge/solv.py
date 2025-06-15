# import pwn
import json
from hashlib import sha1
import pwn

from sage.all import *

from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime # pip install pycryptodome

pwn.context.log_level = 'debug'

io = pwn.process(['python', 'chall.py'])

def generate_command_data(user, command):
    io.sendlineafter(b'Enter choice: ', b'1')
    io.sendlineafter(b'Enter user: ', user.encode())
    io.sendlineafter(b'Enter command: ', command.encode())
    return io.recvline().decode().strip()

def execute_command(data):
    io.sendlineafter(b'Enter choice: ', b'2')
    io.sendlineafter(b'Enter data: ', data.encode())
    return io.recvline().decode().strip()

m0 = bytes_to_long(b'{"user": "')
v = bytes_to_long(b'{"user": "admin')
io.recvuntil(b'modulus = ')
p = int(io.recvline().strip().decode())
# p = 66121435429205161366221191885149776902043242314543344699871226787126515223877
answer = b''
for l in range(100,200):
    print(f'[ ] Trying {l = }...')
    s = int((sum(256**i * 109 for i in range(l)) + 256**l * m0 - v) % p)
    '''
    [s          1      0      0     ... 0] <-- 1
    [256^(k-1)  0      1      0     ... 0] <-- x(k-1)
    [256^(k-2)  0      0      1     ... 0] <-- x(k-2)
    [                       ...          ]     ...
    [256^0      0      0      0     ... 1] <-- x0
    [p          0      0      0     ... 0] <-- *
     ↓          ↓      ↓      ↓         ↓
     0          1      x(k-1) x(k-2)    x0
    '''
    
    weights = [256] + [1 for _ in range(l+1)]
    A = Matrix(l+2, l+2)
    Q = diagonal_matrix(weights)
    
    A[0, 0] = s
    A[l+1, 0] = p
    for i in range(l): 
        A[i+1, 0] = 256**(l-1-i)
    for i in range(l+1): 
        A[i, i+1] = 1
    
    A *= Q
    A = A.LLL()
    A /= Q
    # print(f'[ ] Reduced matrix:\n{A}')
    for row in A:
        if row[0] != 0:
            continue
        if row[1] < 0:
            row = -row
        if row[1] != 1: 
            continue
        m = row[2:]
        
        if min(m) < -12: 
            continue
        if max(m) > 12: 
            continue
        m = bytes(109 + mc for mc in row[2:]).decode()
        print(f'[+] Found: {m} with {l = }')
        answer = m
    if answer:
        break

for _ in range(5):
    raw_data = generate_command_data(answer, 'get_flag')
    a = json.loads(raw_data)
    print(f'Raw data:', raw_data)
    otp = a['otp']
    key = a['key']
    
    a['user'] = 'admin'
    # print(a)
    # key = bytes.fromhex(a['key'])
    # new_key = sha1(key).hexdigest()
    # print(f'New key:', new_key)
    # a['key'] = new_key
    payload = json.dumps(a)
    print(f'Payload:', payload)
    
    execute_command(payload)


io.interactive()
