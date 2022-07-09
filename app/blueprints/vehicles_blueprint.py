from sqlalchemy import and_
from core.database_config import Session
from marshmallow import ValidationError
from flask import Blueprint, jsonify, request
from models.vehicles_model import VehiclesModel
from schemas.vehicles_schema import VehiclesSchema
from utils.vehicles import get_vehicles_query_filters
from middlewares.authentication_decorator import check_authentication


vehicles_blueprint = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@vehicles_blueprint.before_request
@check_authentication
def before_request(*args, **kwargs):
    pass


@vehicles_blueprint.route("/", methods=["GET"])
def index():
    # filtering...
    query_filters = get_vehicles_query_filters(request.args)

    # pagination and sorting...
    offset, limit, sort, sort_by = (
        request.args.get("offset", default=0, type=int),
        request.args.get("limit", default=10, type=int),
        request.args.get("sort", default='asc', type=str),
        request.args.get("sort_by", default='id', type=str)
    )

    order_by = []
    if sort_by == 'year':
        order_by.append(VehiclesModel.vehicle_year.desc()) if sort == 'desc' else order_by.append(VehiclesModel.vehicle_year.asc())
    elif sort_by == 'price':
        order_by.append(VehiclesModel.vehicle_price.desc()) if sort == 'desc' else order_by.append(VehiclesModel.vehicle_price.asc())
    else:
        order_by.append(VehiclesModel.vehicle_id.desc()) if sort == 'desc' else order_by.append(VehiclesModel.vehicle_id.asc())

    vehicles = None
    with Session() as db_session:
        vehicles = db_session.query(VehiclesModel).filter(and_(*query_filters)).order_by(*order_by).offset(offset).limit(limit)
        total_count = db_session.query(VehiclesModel).count()

    vehicles_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicles, many=True)
    return jsonify(
        {
            "message": "A list of vehicles founded in database.",
            "data": {
                "vehicles":vehicles_data,
                "count": len(vehicles_data),
                "total": total_count
            }
        }
    ), 200


@vehicles_blueprint.route("/", methods=["POST"])
def create():
    request_data = request.get_json()
    schema = VehiclesSchema(only=("vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id"))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(
            {
                "message": "There are some data validation errors.",
                "errors": err.messages
            }
        ), 400
    
    vehicle_data = schema.dump(result)
    new_vehicle = VehiclesModel(**vehicle_data)

    db_session = Session()
    db_session.add(new_vehicle)
    db_session.commit()

    db_session.refresh(new_vehicle)
    new_vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(new_vehicle)
    return jsonify(
        {
            "message": "The vehicle has been created.",
            "data": {"vehicle": new_vehicle_data}
        }
    ), 201


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["GET"])
def read(vehicle_id):
    vehicle = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

    if not vehicle:
        return jsonify({"message": "The vehicle is not found in database."}), 204

    vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicle)
    return jsonify(
        {
            "message": "The vehicle has been found in database.",
            "data": {"vehicle": vehicle_data}
        }
    ), 200


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["PUT"])
def update(vehicle_id):
    request_data = request.get_json()
    schema = VehiclesSchema(only=("vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id"))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(
            {
                "message": "There are some data validation errors.",
                "errors": err.messages
            }
        ), 400
    
    vehicle_data = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

        if not vehicle:
            return jsonify({"message": "The vehicle is not found in database."}), 204
        
        # update values here
        vehicle.vehicle_make = result["vehicle_make"]
        vehicle.vehicle_model = result["vehicle_model"]
        vehicle.vehicle_color = result["vehicle_color"]
        vehicle.vehicle_fuel_type = result["vehicle_fuel_type"]
        vehicle.vehicle_transmission = result["vehicle_transmission"]
        vehicle.vehicle_year = result["vehicle_year"]
        vehicle.vehicle_price = result["vehicle_price"]
        vehicle.vehicle_mileage = result["vehicle_mileage"]
        vehicle.vehicle_tank_capacity = result["vehicle_tank_capacity"]
        vehicle.vehicle_engine_capacity = result["vehicle_engine_capacity"]
        vehicle.category_id = result["category_id"]
        
        db_session.commit()
        
        db_session.refresh(vehicle)
        vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicle)

    return jsonify(
        {
            "message": "The vehicle has been updated in database.",
            "data": {"vehicle": vehicle_data}
        }
    ), 200


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["DELETE"])
def delete(vehicle_id):
    vehicle_data = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

        if not vehicle:
            return jsonify({"message": "The vehicle is not found in database."}), 204

        vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicle)

        db_session.delete(vehicle)
        db_session.commit()

    return jsonify(
        {
            "message": "The vehicle has been deleted from database.",
            "data": {"vehicle": vehicle_data}
        }
    ), 200


