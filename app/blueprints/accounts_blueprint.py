from flask import Blueprint


accounts_blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_blueprint.route("/signup", methods=["POST"])
def signup():
    return "signup..."


@accounts_blueprint.route("/signin", methods=["POST"])
def signin():
    return "signin..."