# Flask-Sample-App

A flask app with the following features and concepts implemented,
    
    - User sign up using full name and email
    - Email randomly generated password on sign up
    - Sign in the user using randomly generated password
    - Token based authentication for the RESTful APIs
    - Filtering, Pagination and Sorting for RESTful APIs
    - Flask, SQLAlchemy, Marshmallow based RESTful CRUD APIs
    - Data validation on POST/PUT RESTful APIs
    - Users session management with Redis
    - Redis connection pool configuariton and handling
    - SQLAlchemy connection pool configuariton and handling
    - Flask based app project folders and files structure

## App Tech Stack:

The app is using following tools and technologies,

| Tools & Technologies      | Description  |
| :-------------: |:-------------|
| [Flask](https://flask.palletsprojects.com/) | A micro web framework based on Python. |
| [MySQL](https://www.mysql.com/) | An open-source relational database. |
| [SQLAlchemy](https://www.sqlalchemy.org/) | An open-source object-relational mapper for python. |
| [Marshmallow](https://marshmallow.readthedocs.io/) | A python library for data validation, serialization and deserialization. |
| [Redis](https://redis.io/) | An open source in-memory data structure store. |
| [Docker](https://hub.docker.com/) | An open source containerization platform. |

## Project folders and files structure:
    
    flask-sample-app/                  # Project foler
        app/
            middlewares/                        # It contains decorator files.
                __init__.py
                middleware_files.py
            blueprints/                         # It contains restful api endpoints files.
                __init__.py
                blueprints_files.py
            schemas/                            # It contains schemas files for data validation, serialization and desrialization.
                __init__.py
                schemas_files.py
            models/                             # It contains ORM models files.
                __init__.py
                models_files.py
            utils/                              # It contains common utils funcs files.
                __init__.py
                utils_files.py
            core/                               # It contains core settings files for App or database.
                __init__.py
                core_files.py
            main.py                             # It's the main app file.
        .env
        requirements.txt
        docker-compose.yml

## Postman collection:

The [RESTful APIs](https://www.postman.com/ma593y/workspace/flask-sample-app/collection/14268727-93cfcfd1-0e67-40d1-9c6e-e442e26d900d?ctx=documentation) postman collection for the sample project is available as well as the [documentation](https://www.postman.com/ma593y/workspace/flask-sample-app/documentation/14268727-93cfcfd1-0e67-40d1-9c6e-e442e26d900d).

## RESTful API endpoints:

The RESTful API endpoints are as follows,

    - Temporary API endpoint,
        - [GET] / : hello world!

    - RESTful API endpoints for database status,
        - [GET] /db_status : show database status

    - RESTful API endpoints for signup/signin/signout,
        - [POST] accounts/signup  : signup user
        - [POST] accounts/signin  : signin user
        - [GET]  accounts/signout : signout user

    - RESTful API endpoints for users session management,
        - [GET]    accounts/sessions : user sessions count including current
        - [DELETE] accounts/sessions : delete user sessions except current

    - RESTful API endpoints for vehicle categories,
        - [GET]    categories/ : list categories
        - [POST]   categories/ : create category
        - [GET]    categories/<category_id> : view category
        - [PUT]    categories/<category_id> : update category
        - [DELETE] categories/<category_id> : delete category

    - RESTful API endpoints for vehicles,
        - [GET]    vehicles/ : list vehicles
        - [POST]   vehicles/ : create vehicle
        - [GET]    vehicles/<vehicle_id> : view vehicle
        - [PUT]    vehicles/<vehicle_id> : update vehicle
        - [DELETE] vehicles/<vehicle_id> : delete vehicle 

## To run app on a local machine:

  #### 1. Create virtualenv in the project directory(first time only).
    virtualenv venv

  #### 2. Activate virtualenv(each time).
    source venv/bin/activate

  #### 3. Install libraries(first time only).
    pip install flask sqlalchemy marshmallow PyMySQL[rsa] pyjwt[crypto] python-dotenv flask-cors
    #or
    pip install -r requirements.txt

  #### 4. Run MySQL database server on docker.
    docker compose up -d

  #### 5. Create and set following environment variables in .env file.
    # Set flask variables.
    HOST = '0.0.0.0'
    PORT = 5000

    # Set database variables.
    DB_HOST = 'DB_HOST'
    DB_NAME = 'DB_NAME'
    DB_PORT = 'DB_PORT'
    DB_USERNAME = 'DB_USERNAME'
    DB_PASSWORD = 'DB_PASSWORD'

    # Set mail server variables.
    MAIL_SERVER = 'MAIL_SERVER'
    MAIL_PORT = 'MAIL_PORT'
    EMAIL_ADDRESS = 'EMAIL_ADDRESS'
    EMAIL_PASSWORD = 'EMAIL_PASSWORD'

    # Set RSA512 encryption keys.
    RSA_PRIVATE_KEY = 'RSA_PRIVATE_KEY'
    RSA_PUBLIC_KEY = 'RSA_PUBLIC_KEY'

  #### 6. Set FLASK_ENV variable to developemnt.
    export FLASK_ENV=development

  #### 7. Run flask app.
    python app/main.py