# %%
def caps(input):
    #capitalizing all letter
    return input.upper()

# %%
def make_key_matrix(key):
    key_array = []
    
    #append key first
    for i in key:
        #special rule for letter J
        if i == "J": i = "I"
        
        #check if the letter already in array
        if i not in key_array:
            key_array.append(i)

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #then the rest of alphabet
    for i in alphabet:
        if i not in key:
            key_array.append(i)

    #make into 5x5 matrix
    key_matrix = []
    while key_array != []:
        key_matrix.append(key_array[:5])
        key_array = key_array[5:]
        #print(key_array)
            
    #print(key_matrix)
    return key_matrix

# %%
def prepare_text(plaintext):
    array_text=[]
    prev = ""
    for i in plaintext:
        #special rule for letter J
        if i == "J": i = "I"

        #get last element if array not empty
        if len(array_text)>0: 
            prev = array_text[-1]

        #append x if current and prev is the same
        if prev == i:
            array_text.append("X")

        #append the rest of text except space character
        if i != " ":
            array_text.append(i)
        else:
            continue
        
    #if text is odd length, add Z
    if len(array_text)%2:
        array_text.append("Z")
    
    return array_text
    


# %%
def split_text(plaintext):
    array_text = prepare_text(plaintext)

    #split into 2d array [][2]
    two_letter_array = []
    while array_text != []:
        two_letter_array.append(array_text[:2])
        array_text = array_text[2:]
        #print(array_text)
    #print(two_letter_array)
    return two_letter_array
    
            

# %%
def search(matrix_key, letter):
    i=0
    j=0
    #search for letter in key matrix
    for i in range(5):
        for j in range(5):
            if letter == matrix_key[i][j]:
                index = [i,j]
                #print(index)
                return index
    

# %%
def add_index(num):
    if num == 4:
        return 0
    else:
        return num+1

# %%
def encryption_rules(first_index, second_index):
    #print(first_index, second_index)

    #if in the same column, shift down
    if first_index[1] == second_index[1]:
        first_index[0] = add_index(first_index[0])
        second_index[0] = add_index(second_index[0])

    #if in the same row, shift right
    if first_index[0] == second_index[0]:
        first_index[1] = add_index(first_index[1])
        second_index[1] = add_index(second_index[1])

    #else, switch using rectangle, horizontal opposite
    else:
        hold = first_index[1]
        first_index[1] = second_index[1]
        second_index[1] = hold
    
    return [first_index, second_index]
    

# %%
def start_encrypt(matrix_key, plaintext):
    encrypted_text = ""

    length = len(plaintext)
    for i in range(length):
        #get index in matrix key
        first_index = search(matrix_key, plaintext[i][0])
        second_index = search(matrix_key, plaintext[i][1])

        #apply encryption rules
        new_first, new_second = encryption_rules(first_index, second_index)
        
        #append encrypted letters to text
        encrypted_text += matrix_key[new_first[0]][new_first[1]]
        encrypted_text += matrix_key[new_second[0]][new_second[1]]

        #print(encrypted_text)

    return encrypted_text


# %%
def encrypt(key, plaintext):
    #make both key and plaintext all capitalized
    key = caps(key)
    plaintext = caps(plaintext)

    print("KEY: ", key)
    print("PLAINTEXT: ", plaintext)

    #make key matrix
    matrix = make_key_matrix(key)
    print("KEY MATRIX = ", matrix)
    #split text into 2 letter each
    ready_text = split_text(plaintext)
    result = start_encrypt(matrix, ready_text)

    return result


# %%
key = "xjvwoiagjerigniesor"
plaintext = "jdnvgsoerqwoekfoermgkw"

# key = input("Key: ")
# plaintext = input("Plain Text: ")

encryptedtext = encrypt(key, plaintext)
print("ENCRYPTED TEXT:", encryptedtext)


