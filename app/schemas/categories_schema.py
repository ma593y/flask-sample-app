from wsgiref import validate
from core.database import Session
from models.categories_model import CategoriesModel
from marshmallow import EXCLUDE, Schema, fields, validate, ValidationError



def check_category_name(category_name):
    with Session() as db_session:
        category = db_session.query(CategoriesModel).filter(CategoriesModel.category_name.like(category_name)).all()
        if category:
            raise ValidationError("Category name already exists with the given value.")



class CategoriesSchema(Schema):
    category_id = fields.Integer()
    category_name = fields.String(
        required = True,
        validate = [
            validate.Length(min=3, error="Category name must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="Category name must contain alphabets only."),
            check_category_name
        ]
    )

    updated_on = fields.DateTime()
    created_on = fields.DateTime()
    
    class Meta:
        unknown = EXCLUDE


