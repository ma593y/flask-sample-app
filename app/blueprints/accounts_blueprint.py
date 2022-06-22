from unittest import result
from flask import Blueprint, request
from marshmallow import ValidationError
from core.database import Session
from models.users_model import UsersModel
from schemas.users_schema import UsersSignupSchema, UsersSigninSchema
from utils.common import generate_random_password, email_password_to_user, generate_jwt_token


accounts_blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_blueprint.route("/signup", methods=["POST"])
def signup():
    request_data = request.get_json()
    schema = UsersSignupSchema(only=("user_email", "user_full_name"))
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    user_data = schema.dump(result)
    new_user = UsersModel(**user_data)
    random_password = generate_random_password()
    new_user.set_hashed_password(random_password)

    db_session = Session()
    db_session.add(new_user)
    db_session.commit()
    email_password_to_user(new_user.user_email, random_password)

    db_session.refresh(new_user)
    new_user_data = UsersSignupSchema(only=("user_id", "user_email", "user_full_name", "user_is_active", "created_on")).dump(new_user)
    return new_user_data, 201


@accounts_blueprint.route("/signin", methods=["POST"])
def signin():
    request_data = request.get_json()
    schema = UsersSigninSchema(only=("user_email", "user_password"))
    try:
        user, result = schema.load(request_data)
    except ValidationError as err:
        return err.messages, 400
    
    if not user.check_hashed_password(result["user_password"]):
        return {"user_password":["User password is incorrect."]}, 401

    user_data = UsersSigninSchema(only=("user_id", "user_email", "user_full_name", "user_is_active", "created_on")).dump(user)
    bearer_token = generate_jwt_token(user_data)
    return {"bearer_token": bearer_token}, 200