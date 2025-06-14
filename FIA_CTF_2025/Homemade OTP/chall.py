import hmac
import os
import json
from hashlib import sha1
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime # pip install pycryptodome

flag = 'FIA{5OM371m3_5Up3rLoNG_k3y_12_nOt_GOod}'

def generate_otp(key, data, modulus):
    data = bytes_to_long(data) % modulus
    data = long_to_bytes(data)
    hahsed = hmac.new(key, data, sha1).digest()
    binary = hahsed[0] << 24 | hahsed[1] << 16 | hahsed[2] << 8 | hahsed[3]
    otp = str(binary % 1000000).zfill(6)
    return otp

def verify_otp(req, nonce, modulus):
    req = json.loads(req)
    key = bytes.fromhex(req['key'])
    otp = req['otp']
    user = req['user']
    command = req['command']
    data = {
        'user': user,
        'command': command,
        'nonce': nonce
    }
    return generate_otp(key, json.dumps(data).encode(), modulus) == otp
    
def generate_data(user, command, nonce, modulus):
    data = {
        'user': user,
        'command': command,
        'nonce': nonce
    }
    key = os.urandom(128)
    while key in SEEN_KEY:
        key = os.urandom(128)
    if user == 'admin':
        SEEN_KEY.append(key)
    otp = generate_otp(key, json.dumps(data).encode(), modulus)
    data['otp'] = otp
    data['key'] = key.hex()
    data.pop('nonce', None)
    return json.dumps(data)

def execute_command(data, nonce, modulus):
    global required
    if verify_otp(data, nonce, modulus):
        data = json.loads(data)
        command = data['command']
        user = data['user']
        key = bytes.fromhex(data['key'])
        if command == 'test':
            print('Hey! It work :>')
        elif command == 'get_flag':
            if key not in SEEN_KEY and user == 'admin':
                required += 1
                SEEN_KEY.append(key)
                if required == 5:
                    print(flag)
            else:
                required = 0
        else:
            print('Invalid command')
    else:
        print('Verification failed')
        
def menu():
    return '''1. Generate command data
2. Execute Command
3. Exit
Enter choice: '''

if __name__ == "__main__":
    SEEN_KEY = []
    nonce = os.urandom(16).hex()
    attempts = 0
    required = 0
    modulus = getPrime(256)
    print(f'{modulus = }')
    try:
        while attempts < 24:
            choice = int(input(menu()))
            if choice == 1:
                user = input('Enter user: ')
                command = input('Enter command: ')
                print(generate_data(user, command, nonce, modulus))
            elif choice == 2:
                data = input('Enter data: ')
                execute_command(data, nonce, modulus)
            elif choice == 3:
                break
            else:
                print('Invalid choice')
            attempts += 1
    except:
        print('Something went wrong... Or may be you sussss')
    
    
    