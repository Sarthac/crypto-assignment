from flask import Blueprint, request, render_template
from ciphers.hashing import get_str_hash, get_file_hash

hashing_bp = Blueprint("hashing", __name__)


@hashing_bp.route("/hashing", methods=["GET", "POST"])
def hashing():
    result = None
    text = None

    if request.method == "POST":
        if "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            result = get_file_hash(file)
        else:
            text = request.form.get("text", "")
            result = get_str_hash(text)

    return render_template("hashing.html", result=result, text=text)
