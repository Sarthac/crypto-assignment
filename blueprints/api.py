from flask import Blueprint, request, jsonify
from ciphers import (
    Atbash,
    Baconian,
    Caesar,
    MixedAlphabet,
    PolybiusSquare,
    Rot13,
    Shift,
    SimpleSubstitution,
)

api_bp = Blueprint("api", __name__)

# Map API names to their corresponding cipher classes
cipher_map = {
    "atbash": Atbash,
    "baconian": Baconian,
    "caesar": Caesar,
    "mixed_alphabet": MixedAlphabet,
    "polybius_square": PolybiusSquare,
    "rot13": Rot13,
    "shift": Shift,
    "simple_substitution": SimpleSubstitution,
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

    try:
        # Handle ciphers with specific initialization requirements
        if cipher_name == "mixed_alphabet":
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

        elif cipher_name == "shift":
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

        elif cipher_name == "simple_substitution":
            key = data.get("key")
            # If a key is provided, use it. Otherwise, the class generates a random one.
            cipher_instance = cipher_class(key)

        else:
            # For ciphers like Atbash, Caesar, Rot13, Baconian, PolybiusSquare
            cipher_instance = cipher_class()

        # Perform the requested action
        if action == "encrypt":
            result = cipher_instance.cipher(text)
        else:  # action == "decrypt"
            result = cipher_instance.decipher(text)

        # Include the key in the response for SimpleSubstitution for clarity
        if cipher_name == "simple_substitution":
            return jsonify(
                {
                    "text": text,
                    "result": result,
                    "key": "".join(cipher_instance.cipher_alphabets),
                }
            )
        elif cipher_name == "shift":
            return {"text": text, "result": result, "shift": data.get("shift")}

        elif cipher_name == "mixed_alphabet":
            return {"text": text, "result": result, "shift": data.get("keyword")}

        return jsonify({"text": text, "result": result})

    except Exception as e:
        # Generic error handler for any other issues during cipher processing
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

