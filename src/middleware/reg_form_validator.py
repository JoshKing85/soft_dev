from functools import wraps
from flask import request, abort

# Expected format and fields from sign up registration
ALLOWED_FIELDS = {
    
    1: {
         "step", "first_name", "last_name", "email",
        "confirm_email", "phone_number", "address",
        "date_of_birth", "gender", "password",
        "confirm_password"
    },

    2: {
        "step", "membership_plan"
    },

    3:{
        "step", "exercise_types", "classes", "preffered_time"
    },

    4:{
        "step", "advertising_consent"
    }
}

def validate_registration_form(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if request.method == "POST":
            step = request.form.get("step", type=int)

            if step not in ALLOWED_FIELDS:
                abort(400)

            submitted_fields = set(request.form.keys())

        return f(*args, **kwargs)

    return wrapper