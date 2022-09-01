import urllib.parse

f = open("log.txt", "r")

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