import os
from flask import Flask
from dotenv import load_dotenv


# Load env variables
load_dotenv()


# Create flask app
app = Flask(__name__)


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


# Create Database Tables
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
    return f"This endpoint does not exist.", 404


# Temp Routes
@app.route("/")
def hello():
    return "hello world!", 200

# Endpoint for Database Status
@app.route("/db")
def db():
    db_session = Session()

    db_status = None
    try:
        db_session.execute("select NOW();").all()[0][0]
        db_status = "Up"
    except:
        db_status = "Down"

    return f"Database Status: {db_status}", 200


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