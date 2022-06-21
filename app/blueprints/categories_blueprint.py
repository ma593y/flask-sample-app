from flask import Blueprint


categories_blueprint = Blueprint("categories", __name__, url_prefix="/categories")


@categories_blueprint.route("/", methods=["GET"])
def index():
    return "index categories..."


@categories_blueprint.route("/", methods=["POST"])
def create():
    return "create category..."


@categories_blueprint.route("/<int:category_id>", methods=["GET"])
def read(category_id):
    return f"read category {category_id}..."


@categories_blueprint.route("/<int:category_id>", methods=["PUT"])
def update(category_id):
    return f"update category {category_id}..."


@categories_blueprint.route("/<int:category_id>", methods=["DELETE"])
def delete(category_id):
    return f"delete category {category_id}..."