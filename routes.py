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



caesar = SimpleSubstitution()
text = 'hello world'
cipher = caesar.cipher(text)
decipher = caesar.decipher(cipher)

print(f'Original : {text}')
print(f'Cipher : {cipher}')
print(f'Decipher : {decipher}')

