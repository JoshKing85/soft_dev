from functools import wraps
from flask import request, abort, current_app, session
import jwt


def validate_jwt(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        # Retrieve JWT from browser cookie
        token = request.cookies.get("access_token")

        if not token:
            abort(401)

        # Verify JWT signature, expiry and required claims
        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"require": ["sub", "iat", "exp"]}
            )

        except jwt.InvalidTokenError:
            abort(401)

        # Verify JWT user matches the active session
        if str(session.get("user_id")) != payload["sub"]:
            abort(401)

        # Allow the protected route to execute
        return f(*args, **kwargs)

    return wrapper