from flask import Blueprint

bp = Blueprint("hello", __name__, url_prefix="/hello")


@bp.route("/", methods=["GET"])
def hello():
    return "Hello AGAIN BE KIND! This is a mock endpoint!"