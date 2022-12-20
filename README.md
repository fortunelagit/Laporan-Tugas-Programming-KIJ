# Laporan-Tugas-Programming-KIJ
Playfair Cipher, DES-CBC, DAA

Anggota Kelompok: 

Khaela Fortunela		05111940000057

Fajar Satria			05111940000083

Riki Wahyu			05111940000188


A. Playfair Cipher
  1. Introduction

Playfair Cipher adalah teknik enkripsi simetris menggunakan substitusi digram. Pada implementasinya, Playfair Cipher terdiri dari proses sebagai berikut.

      a. Membuat key menjadi matrix 5x5
      
      b. Padding plaintext dan menjadikan plaintext menjadi array yang terdiri dari 2 huruf
      
      c. Melakukan proses enkripsi

  2. Code and Comment
      a. Membuat key menjadi matrix 5x5.
      ```
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
      ```
      b. Padding plaintext dan menjadikan plaintext menjadi array yang terdiri dari 2 huruf.
      ```
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

      def split_text(plaintext):
          array_text = prepare_text(plaintext)

          #split into 2d array [][2]
          two_letter_array = []
          while array_text != []:
              two_letter_array.append(array_text[:2])
              array_text = array_text[2:]
          return two_letter_array
      ```
      c. Melakukan proses enkripsi
      ```
      def encryption_rules(first_index, second_index):
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
          return encrypted_text
      ```
  3. Operasional


B. DES - CBC

  1. Introduction
  
    DES (Data Encryption Standard) adalah algoritma enkripsi dengan key simetris. DES-CBC (Cipher Block Chaining) merupakan implementasi DES menggunakan mode operasi enkripsi per blok dengan ukuran yang tetap. Pada implementasinya, DES-CBC secara garis besar terdiri dari proses sebagai berikut:
  
    a. Pembuatan key untuk 16 round
    
    b. Initial permutation dari plaintext
    
    c. Proses enkripsi 16 round
    
    d. Final permutation

  2. Code and Comment
    a. Pembuatan key untuk 16 round
      1) Convert key menjadi binary string.
      
      2) Permutasi key dengan menghilangkan parity bits (bit 8, 16, 24, ..) menggunakan tabel parity bit drop.
      
      3) Membagi key menjadi dua bagian.
      
      4) Shift kedua bagian sesuai schedule left shift.

      5) Gabungkan kedua bagian dan kompresi dari 56 bit menjadi 48 bit menggunakan tabel PC-2.
      
      6) Simpan key ke dalam array.
      ```
      #function to prepare 16 round of key
      def prepare_key(key):
          #convert into binary
          key = hex_to_bin(key)

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
        ```
        
    b. Initial permutation dari plaintext
      
       Permutasi awal dari plaintext menggunakan tabel Initial Permutation (IP).
       ```
        def encrypt(plaintext, key):
            ...
            plaintext = permute(plaintext, initial_perm_table, 64)
            ...
        ```
    c. Proses enkripsi 16 round
    1) Bagi plaintext menjadi 2 bagian, left dan right.
    
    2) Loop untuk 16 round:

        a) Expand right text dari 32 bit menjadi 48 bit dengan tabel expansion permutation (E).

        b) Melakukan XOR antara right text dengan key round sekarang.

        c) Menggunakan tabel S-Box, transformasi tiap 6 bit menjadi 4 bit, sehingga di akhir berubah dari 48 bit menjadi 32 bit.

        d) Lakukan XOR antara left text dan hasil dari transformasi S-Box.
        
        e) Simpan hasil sebagai left text (untuk round selanjutnya).
        
        f) Swap right text dan left text.
        ```
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

        def encrypt(plaintext, key):
            ...
            left_text = plaintext[0:32]
            right_text = plaintext[32:64])

            for i in range(0, 16):
                left_text, right_text = encrypt_round(left_text, right_text, key_round, i)
            ...
        ```
  d. Final permutation
  
     Dilakukan permutasi final menggunakan tabel inverse initial permutation (IP^-1).
      ```
      def encrypt(plaintext, key):
          ...
          ciphertext = permute(round_result, final_permutation_table, 64)
          ...
      ```
  e. Tambahan: Proses Decrypt
  
      Proses decrypt memiliki langkah yang sama dengan enkripsi, perbedaan ada di round key yang digunakan. Pada proses decrypt, urutan round key di reverse. 
      ```
      def decrypt(ciphertext, key):
          ...
          key_round = prepare_key(key)[::-1]
          ...
      ```
  3. Operasional


C. DAA
  1. Introduction
  
      DAA (Data Authentication Algorithm) adalah MAC (Message Authentication Code) berbasis DES yang cukup banyak digunakan. Algoritma ini menggunakan mode CBC dari operasi DES. Dengan menggunakan algoritma enkripsi DES (E) dan secret key (K),  nilai dari data authentication code (DAC) dapat dikalkulasikan. Nilai DAC diambil dari ON, dengan N adalah jumlah bit plaintext dibagi menjadi 64 bit block.

  Proses DAA secara garis besar terdiri dari:

      a. Operasi enkripsi blok pertama O(1)
      
      b. Untuk N kali:
      
          1) Proses padding string DN menjadi 64 bit, apabila masih kurang dari 64 bit.
          
          2) XOR antara D(N) dan O(N-1).
          
          3) Proses enkripsi dari hasil XOR antara D(N) dan O(N-1).
          
      c. Mengambil DAC dari bit O(N).

  2. Code and Comment
      ```
      import descbc as des #import descbc.py as library of function

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
          counter = 64 - len(dn)

          #pad with 0 until it’s 64 bit
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
      ```

  3. Operasional


