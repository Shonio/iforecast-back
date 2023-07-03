from functools import wraps

from flask import jsonify

from .custom_exceptions import CustomBadRequest


def handle_error(status_code):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                response = jsonify({"error": str(e)})
                response.status_code = status_code
                return response

        return decorated_function

    return decorator


def init_app(app):
    @app.errorhandler(CustomBadRequest)
    def handle_custom_bad_request(error):
        response = jsonify({"error": error.description})
        response.status_code = error.code
        return response
