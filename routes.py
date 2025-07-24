import string, random

def caesar_cipher(text: str, shift: int = 3) ->str :
    result = ''
    for char in text:
        if char.isupper():
            # capital letter in ASCII start from 97, in ASCII A = 65
            # I would like to set letter A to 1 so -65 and to calculate modular arthmatic using moduls
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            # small letter in ASCII start from 97, in ASCII a = 97
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            result += char
    return result

def mixed_alphanet(text: str, keyword: str) -> str:
    # Convert to uppercase
    keyword = keyword.upper()
    text = text.upper()

    # Make keyword unique while preserving order
    unique_keyword = ""
    for char in keyword:
        if char not in unique_keyword:
            unique_keyword += char

    # Create ciphertext alphabet
    plaintext_alphabet = list(string.ascii_uppercase)
    ciphertext_alphabet = list(unique_keyword)

    for letter in plaintext_alphabet:
        if letter not in ciphertext_alphabet:
            ciphertext_alphabet.append(letter)

    # Cipher the plaintext using the ciphertext alphabet
    cipher_text = ""
    for j in text:
        if j in plaintext_alphabet:
            i = plaintext_alphabet.index(j)
            cipher_text += ciphertext_alphabet[i]
        else:
            cipher_text += j  # handle non-alphabet characters

    return cipher_text


def atbash_en(text: str) -> str:
    cipher =''
    for char in text:
        
        if char.islower():
            # asci lowercase alphabets start at 97 i.e a, and 122 is z
            cipher+= chr(122 - (ord(char)- 97))

        elif char.isupper():
            # ascii uppercase start at 65 i.e A, and 90 is Z
            cipher+= chr(90 - (ord(char) - 65))

        else:
            cipher+=char # for symobols and numbers

    return cipher


def atbash_de(text: str) -> str:
    decipher = ''
    for char in text:
        if char.islower():
            decipher += chr(122-ord(char) + 97)
        
        elif char.isupper():
            decipher += chr(90-ord(char)+65)
        
        else:
            decipher += char
    
    return decipher

class SimpleSubstitution:
    def simple_random_key_gen(self):
        return random.sample(string.ascii_lowercase, k=26)
    
    def letter_mapping(self, key: list) -> dict:
        mapping = {}
        for i, letter in enumerate(string.ascii_lowercase):
            mapping[letter] = key[i]
        return mapping

    def simple_substitution_en(self, text: str, mapping: dict) -> str:
        cipher_text = ''
        for letter in text:
            cipher_text+=mapping.get(letter, letter) # two letter becuase, second letter is for fallback if the letter is not found in mapping, this is going to using because text could have symbols & letters in it
        return cipher_text
    
    def decipher_simple_substitution(self, text: str, mapping: dict) -> str:
        # Reverse the mapping
        inverse_mapping = {v: k for k, v in mapping.items()}

        plain_text = ''
        for letter in text:
            plain_text += inverse_mapping.get(letter, letter)
        return plain_text


        



