# pip install cryptography
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
# pip install pycryptodome
from Crypto.Util.strxor import strxor
import pwn # pip install pwntools

def RSA_encrypt(m, n, e):
	pub_key = rsa.RSAPublicNumbers(e, n).public_key(backend=default_backend())

	c = pub_key.encrypt(m, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None))

	return c

def get_ans(r1, r2):
	m = strxor(r1, r2).hex()
	if 'a' in m:
		return 0
	elif 'b' in m:
		return 1

host, port = 'mc.ax', 31497
m0 = 32*'a'
m1 = 32*'b'
# Prepare dummy
d = 16*b'c'

s = pwn.remote(host,port)
for i in range(128):
	print(f'Attempt: {i}')
	if 'Correct' in s.recvuntil('/128\n').decode('utf-8'):
		print('Success')
	n1 = int(s.recvline().decode('utf-8').split(" ")[-1])
	n2 = int(s.recvline().decode('utf-8').split(" ")[-1])
	# print(f'n1 = {n1}')
	# print(f'n2 = {n2}')
	s.sendline(str('1').encode())
	s.sendline(m0.encode())
	s.sendline(m1.encode())
	result = bytes.fromhex(s.recvline().decode('utf-8').split(" ")[-1])
	s.recv()

	# print('result:', result)
	c1 = result[:256].hex()
	c2 = result[256:].hex()
	# print(f'c1 = {c1}')
	# print(f'c2 = {c2}')
	d1 = RSA_encrypt(d, n1, 65537).hex()
	d2 = RSA_encrypt(d, n2, 65537).hex()
	# print(f'd1 = {d1}')
	# print(f'd2 = {d2}')
	c1d2 = bytes.fromhex(c1+d2).hex()
	d1c2 = bytes.fromhex(d1+c2).hex()
	# print(f'c1d2 = {c1d2}')
	# print(f'd1c2 = {d1c2}')
	s.sendline(str('2').encode())
	# print('After send 2')

	s.recv()
	s.sendline(str(c1d2).encode())
	r1 = bytes.fromhex(s.recvline().decode('utf-8').strip())
	# print(f'r1 = {r1}')

	s.recv()
	s.sendline(str('2').encode())
	s.recv()
	s.sendline(str(d1c2).encode())
	r2 = bytes.fromhex(s.recvline().decode('utf-8').strip())
	# print(f'r2 = {r2}')
	ans = get_ans(r1,r2)
	s.recv()
	s.sendline(str('0').encode())
	s.sendline(str(ans).encode())
	s.recv().decode('utf-8')
 
s.interactive()