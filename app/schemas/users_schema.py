from wsgiref import validate
from core.database import Session
from models.users_model import UsersModel
from marshmallow import EXCLUDE, Schema, fields, validate, post_load, ValidationError



def check_user_emailon_signup(email):
    with Session() as db_session:
        user = db_session.query(UsersModel).filter_by(user_email=email).first()
        if user:
            raise ValidationError("User already exists with the given email.")



def check_user_emailon_signin(email):
    with Session() as db_session:
        user = db_session.query(UsersModel).filter_by(user_email=email).first()
        if not user:
            raise ValidationError("User dosen't exists with the given email.")



class UsersSchema(Schema):
    user_id = fields.Integer()
    user_full_name = fields.String(
        required = True,
        validate = [
            validate.Length(min=3, error="User full name must be at least {min} characters long."),
            validate.Regexp(r"[a-zA-Z ]*$", error="User full name must contain alphabets only.")
        ]
    )
    user_hashed_password = fields.String()
    user_is_active = fields.Boolean()
    updated_on = fields.DateTime()
    created_on = fields.DateTime()
    
    class Meta:
        unknown = EXCLUDE



class UsersSignupSchema(UsersSchema, Schema):
    user_email = fields.Email(
        required = True,
        validate = check_user_emailon_signup
    )



class UsersSigninSchema(UsersSchema, Schema):
    user_email = fields.Email(
        required = True,
        validate = check_user_emailon_signin
    )
    user_password = fields.String(
        required = True,
        validate = [
            validate.Length(equal=18, error="User password must be equal to {equal} characters."),
            validate.Regexp(r"[^ ]*$", error="User password must not contain spaces.")
        ]
    )

    @post_load
    def make_user(self, data, **kwargs):
        user = None
        with Session() as db_session:
            user = db_session.query(UsersModel).filter_by(user_email=data["user_email"]).first()
        return user, data

