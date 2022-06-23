from core.database import Session
from marshmallow import ValidationError
from models.vehicles_model import VehiclesModel
from schemas.vehicles_schema import VehiclesSchema
from flask import Blueprint, jsonify, request, Response
from middlewares.authentication_decorator import check_authentication


vehicles_blueprint = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@vehicles_blueprint.before_request
@check_authentication
def before_request(*args, **kwargs):
    pass


@vehicles_blueprint.route("/", methods=["GET"])
def index():
    vehicles = None
    with Session() as db_session:
        vehicles = db_session.query(VehiclesModel).filter().all()

    vehicles_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicles, many=True)
    return jsonify(vehicles_data), 200


@vehicles_blueprint.route("/", methods=["POST"])
def create():
    request_data = request.get_json()
    schema = VehiclesSchema(only=("vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id"))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    vehicle_data = schema.dump(result)
    new_vehicle = VehiclesModel(**vehicle_data)

    db_session = Session()
    db_session.add(new_vehicle)
    db_session.commit()

    db_session.refresh(new_vehicle)
    new_user_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(new_vehicle)
    return new_user_data, 201


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["GET"])
def read(vehicle_id):
    vehicle = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

    if not vehicle:
        return Response(status=204)

    vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicle)
    return jsonify(vehicle_data), 200


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["PUT"])
def update(vehicle_id):
    request_data = request.get_json()
    schema = VehiclesSchema(only=("vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id"))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    vehicle_data = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

        if not vehicle:
            return Response(status=204)
        
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

    return jsonify(vehicle_data), 200


@vehicles_blueprint.route("/<int:vehicle_id>", methods=["DELETE"])
def delete(vehicle_id):
    vehicle_data = None
    with Session() as db_session:
        vehicle = db_session.query(VehiclesModel).filter_by(vehicle_id=vehicle_id).first()

        if not vehicle:
            return Response(status=204)

        vehicle_data = VehiclesSchema(only=("vehicle_id", "vehicle_make", "vehicle_model", "vehicle_color", "vehicle_fuel_type", "vehicle_transmission", "vehicle_year", "vehicle_price", "vehicle_mileage", "vehicle_tank_capacity", "vehicle_engine_capacity", "category_id", "updated_on", "created_on")).dump(vehicle)

        db_session.delete(vehicle)
        db_session.commit()

    return jsonify(vehicle_data), 200


