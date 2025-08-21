from flask import Blueprint, request, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@home_bp.route("/api", methods=["GET"])
def api_home():
    return render_template("api.html")


@home_bp.route("/test", methods=["GET"])
def test_home():
    return render_template("test.html")
