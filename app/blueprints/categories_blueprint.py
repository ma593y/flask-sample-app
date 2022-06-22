from flask import Blueprint, Response, jsonify, request, abort
from core.database import Session
from marshmallow import ValidationError
from models.categories_model import CategoriesModel
from schemas.categories_schema import CategoriesSchema
from middlewares.authentication_decorator import check_authentication


categories_blueprint = Blueprint("categories", __name__, url_prefix="/categories")


@categories_blueprint.before_request
@check_authentication
def before_request(*args, **kwargs):
    pass


@categories_blueprint.route("/", methods=["GET"])
def index():
    categories = None
    with Session() as db_session:
        categories = db_session.query(CategoriesModel).filter().all()

    categories_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(categories, many=True)

    return jsonify(categories_data), 200


@categories_blueprint.route("/", methods=["POST"])
def create():
    request_data = request.get_json()
    schema = CategoriesSchema(only=("category_name",))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    category_data = schema.dump(result)
    new_category = CategoriesModel(**category_data)

    db_session = Session()
    db_session.add(new_category)
    db_session.commit()

    db_session.refresh(new_category)
    new_user_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(new_category)
    return new_user_data, 201


@categories_blueprint.route("/<int:category_id>", methods=["GET"])
def read(category_id):
    category = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

    if not category:
        return Response(status=204)

    category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)

    return jsonify(category_data), 200


@categories_blueprint.route("/<int:category_id>", methods=["PUT"])
def update(category_id):
    request_data = request.get_json()
    schema = CategoriesSchema(only=("category_name",))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    category_data = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

        if not category:
            return Response(status=204)
        
        category.category_name = result["category_name"]
        db_session.commit()
        
        db_session.refresh(category)
        category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)

    return jsonify(category_data), 200


@categories_blueprint.route("/<int:category_id>", methods=["DELETE"])
def delete(category_id):
    category_data = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

        if not category:
            return Response(status=204)

        category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)

        db_session.delete(category)
        db_session.commit()

    return jsonify(category_data), 200