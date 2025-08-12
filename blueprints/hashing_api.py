from flask import Blueprint, request, jsonify
from hashing import get_str_hash

hashing_api_bp = Blueprint("hashing_api_bp", __name__)


@hashing_api_bp.route("/api/hashing", methods=["POST", "GET"])
def hashing_api():

    # assignning text depening on request method
    if request.method == "POST":
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON body."}), 400
        text = data.get("text")
    else:
        text = request.args.get("text") 

    # validating if the text parameter isn't passed by the user
    if text is None:
        return jsonify({"error": "Missing 'text' paramerter."}), 400
    if not isinstance(text, str):
        return jsonify({"error": "'text' parameter must be a string."}), 400

    result = get_str_hash(text)

    return jsonify({"text": text, "result": result}), 200
