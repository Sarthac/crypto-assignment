from flask import Blueprint, request, render_template
from ciphers.hashing import get_str_hash, get_file_hash

hashing_bp = Blueprint("hashing", __name__)


@hashing_bp.route("/hashing", methods=["GET", "POST"])
def hashing():
    result = None
    text = None
    integrity = None

    if request.method == "POST":
        if "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            file_hash_values = get_file_hash(file)
            sha256_hash = file_hash_values.get("sha256")
            print("testing")

            print(request.form.get("hash-value"))
            print(request.form.get("hash"))

            if request.form.get("hash-value"):
                user_hash_value = request.form.get("hash-value")
                print(request.form.get("hash-value"))
                integrity = True if user_hash_value == sha256_hash else False
            else:
                result = file_hash_values

        else:
            text = request.form.get("text", "")
            result = get_str_hash(text)

    return render_template(
        "hashing.html", result=result, text=text, integrity=integrity
    )
