import os
from flask import Flask
from dotenv import load_dotenv


# Load env variables
load_dotenv()

# print(f"HOST: {os.getenv('HOST')}")
# print(f"PORT: {os.getenv('PORT')}")


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


# Temp Routes
@app.route("/")
def hello():
    return "hello world!"


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