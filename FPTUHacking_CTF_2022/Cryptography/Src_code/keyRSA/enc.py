from Crypto.Util.number import bytes_to_long, getPrime

flag = b'<REDACTED>'

p, q = getPrime(512), getPrime(512)
n = p * q
e = 65537

msg = bytes_to_long(flag)

assert n > msg
ct = pow(msg,e,n)

phi = (p-1) * (q-1)
d = pow(e,-1,phi)

yn = input(b'Do you want to try your own key? [ y/n ] : ) ')
if yn == 'y':
    print('\nSure, here are your keys \n')
    print(f'\ne = {e}')
    print(f'\nn = {n}')
    print(f'\nx = {p % (n // 2)}')

    user_d = int(input("\nEnter your key : \n"))
    if user_d != d:
        if pow(ct,user_d,n) == pow(ct,d,n):
            print(flag)
        else:
            print('Better luck next time !!')
            exit(0)
    else:
        print("Sorry you can't use my key, or maybe our keys were similar this time, try again !!")
        exit(0)
else:
    print('See you next time')
    exit(0)
