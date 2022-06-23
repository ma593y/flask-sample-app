# Ropstam-Test-Task-Backend

A backend app server with the following features,
- User sign up using full name and email
- Email randomly generated password on sign up
- Sign in using the user credentials to get JWT token
- Access API endpoints with the issued JWT token
- Data validation on POST/PUT API endpoints


## API endpoints are as follows,
    - Temporary API endpoint,
        - [GET] / : hello world!

    - API endpoints for database status,
        - [GET] /db_status : show database status

    - API endpoints for user signup and signin,
        - [POST] accounts/signup : signup user
        - [POST] accounts/signin : signin user

    - API endpoints for vehicle categories,
        - [GET]    categories/ : list categories
        - [POST]   categories/ : create category
        - [GET]    categories/<category_id> : view category
        - [PUT]    categories/<category_id> : update category
        - [DELETE] categories/<category_id> : delete category
        
    - API endpoints for vehicles,
        - [GET]    vehicles/ : list vehicle
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
    pip install flask sqlalchemy marshmallow PyMySQL[rsa] pyjwt[crypto] python-dotenv
    #or
    pip install -r requirements.txt

  #### 4. Run MySQL database server on docker.
    docker compose up

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