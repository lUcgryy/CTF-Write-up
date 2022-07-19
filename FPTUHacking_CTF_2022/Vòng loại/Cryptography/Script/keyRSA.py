import pwn
host, port = '103.245.249.76', 49160

s = pwn.remote(host, port)
s.recv().decode("utf-8") # Do you want to try your own key? [ y/n ] : )
s.sendline(str('y').encode()) # Điền 'y' vào
s.recv().decode("utf-8") # Sure, here are your keys
s.recvline().decode("utf-8") # \n
s.recvline().decode("utf-8") # e = 65537
e = 65537
n = int(s.recvline().decode("utf-8").split(" ")[-1]) # lấy giá trị của n
p = int(s.recvline().decode("utf-8").split(" ")[-1]) # lấy giá trị của x

q = n // p

phi = (p-1) * (q-1)
d = pow(e,-1,phi) 

s.recvline().decode("utf-8") # Enter your key:

i = d + 2*phi

s.sendline(str(int(i)).encode()) # Điền đáp án vào.

print(s.recv().decode("utf-8")) # In ra flag


s.close()