from flask import Blueprint, request, render_template

from retro_ciphers.mono import (
    Atbash,
    Shift,
    Caesar,
    Rot13,
    MixedAlphabet,
    SimpleSubstitution,
    Baconian,
    PolybiusSquare,

)

from retro_ciphers.poly import Vigenere, Alberti, Beaufort, Autokey


crypto = Blueprint("crypto", __name__)


@crypto.route("/", methods=["GET", "POST"])
def convertor():
    result : str | None = None
    cipher_alphabet : str | None = None
    error = None

    if request.method == "POST":
        text: str = request.form.get("text", "")
        algo: str  = request.form.get("algo", "caesar")
        action: str = request.form.get("action", "encrypt")

        try:
            # enforce text
            if not text:
                raise ValueError("Text is required.")

            # map algorithm to class
            cipher_class_map: dict[str,type] = {
                "atbash": Atbash,
                "shift": Shift,
                "caesar": Caesar,
                "rot13": Rot13,
                "mixed_alphabet": MixedAlphabet,
                "simple_substitution": SimpleSubstitution,
                "baconian": Baconian,
                "polybius_square": PolybiusSquare,
            }

            # get cipher class from map
            if algo not in cipher_class_map:
                raise KeyError(f"Invalid algorithm: {algo}")
            cipher_class: type = cipher_class_map[algo]

            # handle different algorithms
            match algo:
                case "shift":
                    shift = int(request.form.get("shift", 3))
                    cipher_instance = Shift(shift)
                case "mixed_alphabet":
                    # enforce user to provide a keyword, setting a default keyword is a bad idea.
                    keyword: str = request.form.get("keyword", "")
                    if not keyword:
                        raise ValueError(
                            "Keyword is required for Mixed Alphabet cipher."
                        )
                    cipher_instance = MixedAlphabet(keyword)
                case "simple_substitution":
                    # enforce user to provide one or generate one, use need to know the cipher_alphabet as it is work as a key
                    cipher_alphabet : str = request.form.get("cipher_alphabet", "")
                    
                    # generate a random cipher_alphabet
                    if action == "generate":
                        cipher_alphabet: str = SimpleSubstitution.generate_cipher_alphabet()
                        
                    if not cipher_alphabet:
                        raise ValueError(
                            "Alphabet is required for Simple Substitution cipher; generate one."
                        )
                    cipher_instance = SimpleSubstitution(cipher_alphabet)
                case _:
                    cipher_instance = cipher_class()
                
            # Perform encryption or decryption
            if action == "encrypt":
                result: str = cipher_instance.cipher(text)
            elif action == "decrypt":
                result : str = cipher_instance.decipher(text)

        except (ValueError, KeyError) as e:
            error = str(e)

    return render_template(
        "cipher.html",
        result=result,
        cipher_alphabet=cipher_alphabet,
        error=error,
    )
