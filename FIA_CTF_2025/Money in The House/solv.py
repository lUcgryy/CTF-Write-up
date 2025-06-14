import pwn
import json
import base64
import os

from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

pwn.context.log_level = 'debug'

io = pwn.process(['python', 'chall.py'])

def RSA_encrypt(message, public_key):
    
    n = public_key['n']
    e = public_key['e']
    return base64.b64encode(long_to_bytes(pow(bytes_to_long(message), e, n))).decode()

def RSA_decrypt(ciphertext, private_key):
    n = private_key['n']
    d = private_key['d']
    return long_to_bytes(pow(bytes_to_long(base64.b64decode(ciphertext)), d, n))

def AES_encrypt(message, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + aes.encrypt(pad(message, AES.block_size))).decode()

def AES_decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(ciphertext), AES.block_size).decode()

def generate_data(data, public_key, aes_key):
    # aes_key = os.urandom(16)
    iv = os.urandom(16)
    public_key = json.loads(public_key)
    encrypted_data = AES_encrypt(data, aes_key, iv)
    encrypted_key = RSA_encrypt(aes_key, public_key)
    return json.dumps({"data": encrypted_data, "key": encrypted_key})

def decrypt_data(data, private_key):
    data = json.loads(data)
    aes_key = RSA_decrypt(data['key'].encode(), private_key)
    return (AES_decrypt(data['data'].encode(), aes_key), aes_key)

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 65537
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

MY_PUBLIC_KEY = {'n': n, 'e': e}
MY_PRIVATE_KEY = {'n': n, 'd': d}
io.recvuntil(b'data:  ')
ALICE_PUBLIC_KEY = io.recvline().strip().decode()
print(f'ALICE_PUBLIC_KEY: {ALICE_PUBLIC_KEY}')

io.sendlineafter(b'Bob: ', json.dumps(MY_PUBLIC_KEY).encode())

io.recvuntil(b'data:  ')

raw_data = io.recvline().strip().decode()

# data_json = json.loads(raw_data)
# enc_key = data_json['key']
# enc_data = data_json['data']

decrypted_data, aes_key = decrypt_data(raw_data, MY_PRIVATE_KEY)
print(f'aes_key: {aes_key.hex()}')
print(f'Decrypted data: {decrypted_data}')

io.sendlineafter(b'Alice: ', generate_data(decrypted_data.encode(), ALICE_PUBLIC_KEY, aes_key).encode())

io.recvuntil(b'data:  ')

encrypted_flag = io.recvline().strip()
print(f'Encrypted flag: {encrypted_flag }')
print(AES_decrypt(encrypted_flag, aes_key))
io.interactive()