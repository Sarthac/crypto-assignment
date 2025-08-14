from flask import Blueprint, render_template, request, send_file
from stegano import lsb
import io

from ciphers.ciphers import MixedAlphabet

steganography_bp = Blueprint(
    "steganography", __name__, template_folder="templates", static_folder="static"
)


@steganography_bp.route("/steganography", methods=["GET", "POST"])
def steganography():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file part", 400
        file = request.files["image"]
        if file.filename == "":
            return "No selected file", 400

        keyword = request.form.get("keyword")
        mix = MixedAlphabet(keyword)

        action = request.form.get("action")

        if file:
            if action == "hide":
                text = request.form.get("text", "hello world")
                cipher = mix.cipher(text)

                # Create an in-memory bytes buffer
                buffer = io.BytesIO()
                # Hide the message in the image and save it to the buffer
                secret_image = lsb.hide(file, cipher)
                secret_image.save(buffer, "PNG")
                buffer.seek(0)  # Rewind the buffer

                return send_file(
                    buffer,
                    as_attachment=True,
                    download_name=f"{file.filename}-secret.png",
                    mimetype="image/png",
                )
            elif action == "show":
                keyword = request.form.get("keyword")
                try:
                    message = lsb.reveal(file)
                    message = mix.decipher(message)
                except Exception as e:
                    message = "No hidden message found or error in revealing."
                return render_template("steganography.html", message=message)

    return render_template("steganography.html")
