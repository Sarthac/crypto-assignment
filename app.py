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
        if request.form["action"] == "encrypt":
            result = caesar_cipher(text, shift)
        else:
            result = caesar_cipher(text, -shift)
    return render_template('index.html', result=result)


@app.route("/about")
def about():
    return "this will be about page"

@app.route('/api')
def api():
    return render_template('api.html')

@app.route("/api/shift/<string:text>/<int:shift>")
def shift(text,shift):
    return caesar_cipher(text,shift)

@app.route("/api/mix/<string:text>/<string:key>")
def mix(text,key):
    # print("TEXT:", repr(text))
    # print("KEY:", repr(key))
    return mixed_alphanet(text,key)

@app.route("/api/atbash_en", methods= ['POST', 'GET'])
def atbash_encrypt():
    text = get_text_from_request()
    cipher_text = atbash_en(text)
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
    
    decipher_text = atbash_de(text)
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
    key = cipher.simple_random_key_gen()
    cipher_key = ''.join(key)
    mapping = cipher.letter_mapping(key)
    ans = cipher.simple_substitution_en(text,mapping)
    return jsonify({'text': text,
                    'cipher_key': cipher_key,  
                    'mapping': mapping, 
                    'ciphertext': ans})


if __name__ == "__main__":
    app.run(debug=True)
