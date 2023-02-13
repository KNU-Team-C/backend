from flask import Blueprint

bp = Blueprint("hello", __name__, url_prefix="/hello")


@bp.route("/", methods=["GET"])
def hello():
    return "Hello AGAIN DOUBLE TIME! This is a mock endpoint!"