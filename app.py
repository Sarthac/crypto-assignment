from flask import Flask, render_template, request
from routes import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        shift = int(request.form["shift"])
        if request.form["action"] == "encrypt":
            result = caesar_cipher(text, shift)
        else:
            result = caesar_cipher(text, -shift)
    return render_template('index.html', result=result)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/shift/<string:text>/<int:shift>")
def shift(text,shift):
    return caesar_cipher(text,shift)

@app.route("/mix/<string:text>/<string:key>")
def mix(text,key):
    # print("TEXT:", repr(text))
    # print("KEY:", repr(key))
    return mixed_alphanet(text,key)

@app.route("/atbash_en/<string:text>")
def atbash_encrypt(text):
    return atbash_en(text)

@app.route("/atbash_de/<string:text>")
def atbash_decrypt(text):
    return atbash_de(text)

if __name__ == "__main__":
    app.run(debug=True)
