from flask import Blueprint, request, render_template

from ciphers.ciphers import (
    Atbash,
    Baconian,
    Caesar,
    MixedAlphabet,
    PolybiusSquare,
    Rot13,
    Rotate,
    SimpleSubstitution,
)

from ciphers.rail_fence import RailFence
from ciphers.columnar_transposition import ColumnarTransposition
from ciphers.scytale_cipher import Scytale

cipher_bp = Blueprint("cipher", __name__)


@cipher_bp.route("/cipher", methods=["GET", "POST"])
def cipher():
    result = None
    cipher_alphabets = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "")
        algo = request.form.get("algo")
        action = request.form.get("action")

        try:
            cipher_class_map = {
                "atbash": Atbash,
                "baconian": Baconian,
                "caesar": Caesar,
                "rot13": Rot13,
                "polybius_square": PolybiusSquare,
                "mixed_alphabet": MixedAlphabet,
                "shift": Rotate,
                "simple_substitution": SimpleSubstitution,
                "rail_fence": RailFence,
                "columnar": ColumnarTransposition,
                "scytale": Scytale,
            }

            cipher_class = cipher_class_map.get(algo)

            if not cipher_class:
                raise ValueError(f"Invalid algorithm: {algo}")

            # Handle actions and cipher-specific parameters
            if action == "generate" and algo == "simple_substitution":
                cipher_alphabets = "".join(
                    SimpleSubstitution.generate_cipher_alphabets()
                )
            else:
                # Instantiate the correct cipher with its required parameters
                if algo == "shift":
                    shift = int(request.form.get("shift", 3))
                    cipher_instance = Rotate(shift)
                elif algo == "mixed_alphabet":
                    keyword = request.form.get("keyword", "")
                    if not keyword:
                        raise ValueError(
                            "Keyword is required for Mixed Alphabet cipher."
                        )
                    cipher_instance = MixedAlphabet(keyword)
                elif algo == "simple_substitution":
                    user_alphabet = request.form.get("cipher_alphabets")
                    cipher_instance = SimpleSubstitution(user_alphabet)
                    # Persist the user-provided or generated alphabet in the form
                    cipher_alphabets = "".join(cipher_instance.cipher_alphabets)

                elif algo == "rail_fence":
                    key_raw = request.form.get("key", 3)
                    key = int(key_raw)
                    cipher_instance = RailFence(text, key)
                    text = cipher_instance.create_rail_fence()

                elif algo == "columnar":
                    keyword = request.form.get("keyword", "")
                    if not keyword:
                        raise ValueError(
                            "Keyword is required for Columnar Transposition cipher."
                        )
                    cipher_instance = ColumnarTransposition(keyword)

                elif algo == "scytale":
                    key_raw = request.form.get("key", 3)
                    key = int(key_raw)
                    cipher_instance = Scytale(key)

                else:
                    cipher_instance = cipher_class()

                # Perform encryption or decryption
                if action == "encrypt":
                    result = cipher_instance.cipher(text)
                elif action == "decrypt":
                    result = cipher_instance.decipher(text)

        except (ValueError, TypeError, KeyError) as e:
            error = f"Error: {e}"
            print(error)
            result = "An error occurred. Please check your input."

    return render_template(
        "cipher.html",
        result=result,
        cipher_alphabets=cipher_alphabets,
        error=error,
    )
