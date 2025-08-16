from ciphers.rail_fence import RailFence
from ciphers.columnar_transposition import ColumnarTransposition
from ciphers.scytale_cipher import Scytale

# Encrypt
t = RailFence("sarthak, this is a test ! ..", 3)
rail = t.create_rail_fence()
enc = t.cipher(rail)
print(enc)  # e.g., shatark

# Decrypt
td = RailFence(enc, 3)
dec = td.decipher()
print(dec)  # sarthak


# ----------------------
# Example usage
# ----------------------
cipher = ColumnarTransposition("LOKEY")

plaintext = "HELLOWORLDTHISISANEX"
enc = cipher.cipher(plaintext)
print("Ciphertext:", enc)

dec = cipher.decipher(enc)
print("Plaintext:", dec)


# ----------------------
# Example usage
# ----------------------
cipher = Scytale(3)

plaintext = "HELLOWORLDTHISISANEX"
enc = cipher.cipher(plaintext)
print("Ciphertext:", enc)

dec = cipher.decipher(enc)
print("Plaintext:", dec)
