import base64
import json
import os
# pip install pycryptodome
from Crypto.Util.number import getPrime, inverse, long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

flag = b"FIA{m1TH_1s_T00_p0WerFuLLL}"

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
    
def generate_data(data, public_key):
    aes_key = os.urandom(16)
    iv = os.urandom(16)
    public_key = json.loads(public_key)
    encrypted_data = AES_encrypt(data, aes_key, iv)
    encrypted_key = RSA_encrypt(aes_key, public_key)
    return json.dumps({"data": encrypted_data, "key": encrypted_key})

def decrypt_data(data, private_key):
    data = json.loads(data)
    aes_key = RSA_decrypt(data['key'].encode(), private_key)
    return (AES_decrypt(data['data'].encode(), aes_key), aes_key)

if __name__ == "__main__":
    
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 65537
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    ALICE_PUBLIC_KEY = {'n': n, 'e': e}
    ALICE_PRIVATE_KEY = {'n': n, 'd': d}
    
    BOB_PASSWORD = os.urandom(16).hex()
    
    try:
        print('Alice sending public key')
        print('Intercepted data: ', json.dumps(ALICE_PUBLIC_KEY))
        intercepted_public_key = input('Send data to Bob: ')
        public_key = json.loads(intercepted_public_key)
        if not ((int(public_key['n']).bit_length() == 2048) and (int(public_key['e']) == 65537)):
            raise Exception
        print('Bob sending password')
        print('Intercepted data: ', generate_data(BOB_PASSWORD.encode(), intercepted_public_key))
        intercepted_data = input('Send data to Alice: ')
        password, aes_key = decrypt_data(intercepted_data, ALICE_PRIVATE_KEY)
        if password == BOB_PASSWORD:
            print('Alice sending flag')
            print(f'aes_key: {aes_key.hex()}')
            print('Intercepted data: ', AES_encrypt(flag, aes_key, os.urandom(16)))
        else:
            raise Exception
    except:
        print('Something went wrong... Or may be you sussss')
    