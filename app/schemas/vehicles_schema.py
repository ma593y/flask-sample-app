from wsgiref import validate
from core.database import Session
from models.vehicles_model import VehiclesModel
from marshmallow import EXCLUDE, Schema, fields, validate, post_load, ValidationError



class VehiclesSchema(Schema):
    vehicle_id = fields.Integer()
    vehicle_make = fields.String( required = True,
        validate = [
            validate.Length(min=3, error="Vehicle make must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle make must contain alphabets only.")
        ]
    )  
    vehicle_model = fields.String( required = True,
        validate = [
            validate.Length(min=3, error="Vehicle model must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle model must contain alphabets only.")
        ]
    )
    vehicle_color = fields.String( required = True,
        validate = [
            validate.Length(min=3, error="Vehicle color must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle color must contain alphabets only.")
        ]
    )
    vehicle_fuel_type = fields.String( required = True,
        validate = [
            validate.Length(min=3, error="Vehicle fuel type must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle fuel type must contain alphabets only.")
        ]
    )
    vehicle_transmission = fields.String( required = True,
        validate = [
            validate.Length(min=3, error="Vehicle transmission must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Vehicle transmission must contain alphabets only.")
        ]
    )
    
    vehicle_year = fields.Integer( required = True,
        validate = [validate.Length(equal=4, error="Vehicle year must be at least {equal} characters long.")]
    )
    vehicle_price = fields.Integer( required = True,
        validate = [validate.Length(min=4, error="Vehicle price must be at least {min} characters long.")]
    )
    vehicle_mileage = fields.Integer( required = True,
        validate = [validate.Length(min=6, error="Vehicle mileage must be at least {min} characters long.")]
    )
    vehicle_tank_capacity = fields.Integer( required = True,
        validate = [validate.Length(min=2, error="Vehicle tank capacity must be at least {min} characters long.")]
    )
    vehicle_engine_capacity = fields.Integer( required = True,
        validate = [validate.Length(min=3, error="Vehicle engine capacity must be at least {min} characters long.")]
    )

    # category = fields.String()

    updated_on = fields.DateTime()
    created_on = fields.DateTime()
    
    class Meta:
        unknown = EXCLUDE


