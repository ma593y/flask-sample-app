import jwt, os
from functools import wraps
from flask import request, abort



def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "Authorization" not in request.headers or "Bearer " not in request.headers.get("Authorization"):
            abort(401)

        token = request.headers.get('Authorization')[7:]
        try:
            payload = jwt.decode(token, os.getenv("RSA_PUBLIC_KEY"), algorithms=["RS512"])
            print(payload)
            if not payload["user_is_active"]:
                abort(401)
        except jwt.ExpiredSignatureError:
            abort(401)
        except jwt.InvalidTokenError:
            abort(401)
        
        return f(*args, **kwargs)
    return decorated_function


