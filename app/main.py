import os
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv


# Load env variables
load_dotenv()


# Create flask app
app = Flask(__name__)
CORS(app)


# Fix Cors Issues
@app.before_request
def before_request_func():
    if request.method == "OPTIONS": # CORS preflight
        response = make_response()
        return response


# Configurations
if app.config["ENV"] == "production":
    app.config.from_object("core.config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("core.config.TestingConfig")
else:
    app.config.from_object("core.config.DevelopmentConfig")

print(f"\n-> ENV is set to: {app.config['ENV']}\n")


# Import Database Configurations & Models
from core.database import engine, Session, Base
from models.users_model import UsersModel
from models.vehicles_model import VehiclesModel
from models.categories_model import CategoriesModel


# Create/Drop Database Tables
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# SQLAlchemy session handling
@app.teardown_appcontext
def shutdown_session(*args, **kwargs):
    print(
        " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n",
        f"before: {engine.pool.status()}"
    )
    Session.remove()
    print(
        f" after:  {engine.pool.status()}\n",
        " - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ",
    )


# 404 Error Handler
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "This endpoint doesn't exists."}), 404


# Temp Routes
@app.route("/")
def hello():
    return jsonify({"message":"hello world!"}), 200

# Endpoint for Database Status
@app.route("/db_status")
def db():
    db_session = Session()
    try:
        db_session.execute("select NOW();").all()[0][0]
        return jsonify({"message": "Database is working fine."}), 200
    except:
        return jsonify({"message": "Something is wrong with database."}), 503


# Import blueprints
from blueprints.accounts_blueprint import accounts_blueprint
from blueprints.categories_blueprint import categories_blueprint
from blueprints.vehicles_blueprint import vehicles_blueprint


# Register blueprints to flask app
app.register_blueprint(accounts_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(vehicles_blueprint)


# Run flask app
if __name__=="__main__":
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))