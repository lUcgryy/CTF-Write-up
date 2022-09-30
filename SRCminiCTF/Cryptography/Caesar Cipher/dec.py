#caesar cipher brute force
with open("cipher.txt") as f:
    cipher = f.readlines()
    for line in cipher:
        for i in range(26):
            flag = ''
            for c in line:
                if c.isupper():
                    flag += chr((ord(c) - i - 65) % 26 + 65)
                elif c.islower():
                    flag += chr((ord(c) - i - 97) % 26 + 97)
                else:
                    flag += c
            if 'SRC{' in flag:
                print(flag)
                exit(0)