from functools import wraps

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.models.user.user import User


def admin_required():

    def decorator(fn):

        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):

            user_id = get_jwt_identity()

            user = User.query.get(user_id)

            if not user:
                return {
                    "message": "User not found."
                }, 404


            if user.role != "admin":
                return {
                    "message": "Admin access required."
                }, 403


            return fn(*args, **kwargs)

        return wrapper

    return decorator