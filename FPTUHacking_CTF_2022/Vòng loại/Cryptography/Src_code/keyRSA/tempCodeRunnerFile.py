 user_d = int(input("\nEnter your key : \n"))
    if user_d != d:
        if pow(ct,user_d,n) == pow(ct,d,n):
            print(flag)