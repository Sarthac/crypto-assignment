from flask import Blueprint, request, jsonify
from ciphers.ciphers import (
    Atbash,
    Baconian,
    Caesar,
    MixedAlphabet,
    PolybiusSquare,
    Rot13,
    Shift,
    SimpleSubstitution,
)

from ciphers.rail_fence import RailFence
from ciphers.columnar_transposition import ColumnarTransposition
from ciphers.scytale_cipher import Scytale

api_bp = Blueprint("api", __name__)

cipher_map = {
    "atbash": Atbash,
    "baconian": Baconian,
    "caesar": Caesar,
    "rot13": Rot13,
    "polybius_square": PolybiusSquare,
    "mixed_alphabet": MixedAlphabet,
    "shift": Shift,
    "simple_substitution": SimpleSubstitution,
    "rail_fence": RailFence,
    "columnar": ColumnarTransposition,
    "scytale": Scytale,
}


@api_bp.route("/api/<cipher_name>", methods=["GET", "POST"])
def api(cipher_name):
    """
    A single API endpoint to handle all supported ciphers.
    It accepts both GET and POST requests.
    """
    if cipher_name not in cipher_map:
        return jsonify({"error": f"Cipher '{cipher_name}' not found."}), 404

    # Use request.args for GET and request.get_json() for POST
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON body."}), 400
    else:
        data = request.args

    # Extract common parameters
    text = data.get("text")
    action = data.get("action", "encrypt")

    if not text:
        return jsonify({"error": "The 'text' parameter is required."}), 400

    if action not in ["encrypt", "decrypt"]:
        return jsonify({"error": "Invalid action. Use 'encrypt' or 'decrypt'."}), 400

    cipher_class = cipher_map[cipher_name]
    cipher_instance = None

    # Handle ciphers with specific initialization requirements
    try:
        match cipher_name:
            # ----------------------
            # substitution ciphers
            # ----------------------
            case "mixed_alphabet":
                keyword = data.get("keyword")
                if not keyword:
                    return (
                        jsonify(
                            {
                                "error": "The 'keyword' parameter is required for mixed_alphabet."
                            }
                        ),
                        400,
                    )
                cipher_instance = cipher_class(keyword)

            case "shift":
                shift_str = data.get("shift")
                if shift_str is None:
                    return (
                        jsonify(
                            {
                                "error": "The 'shift' parameter is required for the rotate cipher."
                            }
                        ),
                        400,
                    )
                try:
                    shift = int(shift_str)
                    cipher_instance = cipher_class(shift)
                except (ValueError, TypeError):
                    return (
                        jsonify(
                            {"error": "The 'shift' parameter must be a valid integer."}
                        ),
                        400,
                    )

            case "simple_substitution":
                key = data.get("key")
                # If a key is provided, use it. Otherwise, the class generates a random one.
                cipher_instance = cipher_class(key)

            # ----------------------
            # transposition ciphers
            # ----------------------

            case "rail_fence":
                key_raw = data.get("key")
                key = (
                    int(key_raw)
                    if isinstance(key_raw, str) and key_raw.isdigit()
                    else 3
                )
                original_text = text
                cipher_instance = cipher_class(text, key)
                text = cipher_instance.create_rail_fence()

            case "columnar":
                keyword = data.get("keyword")
                cipher_instance = cipher_class(keyword)

            case "scytale":
                key_raw = data.get("key")
                key = (
                    int(key_raw)
                    if isinstance(key_raw, str) and key_raw.isdigit()
                    else 3
                )

                cipher_instance = cipher_class(key)
            case _:
                # For ciphers like Atbash, Caesar, Rot13, Baconian, PolybiusSquare
                cipher_instance = cipher_class()

        # Perform the requested action
        if action == "encrypt":
            result = cipher_instance.cipher(text)
        else:  # action == "decrypt"
            result = cipher_instance.decipher(text)

        # returing json
        match cipher_name:
            case "simple_substitution":
                return jsonify(
                    {
                        "text": text,
                        "result": result,
                        "key": "".join(cipher_instance.cipher_alphabets),
                    }
                )

            case "shift":
                return {"text": text, "result": result, "shift": data.get("shift")}

            case "mixed_alphabet":
                return {"text": text, "result": result, "shift": data.get("keyword")}

            case "rail_fence":
                return {"text": original_text, "result": result}

            case _:
                return jsonify({"text": text, "result": result})

    except Exception as e:
        # Generic error handler for any other issues during cipher processing
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
