import base64
ciphertext = '3HM0BXWSN0XtBDdzV3YfNTbwM3eDJ1U='
ciphertext.replace('=', '')
ciphertext = ciphertext[::-1] + "="
print(base64.b64decode(ciphertext).decode('utf-8'))
