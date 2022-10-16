ciphertext1 = b"\xb3y\xf5Ky\xed\x13\xcd\x85U1\xbb\x9c\xd8?A\xe9?P/\xc3/\x97\x97\xbf\xe3\xfam\xb9\x00\xf0_\xf3\x02s\x97\x1b\x87\xeb\t\xda\xe6\x04@0\x9a\xa8\xea\x8b\xa9\x86\x87\x1c-\xeaDI\x8b\xd1v\x1e6!\xc8'\x06_\xd4\xb9".hex()

ciphertext2 = b'\xa6e\xf2M\x10\x9cp\x8f\xcbs\x07\x9e\xc8\xe5\x12r\xd9\x1f]n\xee\x03\x89\x8c\xc0\xca\xd7\x1a\x91E\xe6e\xe3\x1e`\x9d\x02\x80\xfb@\xa8\x92tUD\x81\xeb\xc4\xa6\x84\xad\xda'.hex()

plaintext = b"TODO:\n - ADD HARDER CHALLENGE IN CRYPTO\n - ADD FLAG TO THE CHALLENGE\n".hex()

def xor(hex1, hex2, getAscii = False):
  result = []

  for ind in range(0, len(hex1), 2):
    longIndex = ind
    shortIndex = ind%len(hex2)
    hexChar1 = hex1[longIndex:longIndex+2]
    byte1 = int(hexChar1, 16)

    hexChar2 = hex2[shortIndex:shortIndex+2]
    byte2 = int(hexChar2, 16)

    asciiNum = byte1 ^ byte2
    result.append(chr(asciiNum))


  out = ''.join(result)
  if getAscii:
    print('Result:', out)
    return out
  else:
    out = out.encode('utf-8').hex()
    print('Result:', out)
    return out
    

xored = xor(ciphertext2, ciphertext1)

flag = xor(xored, plaintext, True)