import descbc as des
 
plaintext = "123456ABCDEF1234123456ABCDEF1234"
key = "AABBCCDDEEFF1234"
 
#take first 64 bit of text (16 hex code)
d1 = plaintext[0:16]
plaintext = plaintext[16:]
result = []
result.append(des.encrypt(d1, key))
 
length = len(plaintext)
for i in range(0, 16, length):
    #take subsequent 64 bit of text (16 hex code)
    dn = plaintext[i:i+16]
    dn = des.hex_to_bin(dn)
 
    #pad with 0 until it’s 64 bit
    counter = 64 - len(dn)
    for i in range(0, counter):
        dn += '0'
 
    #xor the current input plaintext with previous result
    text = des.xor(dn, des.hex_to_bin(result[i]))
 
    #append to array of result
    result.append(des.encrypt(des.bin_to_hex(text), key))
 
#get 16 bit of last result (size of dac is 16 ≤ x ≤ 64)
dac = des.hex_to_bin(result[-1])
dac = dac[0:16]
print("Data Authentication Code: " + dac + " | " + des.bin_to_hex(dac))