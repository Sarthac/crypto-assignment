from ciphers.rail_fence import RailFence
from ciphers.columnar_transposition import ColumnarTransposition


# Encrypt
t = RailFence("sarthak, this is a test ! ..", 3)
rail = t.create_rail_fence()
enc = t.encrypt_with_rail_fence(rail)
print(enc)  # e.g., shatark

# Decrypt
td = RailFence(enc, 3)
dec = td.decrypt_with_rail_fence()
print(dec)  # sarthak


# ----------------------
# Example usage
# ----------------------
cipher = ColumnarTransposition("LOKEY")

plaintext = "HELLOWORLDTHISISANEX"
enc = cipher.encrypt(plaintext)
print("Ciphertext:", enc)

dec = cipher.decrypt(enc)
print("Plaintext:", dec)
