import string

def caesar_cipher(text, shift):
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

def mixed_alphanet(text: str, keyword: str):
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


