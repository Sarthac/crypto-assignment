from flask import Flask, render_template, request

app = Flask(__name__)

def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char.isupper():
            # capital letter in ASCII start from 97, in ASCII A = 65
            # I would like to set letter A to 1 so -65 and to calculate modular arthmatic using moduls
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            # small letter in ASCII start from 97, in ASCII a = 97
            result += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            result += char
    return result

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


if __name__ == "__main__":
    app.run(debug=True)
