from flask import Flask, render_template, request, jsonify
from routes import *

def get_text_from_request():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
    else:
        text = request.args.get('text')
    
    if not text:
        return jsonify({'error' : "Missing 'text' field in request."}), 400
    
    return text



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        shift = int(request.form["shift"])

        rotate = Rotate(shift)
        if request.form["action"] == "encrypt":
            result = rotate.cipher(text)
        else:
            result = rotate.decipher(text)
    return render_template('index.html', result=result)


@app.route("/about")
def about():
    return "this will be about page"

@app.route('/api')
def api():
    return render_template('api.html')
   
@app.route("/api/mix")
def mix():
    # print("TEXT:", repr(text))
    # pr    int("KEY:", repr(key))
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
        key = data.get('key')
    else:
        text = request.args.get('text')
        key = request.args.get('key')
    
    if not text:
        return jsonify({'error' : "Missing 'text' field in request."}), 400
    

    cipher = MixedAlphabet(key)
    cipher_text = cipher.cipher(text)
    return jsonify({'text' : cipher_text,
                    'key' : key})

@app.route("/api/atbash_en", methods= ['POST', 'GET'])
def atbash_encrypt():
    text = get_text_from_request()
    atbash = Atbash()
    atbash_cipher_alphabets=atbash.cipher_alphabets
    cipher_text = atbash.cipher(text)
    return jsonify({'text' : text,
                    'cipher_text' : cipher_text })

@app.route("/api/atbash_de", methods = ['POST', 'GET'])
def atbash_decrypt():
    
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
    else:
        text = request.args.get('text')
    
    if not text:
        return jsonify({'error' : "Missing 'text' field in request."}), 400
    atbash = Atbash()
    decipher_text = atbash.decipher(text)
    return jsonify({'text' : text,
                    'cipher_text' : decipher_text })

@app.route("/api/simple_en", methods=['POST','GET'])
def simple_substitution_encrypt():
    if request.method == "POST":
        data = request.get_json()
        text = data.get('text')
    else:
        text = request.args.get('text')

    if not text:
        return jsonify({'error' : "Missing 'text' field in request."}), 400

    cipher = SimpleSubstitution()
    ans = cipher.cipher(text)
    cipher_key = cipher.cipher_alphabets
    return jsonify({'text': text,
                    'cipher_key': cipher_key, 
                    'ciphertext': ans})


if __name__ == "__main__":
    app.run(debug=True)
