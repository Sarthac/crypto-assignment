from flask import Flask

from blueprints.main import crypto

app = Flask(__name__)
app.register_blueprint(crypto)


if __name__ == "__main__":
    app.run()
