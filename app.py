from flask import Flask

from blueprints.home import home_bp
from blueprints.cipher import cipher_bp
from blueprints.steganography import steganography_bp
from blueprints.api import api_bp
from blueprints.hashing_api import hashing_api_bp
from blueprints.hashing import hashing_bp


app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(cipher_bp)
app.register_blueprint(steganography_bp)
app.register_blueprint(api_bp)
app.register_blueprint(hashing_api_bp)
app.register_blueprint(hashing_bp)


if __name__ == "__main__":
    app.run(debug=True)
