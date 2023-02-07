import pwn # pip install pwntools

host, port = 'mc.ax', 31493
m0 = 32*'a'
m1 = 32*'b'

s = pwn.remote(host,port)
for i in range(128):
	print(f'Attempt: {i}')
	if 'Correct' in s.recv().decode('utf-8'):
		print('Success')
	s.sendline(str('1').encode())
	s.sendline(m0.encode())
	s.sendline(m1.encode())
	c = s.recvline().decode('utf-8').split(" ")[-1]
	s.recv().decode('utf-8')

	# print('cipher:', c)
	s.sendline(str('2').encode())
	# print('After send 2')
	s.recv()
	s.send(str(c).encode())
	m = str(s.recvline().decode('utf-8'))
	if 'a' in m:
		ans = 0
	elif 'b' in m:
		ans = 1
	s.recv()
	s.sendline(str('0').encode())
	s.sendline(str(ans).encode())
	s.recv().decode('utf-8')

s.interactive()