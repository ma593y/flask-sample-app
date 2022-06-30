import jwt, os
from functools import wraps
from flask import request, jsonify



def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "Authorization" not in request.headers or "Bearer " not in request.headers.get("Authorization"):
            return jsonify({"message": "Authorization header or Bearer token is missing."}), 401

        token = request.headers.get('Authorization')[7:]
        try:
            payload = jwt.decode(token, os.getenv("RSA_PUBLIC_KEY"), algorithms=["RS512"])
            if not payload["user_is_active"]:
                return jsonify({"message": "User is not active."}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Bearer token is expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Bearer token is invalied."}), 401
        except Exception as e:
            return jsonify({"message": "Unknown error encountered."}), 401
        
        return f(*args, **kwargs)
    return decorated_function


