from marshmallow import ValidationError
from core.database_config import Session
from flask import Blueprint, jsonify, request
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
    # filtering...
    name = request.args.get("name", default='', type=str).strip().lower()

    query_filters = []
    if name:
        query_filters.append(CategoriesModel.category_name.like(f"%{name}%"))
    
    # pagination and sorting...
    offset, limit, sort, sort_by = (
        request.args.get("offset", default=0, type=int),
        request.args.get("limit", default=10, type=int),
        request.args.get("sort", default='asc', type=str),
        request.args.get("sort_by", default='id', type=str)
    )
    
    order_by = []
    if sort_by == 'name':
        order_by.append(CategoriesModel.category_name.desc()) if sort == 'desc' else order_by.append(CategoriesModel.category_name.asc())
    else:
        order_by.append(CategoriesModel.category_id.desc()) if sort == 'desc' else order_by.append(CategoriesModel.category_id.asc())

    categories = None
    with Session() as db_session:
        categories = db_session.query(CategoriesModel).filter(*query_filters).order_by(*order_by).offset(offset).limit(limit)
        total_count = db_session.query(CategoriesModel).count()

    categories_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(categories, many=True)
    return jsonify(
        {
            "message": "A list of categories founded in database.",
            "data": {
                "categories":categories_data,
                "count": len(categories_data),
                "total": total_count
            }
        }
    ), 200


@categories_blueprint.route("/", methods=["POST"])
def create():
    request_data = request.get_json()
    schema = CategoriesSchema(only=("category_name",))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(
            {
                "message": "There are some data validation errors.",
                "errors": err.messages
            }
        ), 400
    
    category_data = schema.dump(result)
    new_category = CategoriesModel(**category_data)

    db_session = Session()
    db_session.add(new_category)
    db_session.commit()

    db_session.refresh(new_category)
    new_category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(new_category)
    return jsonify(
        {
            "message": "The category has been created.",
            "data": {"category": new_category_data}
        }
    ), 201


@categories_blueprint.route("/<int:category_id>", methods=["GET"])
def read(category_id):
    category = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

    if not category:
        return jsonify({"message": "The category is not found in database."}), 204

    category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)
    return jsonify(
        {
            "message": "The category has been found in database.",
            "data": {"category": category_data}
        }
    ), 200


@categories_blueprint.route("/<int:category_id>", methods=["PUT"])
def update(category_id):
    request_data = request.get_json()
    schema = CategoriesSchema(only=("category_name",))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(
            {
                "message": "There are some data validation errors.",
                "errors": err.messages
            }
        ), 400
    
    category_data = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

        if not category:
            return jsonify({"message": "The category is not found in database."}), 204
        
        category.category_name = result["category_name"]
        db_session.commit()
        
        db_session.refresh(category)
        category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)

    return jsonify(
        {
            "message": "The category has been updated in database.",
            "data": {"category": category_data}
        }
    ), 200


@categories_blueprint.route("/<int:category_id>", methods=["DELETE"])
def delete(category_id):
    category_data = None
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter_by(category_id=category_id).first()

        if not category:
            return jsonify({"message": "The category is not found in database."}), 204

        category_data = CategoriesSchema(only=("category_id", "category_name", "updated_on", "created_on")).dump(category)

        db_session.delete(category)
        db_session.commit()

    return jsonify(
        {
            "message": "The category has been deleted from database.",
            "data": {"category": category_data}
        }
    ), 200


