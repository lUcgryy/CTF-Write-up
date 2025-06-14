import pwn
import json
from hashlib import sha1

pwn.context.log_level = 'debug'

p = pwn.process(['python', 'chall.py'])

def generate_command_data(user, command):
    p.sendlineafter(b'Enter choice: ', b'1')
    p.sendlineafter(b'Enter user: ', user.encode())
    p.sendlineafter(b'Enter command: ', command.encode())
    return p.recvline().decode().strip()

def execute_command(data):
    p.sendlineafter(b'Enter choice: ', b'2')
    p.sendlineafter(b'Enter data: ', data.encode())
    return p.recvline().decode().strip()


for _ in range(5):
    raw_data = generate_command_data('admin', 'get_flag')
    a = json.loads(raw_data)
    print(f'Raw data:', raw_data)
    
    print(a)
    key = bytes.fromhex(a['key'])
    new_key = sha1(key).hexdigest()
    print(f'New key:', new_key)
    a['key'] = new_key
    payload = json.dumps(a)
    print(f'Payload:', payload)
    
    execute_command(payload)


p.interactive()
