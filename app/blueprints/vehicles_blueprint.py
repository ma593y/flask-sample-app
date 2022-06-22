from flask import Blueprint
from middlewares.authentication_decorator import check_authentication


vehicles_blueprint = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@vehicles_blueprint.before_request
@check_authentication
def before_request(*args, **kwargs):
    pass


@vehicles_blueprint.route("/", methods=["GET"])
def index():
    return "index vehicles..."


@vehicles_blueprint.route("/", methods=["POST"])
def create():
    return "create vehicle..."


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["GET"])
def read(vehicle_id):
    return f"read vehicle {vehicle_id}..."


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["PUT"])
def update(vehicle_id):
    return f"update vehicle {vehicle_id}..."


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["DELETE"])
def delete(vehicle_id):
    return f"delete vehicle {vehicle_id}..."