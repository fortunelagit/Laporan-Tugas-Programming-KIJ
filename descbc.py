# %%
#function to convert hex string to binary
def hex_to_bin(str):
    str = str.upper()
    mapping = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    result = ""
    for i in range(len(str)):
        result += mapping[str[i]]
    return result

# %%
#function to convert binary string to hexadecimal
def bin_to_hex(str):
    mapping = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(str), 4):
        ch = ""
        ch += str[i] + str[i + 1] + str[i + 2] + str[i + 3]
        hex = hex + mapping[ch]
 
    return hex

# %%
#initial permutation (IP) table for DES
initial_perm_table = [58, 50, 42, 34, 26, 18, 10, 2,
                    60, 52, 44, 36, 28, 20, 12, 4,
                    62, 54, 46, 38, 30, 22, 14, 6,
                    64, 56, 48, 40, 32, 24, 16, 8,
                    57, 49, 41, 33, 25, 17, 9, 1,
                    59, 51, 43, 35, 27, 19, 11, 3,
                    61, 53, 45, 37, 29, 21, 13, 5,
                    63, 55, 47, 39, 31, 23, 15, 7]

# %%
#permutation function using input table
def permute(text, table, n):
    result = ""
    for i in range(0, n):
        result += text[table[i] - 1]
    return result

# %%
#expansion permutation (E) table for DES
expansion_table = [32, 1, 2, 3, 4, 5, 
                    4, 5, 6, 7, 8, 9, 
                    8, 9, 10, 11, 12, 13, 
                    12, 13, 14, 15, 16, 17,
                    16, 17, 18, 19, 20, 21, 
                    20, 21, 22, 23, 24, 25, 
                    24, 25, 26, 27, 28, 29, 
                    28, 29, 30, 31, 32, 1]

# %%
#parity bit drop table for dropping (8, 16, 24,...) bit in key
parity_drop_table = [57, 49, 41, 33, 25, 17, 9, 1, 
                58, 50, 42, 34, 26, 18, 10, 2, 
                59, 51, 43, 35, 27, 19, 11, 3, 
                60, 52, 44, 36, 63, 55, 47, 39, 
                31, 23, 15, 7, 62, 54, 46, 38, 
                30, 22, 14, 6, 61, 53, 45, 37, 
                29, 21, 13, 5, 28, 20, 12, 4]

# %%
#schedule of left shifts (1 for key round 1, 2, 9, 16)
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# %%
#shift left by appending string 1 to n, then adding [0]
def shift_left(k, n):
    s = ""
    for i in range(n):
        for j in range(1, len(k)):
            s += k[j]
        s = s + k[0]
        k = s
        s = ""
    return k

# %%
#compression permutation table also known as permutation choice two (PC-2) table
key_compression_table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
                        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
                        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
                        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

# %%
#function to prepare 16 round of key
def prepare_key(key):
    #convert into binary
    key = hex_to_bin(key)
    #print(key)
    #permute key into 56 bit by dropping parity bits (bit 8, 16, 24, ...)
    key = permute(key, parity_drop_table, 56)

    #split key into two parts, 28 bit each
    left_key = key[0:28]
    right_key = key[28:56]

    #array to hold 16 round of key
    key_round_bin = []

    for i in range(16):
        #shift according to the shift table scheme
        left_key = shift_left(left_key, shift_table[i])
        right_key = shift_left(right_key, shift_table[i])

        #combine both parts
        combined = left_key + right_key

        #compress key from 56 bit to 48 bit using PC-2 table or compression permutation table
        round_key = permute(combined, key_compression_table, 48)

        #append each round of key
        key_round_bin.append(round_key)
        
    return key_round_bin

# %%
#xor function
def xor(a, b):
    res = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            res += "0"
        else:
            res += "1"
    return res

# %%
#DES S-box table
s_box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

# %%
#function to convert binary into decimal
def bin_to_dec(binary):
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        #2 to the power of each bit, start from most insignificant bit
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

# %%
#function to convert decimal into binary
def dec_to_bin(num):
    res = bin(num).replace("0b", "")
    #pad the front with zero so the len of bianry string is 4n
    if(len(res) % 4 != 0):
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

# %%
#permutation function (P) for DES
permutation_table = [16,  7, 20, 21, 29, 12, 28, 17,
                     1, 15, 23, 26, 5, 18, 31, 10,
                     2,  8, 24, 14, 32, 27,  3,  9,
                     19, 13, 30,  6, 22, 11,  4, 25]

# %%
#function for 16 round of encryption
def encrypt_round(left, right, key_round, i):
    #expand right text from 32 bit to 48 bit using expansion permutation table
    right_expand = permute(right, expansion_table, 48)

    #xor the 48 bit right text with current round key
    xor_r = xor(right_expand, key_round[i])

    #transform each 6 bits into 4 bits, resulting from 48 bits into total of 32 bits
    sbox_str = ""
    for j in range(0, 8):
        row = bin_to_dec(int(xor_r[j * 6] + xor_r[j * 6 + 5]))
        col = bin_to_dec(int(xor_r[j * 6 + 1] + xor_r[j * 6 + 2] + xor_r[j * 6 + 3] + xor_r[j * 6 + 4]))
        val = s_box[j][row][col]
        sbox_str += dec_to_bin(val)
    #permutation of s-box output
    sbox_str = permute(sbox_str, permutation_table, 32)

    #xor left text with x-box output
    result = xor(left, sbox_str)
    #save result for next round
    left = result

    #swap left text and right text
    if(i != 15):
        temp = left
        left = right
        right = temp

    return [left, right]

# %%
#table for final permutation, also known as inverse initial permutation (IP^-1) table
final_permutation_table = [40, 8, 48, 16, 56, 24, 64, 32,
                            39, 7, 47, 15, 55, 23, 63, 31,
                            38, 6, 46, 14, 54, 22, 62, 30,
                            37, 5, 45, 13, 53, 21, 61, 29,
                            36, 4, 44, 12, 52, 20, 60, 28,
                            35, 3, 43, 11, 51, 19, 59, 27,
                            34, 2, 42, 10, 50, 18, 58, 26,
                            33, 1, 41, 9, 49, 17, 57, 25]

# %%
def encrypt(plaintext, key):
    print("ENCRYPTION\n")
    print("PLAINTEXT = " + plaintext)
    print("KEY = " + key + "\n")
    plaintext = hex_to_bin(plaintext)

    #initial permutation, permute plaintext into 64 bit text
    plaintext = permute(plaintext, initial_perm_table, 64)
    print("INITIAL PERMUTATION: " + bin_to_hex(plaintext))

    #split plaintext into two, left and right, 32 bit each
    left_text = plaintext[0:32]
    right_text = plaintext[32:64]
    print("LEFT0: " + bin_to_hex(left_text) + " | "+ "RIGHT0: " + bin_to_hex(right_text))
    key_round = prepare_key(key)

    #start 16 round of encryption process
    for i in range(0, 16):
        left_text, right_text = encrypt_round(left_text, right_text, key_round, i)
        print("ROUND {}: {} {} {}".format(i+1, bin_to_hex(left_text), bin_to_hex(right_text), bin_to_hex(key_round[i])))

    #combine left and right text
    round_result = left_text + right_text

    #final permutation
    ciphertext = permute(round_result, final_permutation_table, 64)

    #convert to hexadecimal
    ciphertext = bin_to_hex(ciphertext)
    print("\n" + "CIPHERTEXT = " + ciphertext + "\n_________________________________")
    return ciphertext

# %%
def decrypt(ciphertext, key):
    print("DECRYPTION\n")
    print("CIPHERTEXT = " + ciphertext)
    print("KEY = " + key + "\n")
    ciphertext = hex_to_bin(ciphertext)

    #initial permutation, permute plaintext into 64 bit text
    ciphertext = permute(ciphertext, initial_perm_table, 64)
    print("INITIAL PERMUTATION: " + bin_to_hex(ciphertext))

    #split plaintext into two, left and right, 32 bit each
    left_text = ciphertext[0:32]
    right_text = ciphertext[32:64]
    print("LEFT0: " + bin_to_hex(left_text) + " | "+ "RIGHT0: " + bin_to_hex(right_text))

    #the only part different from encryption process, the order of key is reversed
    key_round = prepare_key(key)[::-1]

    #start 16 round of decryption process
    for i in range(0, 16):
        left_text, right_text = encrypt_round(left_text, right_text, key_round, i)
        print("ROUND {}: {} {} {}".format(i+1, bin_to_hex(left_text), bin_to_hex(right_text), bin_to_hex(key_round[i])))

    #combine left and right text
    round_result = left_text + right_text

    #final permutation
    plaintext = permute(round_result, final_permutation_table, 64)

    #convert to hexadecimal
    plaintext = bin_to_hex(plaintext)
    print("\n" + "PLAINTEXT = " + ciphertext + "\n_________________________________")
    return plaintext