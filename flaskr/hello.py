from flask import Blueprint

bp = Blueprint("hello", __name__, url_prefix="/hello")


@bp.route("/", methods=["GET"])
def hello():
    return "Hello! This is a mock endpoint! :)"


@bp.route("/greeting", methods=["GET"])
def hello2():
    return "Hello! This is yet another one test endpoint"