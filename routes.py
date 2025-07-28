import string, random

class SubstitutionCipher:

    def __init__(self, cipher_alphabets: list) -> None:
        self.cipher_alphabets = cipher_alphabets
        self.mapping = self.cipher_mapping()

    # creating mapping of alphanets to cipher_alphanets
    # examples : for atbash cipher
    # 'a' : 'z'
    # 'b  : 'y'
    # 'c' : 'x'

    def cipher_mapping(self):
        mapping = {
            'lowercase': {},
            'uppercase': {}
        }
        for i, val in enumerate(string.ascii_lowercase):
            mapping['lowercase'][val] = self.cipher_alphabets[i]
            mapping['uppercase'][val.upper()] = self.cipher_alphabets[i].upper()
        
        return mapping


    def cipher(self, text: str ) -> str:
        cipher_text = ''
        for letter in text:
            if letter.islower():
                cipher_text += self.mapping['lowercase'].get(letter, letter) # two letter parameters because if the letter doesn't include in the mapping, it will fallback to default i.e second letter parameter which is original letter
            elif letter.isupper():
                cipher_text += self.mapping['uppercase'].get(letter, letter)
            else:
                cipher_text += letter
        return cipher_text

    
    def decipher(self, text : str) -> str:
        # Reverse the mapping for both cases
        inverse_lower = {v: k for k, v in self.mapping['lowercase'].items()}
        inverse_upper = {v: k for k, v in self.mapping['uppercase'].items()}

        plain_text = ''
        for letter in text:
            if letter.islower():
                plain_text += inverse_lower.get(letter, letter)
            elif letter.isupper():
                plain_text += inverse_upper.get(letter, letter)
            else:
                plain_text += letter
        return plain_text


class MixedAlphabet(SubstitutionCipher):

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword
        cipher_alphabets = self.mixed_cipher_alphabets()
        super().__init__(cipher_alphabets)

    def mixed_cipher_alphabets(self):
        # Make keyword unique while preserving order
        unique_keyword = list(dict.fromkeys(self.keyword))
        
        alphabets = string.ascii_lowercase
        cipher_alphabet = unique_keyword

        for letter in alphabets:
            if letter not in cipher_alphabet:
                cipher_alphabet.append(letter)

        return cipher_alphabet    


class Atbash(SubstitutionCipher):

    def __init__(self) -> None:
        reverse_lowercase =  list(string.ascii_lowercase[::-1])
        super().__init__(reverse_lowercase)
        

class SimpleSubstitution(SubstitutionCipher):
    def __init__(self) -> None:
        cipher_alphabets = random.sample(string.ascii_lowercase, k=26)
        super().__init__(cipher_alphabets)
    

class Rotate(SubstitutionCipher):
    def __init__(self, shift: int) -> None:
        self.shift = shift
        cipher_alphabets = self.shift_to()
        super().__init__(cipher_alphabets)

    def shift_to(self):
        # small letter in ASCII start from 97, in ASCII a = 97
        return [chr((ord(char) - 97 + self.shift) % 26 + 97) for char in string.ascii_lowercase]
            

class Caesar(Rotate):
    def __init__(self, shift: int =3) -> None:
        super().__init__(shift)


class Rot13(Rotate):
    def __init__(self, shift: int =13) -> None:
        super().__init__(shift)

class Baconian(SubstitutionCipher):
    modern_baconian_cipher = [
    'aaaaa',  # a
    'aaaab',  # b
    'aaaba',  # c
    'aaabb',  # d
    'aabaa',  # e
    'aabab',  # f
    'aabba',  # g
    'aabbb',  # h
    'abaaa',  # i
    'abaab',  # j
    'ababa',  # k
    'ababb',  # l
    'abbaa',  # m
    'abbab',  # n
    'abbba',  # o
    'abbbb',  # p
    'baaaa',  # q
    'baaab',  # r
    'baaba',  # s
    'baabb',  # t
    'babaa',  # u
    'babab',  # v
    'babba',  # w
    'babbb',  # x
    'bbaaa',  # y
    'bbaab'   # z
    ]

    old_baconian_cipher = [
    'aaaaa',  # A
    'aaaab',  # B
    'aaaba',  # C
    'aaabb',  # D
    'aabaa',  # E
    'aabab',  # F
    'aabba',  # G
    'aabbb',  # H
    'abaaa',  # I / J
    'abaaa',   # I / J
    'abaab',  # K
    'ababa',  # L
    'ababb',  # M
    'abbaa',  # N
    'abbab',  # O
    'abbba',  # P
    'abbbb',  # Q
    'baaaa',  # R
    'baaab',  # S
    'baaba',  # T
    'baabb',  # U / V
    'baabb',  # U / V
    'babaa',  # W
    'babab',  # X
    'babba',  # Y
    'babbb'   # Z
]


    def __init__(self, cipher_alphabet : list = None , modern_implementation=True) -> None:
        if modern_implementation:
            cipher_alphabet = self.modern_baconian_cipher
        else:
            cipher_alphabet = self.old_baconian_cipher

        super().__init__(cipher_alphabet)
    
    def decipher(self, text: str) -> str:
        inverse_lower = {v: k for k, v in self.mapping['lowercase'].items()}
        inverse_upper = {v: k for k, v in self.mapping['uppercase'].items()}
        plain_text = ''
        i = 0
        word_length = 5
        while i < len(text):
            if text[i] in [' ', '\n', '\t']:  # You can expand this list for more
                plain_text += text[i]
                i += 1
            else:
                block = text[i:i+word_length]
                if block[0].islower():
                    plain_text += inverse_lower.get(block, '?')
                else:
                    plain_text += inverse_upper.get(block, '?')
                i += word_length
        return plain_text

class PolybiusSquare(SubstitutionCipher):
    cipher_alphabets = ['00','01','02','03','04',
                        '10','11','12','13','14',
                        '20','21','22','23','24',
                        '30','31','32','33','34',
                        '40','41','42','43','44',
                        '51'
            ]
    
    def __init__(self) -> None:
        super().__init__(self.cipher_alphabets)

    def cipher(self, text: str ) -> str:
        cipher_text = ''
        for letter in text:
            if letter.islower():
                cipher_text += self.mapping['lowercase'].get(letter, letter) # two letter parameters because if the letter doesn't include in the mapping, it will fallback to default i.e second letter parameter which is original letter
            elif letter.isupper():
                cipher_text += self.mapping['uppercase'].get(letter, letter)
            elif letter.isnumeric():
                cipher_text += ''
            else:
                cipher_text += letter
        return cipher_text
       
    def decipher(self, text: str) -> str:
        inverse_lower = {v: k for k, v in self.mapping['lowercase'].items()}
        inverse_upper = {v: k for k, v in self.mapping['uppercase'].items()}
        plain_text = ''
        i = 0
        word_length = 2
        while i < len(text):
            if text[i] in [' ', '\n', '\t']:  # You can expand this list for more
                plain_text += text[i]
                i += 1
            else:
                block = text[i:i+word_length]
                plain_text += inverse_lower.get(block, '?')
                i += word_length
        return plain_text
    

caesar = PolybiusSquare()
text = 'hello world 234'
cipher = caesar.cipher(text)
decipher = caesar.decipher(cipher)

print(f'Original : {text}')
print(f'Cipher : {cipher}')
print(f'Decipher : {decipher}')

num = '234'
print(num.isnumeric)