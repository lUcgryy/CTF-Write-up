import urllib.parse

f = open("log.txt", "r")
payloads=  []

while True:
  
  log = f.readline()
  if log == "":
    break
  i = log.find("?username=")
  if i == -1:
    continue
  j = log.find("HTTP/1.1")
 
  params = log[i+1:j-1]
  
  print("Encoded: " + params)
  url = urllib.parse.unquote(params)
  print("Decoded: " +url)
  print("-"*20)
  payloads.append("http://128.199.190.141:5552/index.php?"+params)


with open("./payload.txt", mode='w') as f:
    for i in range(len(payloads)):
        f.write(payloads[i]+"\n")