from datetime import date
from wsgiref import validate
from core.database_config import Session
from models.categories_model import CategoriesModel
from marshmallow import EXCLUDE, Schema, fields, validate, ValidationError




def check_category_id(category_id):
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter(CategoriesModel.category_id.like(category_id)).all()
        if not category:
            raise ValidationError("Category id does not exists with the given value.")



class VehiclesSchema(Schema):
    vehicle_id = fields.Integer()
    vehicle_make = fields.String(required=True,
        validate = [
            validate.Length(min=3, error="Vehicle make must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle make must contain alphabets only.")
        ]
    )  
    vehicle_model = fields.String(required=True,
        validate = [
            validate.Length(min=3, error="Vehicle model must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z0-9 ]*$", error="Vehicle model must contain alphabets only.")
        ]
    )
    vehicle_color = fields.String(required=True,
        validate = [
            validate.Length(min=3, error="Vehicle color must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle color must contain alphabets only.")
        ]
    )
    vehicle_fuel_type = fields.String(required=True,
        validate = [
            validate.Length(min=3, error="Vehicle fuel type must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle fuel type must contain alphabets only.")
        ]
    )
    vehicle_transmission = fields.String(required=True,
        validate = [
            validate.Length(min=3, error="Vehicle transmission must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle transmission must contain alphabets only.")
        ]
    )
    
    vehicle_year = fields.Integer(required=True,
        validate = [
            validate.Range(min=1990, max=date.today().year, error="Vehicle year value must be between {min} and {max}.")
        ]
    )
    vehicle_price = fields.Integer(required=True,
        validate = [
            validate.Range(min=0, error="Vehicle price value must be greater than or equal to {min}.")
        ]
    )
    vehicle_mileage = fields.Integer(required=True,
        validate = [
            validate.Range(min=0, error="Vehicle mileage value must be greater than or equal to {min}.")
        ]
    )
    vehicle_tank_capacity = fields.Integer(required=True,
        validate = [
            validate.Range(min=0, error="Vehicle tank_capacity value must be greater than or equal to {min}.")
        ]
    )
    vehicle_engine_capacity = fields.Integer(required=True,
        validate = [
            validate.Range(min=0, error="Vehicle engine_capacity value must be greater than or equal to {min}.")
        ]
    )

    category_id = fields.Integer(required=True,
        validate = check_category_id
    )

    updated_on = fields.DateTime()
    created_on = fields.DateTime()
    
    class Meta:
        unknown = EXCLUDE


