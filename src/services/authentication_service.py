from src.repositories.postgres_repo import get_password_hash, get_user_ID
from database.postgres_db import get_connection
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta, timezone
import jwt


def auth_login(email, password):

    connection = get_connection()

    try:
        stored_password = get_password_hash(email, connection)

        if stored_password is None:
            return None

        if check_password_hash(stored_password, password):
            return get_user_ID(email, connection)

        return None

    finally:
        connection.rollback()
        connection.close()




def gen_token(user_id, secret_key):

    now = datetime.now(timezone.utc)

    # Build payload
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(hours=1)
    }

    # Sign token using secret key
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return token


