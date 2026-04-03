class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")  
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = []
        seen = set()
        for char in key:
            if char not in seen and char in alphabet:
                seen.add(char)
                matrix.append(char)
        
        for char in alphabet:
            if char not in seen:
                seen.add(char)
                matrix.append(char)
                
        playfair_matrix = []
        for i in range(0,25,5):
            playfair_matrix.append(matrix[i:i+5])

        return playfair_matrix
    
    def prepare_text(self, plain_text):
        plain_text = plain_text.upper().replace("J","I")
        plain_text = plain_text.replace(" "," ")
        
        pairs = []
        i=0
        
        while i < len(plain_text):
            a = plain_text[i]
            if i+1 < len(plain_text):
                b=plain_text[i+1]
                if a==b:
                    pairs.append(a+"X")
                    i+=1
                else:
                    pairs.append(a+b)
                    i+=2
            else:
                pairs.append(a+"X")
                i+=1
        return pairs        
     
           

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = self.prepare_text(plain_text)
        encrypted_text = ""

        for pair in plain_text:

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:  
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = self.prepare_text(cipher_text)
        decrypted_text = ""

        for pair in cipher_text:

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:  
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        banro = ""
        for i in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + decrypted_text[i+1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2]
            banro += decrypted_text[-1]


        return banro