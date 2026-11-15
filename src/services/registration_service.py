
import re

from werkzeug.security import generate_password_hash
from database.postgres_db import get_connection

from src.repositories.postgres_repo import (
    create_user,
    email_exists,
    add_membership,
    membership_exists
)

from src.repositories.mongodb_repo import (
    create_profile,
    delete_profile
)


def validate_registration(form):

    # Validate user input
    email = form["email"].strip()
    confirm_email = form["confirm_email"].strip()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Please enter a valid email address."

    if email != confirm_email:
        return False, "Email addresses do not match."

    if form["password"] != form["confirm_password"]:
        return False, "Passwords do not match."

    phone = form["phone_number"]

    if not (phone.isdigit() and phone.startswith("0") and len(phone) == 11):
        return False, "Please enter a valid 11-digit phone number."

    return True, None


def register_user(user_data, connection):

    # Check for existing email
    if email_exists(user_data["email"], connection):
        return {
            "success": False,
            "error": "Email address already registered"
        }

    # Hash password before database insertion
    account_data = {
        **user_data,
        "password_hash": generate_password_hash(user_data["password"])
    }

    user_id = create_user(account_data, connection)

    return {
        "success": True,
        "user_id": user_id
    }


def register_membership(memb_data, connection):

    # Check for existing membership
    if membership_exists(memb_data["user_id"], connection):
        return {
            "success": False,
            "error": "User already has an active membership"
        }

    user_id = add_membership(memb_data, connection)

    return {
        "success": True,
        "user_id": user_id
    }


def registration(registration_data):

    plan_ids = {
        "standard": 1,
        "plus": 2,
        "premium": 3
    }

    plan = registration_data["membership"]["plan"]

    if plan not in plan_ids:
        return {
            "success": False,
            "step": 2,
            "error": "Invalid membership plan selected."
        }

    user_id = None
    mongo_created = False

    try:
        # PostgreSQL transaction remains open
        # until MongoDB profile creation succeeds.
        with get_connection() as connection:

            # 1. Create PostgreSQL user
            user_result = register_user(
                registration_data["user_data"],
                connection
            )

            if not user_result["success"]:
                return {
                    "success": False,
                    "step": 1,
                    "error": user_result["error"]
                }

            user_id = user_result["user_id"]

            # 2. Create PostgreSQL membership
            membership_result = register_membership(
                {
                    "user_id": user_id,
                    "memp_id": plan_ids[plan]
                },
                connection
            )

            if not membership_result["success"]:
                connection.rollback()

                return {
                    "success": False,
                    "step": 2,
                    "error": membership_result["error"]
                }

            # 3. Create MongoDB profile
            create_profile(
                user_id=user_id,
                fitness_data=registration_data["fitness"],
                advertising_consent=registration_data.get(
                    "advertising_consent", False
                )
            )

            mongo_created = True

            # 4. Commit PostgreSQL only after
            # MongoDB profile creation succeeds.
            connection.commit()

        return {
            "success": True,
            "step": None,
            "user_id": user_id
        }

    except Exception:

        # Postgres rolls back
        # uncommitted changes on exception.

        # If MongoDB succeeded but Postgres failed,
        # attempt to remove the MongoDB profile.
        if mongo_created:
            delete_profile(user_id)

        raise
