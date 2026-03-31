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

from retro_ciphers.poly import Vigenere, Alberti, Beaufort, Autokey, Trithemius


crypto = Blueprint("crypto", __name__)


@crypto.route("/", methods=["GET", "POST"])
def convertor():
    text: str = ""
    algo: str = "caesar"
    keyword: str = ""
    shift: int = 3
    toggle_value : bool = False
    modern_implementation: bool = True
    frequency : int = 50
    result: str | None = None
    cipher_alphabet: str | None = None
    error = None

    if request.method == "POST":
        text: str = request.form.get("text", "")
        algo: str = request.form.get("algo", "caesar")
        action: str = request.form.get("action", "encrypt")
        toggle_value : bool = request.form.get("toggle", False)

        try:
            # Enforce text ONLY if they are actively trying to encrypt/decrypt
            if action in ["encrypt", "decrypt"] and not text:
                raise ValueError("Text is required.")

            cipher_class_map: dict[str, type] = {
                "atbash": Atbash,
                "shift": Shift,
                "caesar": Caesar,
                "rot13": Rot13,
                "mixed_alphabet": MixedAlphabet,
                "simple_substitution": SimpleSubstitution,
                "baconian": Baconian,
                "polybius_square": PolybiusSquare,
                "alberti": Alberti,
                "trithemius": Trithemius,
                "vigenere": Vigenere,
                "beaufort": Beaufort,
                "autokey": Autokey,
            }

            if algo not in cipher_class_map:
                raise KeyError(f"Invalid algorithm: {algo}")

            cipher_class: type = cipher_class_map[algo]

            match algo:
                case "shift":
                    # Handle empty string submissions gracefully
                    shift_val = request.form.get("shift", "").strip()
                    shift = int(shift_val) if shift_val else 3
                    cipher_instance = Shift(shift)

                case "alberti" :
                    modern_implementation = request.form.get("modern-implementation-toggle", False)
                    # Safely get keyword to avoid Flask BadRequestKeyError
                    keyword = request.form.get("keyword", "").strip()
                    frequency = request.form.get("frequency", 50)
                    try:
                        frequency = int(frequency)
                    except ValueError:
                        raise ValueError("Frequency is required.")
                    if not keyword:
                        raise ValueError("Keyword is required.")
                    cipher_instance = cipher_class(key= keyword,frequency=frequency, modern_implementation=modern_implementation)

                case "baconian":
                    modern_implementation = request.form.get("modern-implementation-toggle", False)
                    cipher_instance = cipher_class(modern_implementation=modern_implementation)

                case "simple_substitution":
                    cipher_alphabet = request.form.get("cipher_alphabet", "").strip()

                    if action == "generate":
                        cipher_alphabet = SimpleSubstitution.generate_cipher_alphabet()

                    if not cipher_alphabet:
                        raise ValueError("Alphabet is required for Simple Substitution cipher; generate one.")

                    cipher_instance = SimpleSubstitution(cipher_alphabet)

                case "mixed_alphabet" | "vigenere" | "beaufort" | "autokey":
                    # Safely get keyword to avoid Flask BadRequestKeyError
                    keyword = request.form.get("keyword", "").strip()
                    if not keyword:
                        raise ValueError("Keyword is required.")
                    cipher_instance = cipher_class(keyword)

                case _:
                    cipher_instance = cipher_class()

            # Perform encryption or decryption
            if action == "encrypt":
                result = cipher_instance.cipher(text, omit_non_alpha=toggle_value)
            elif action == "decrypt":
                result = cipher_instance.decipher(text)

        except (ValueError, KeyError) as e:
            error = str(e)

    return render_template(
        "cipher.html",
        text=text,
        algo=algo,
        keyword=keyword,
        shift=shift,
        toggle_value=toggle_value,
        modern_implementation=modern_implementation,
        frequency=frequency,
        result=result,
        cipher_alphabet=cipher_alphabet,
        error=error,
    )
