from functools import wraps
from flask import request, abort

# Fields shared by all goals
COMMON_FIELDS = {
    "action",
    "goal_type"
}
# Specific goal fields
GOAL_FIELDS = {
    "activities": {
        "activity_type",
        "activity_target"
    },
    "weight": {
        "current_weight",
        "current_weight_unit",
        "target_weight",
        "target_weight_unit",
        "duration"
    },
    "pb": {
        "pb_type"
    }
}
# Nested personal best fields
PB_FIELDS = {
    "running": {
        "pb_current_time",
        "pb_target_time"
    },
    "rowing": {
        "pb_current_time",
        "pb_target_time"
    },
    "bench_press": {
        "pb_current_weight",
        "pb_target_weight"
    },
    "pull_ups": {
        "pb_current_reps",
        "pb_target_reps"
    }
}

# Wrap POST request and validate form submission
def validate_create_goal(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if request.method == "POST":

            goal_type = request.form.get("goal_type")

            if goal_type not in GOAL_FIELDS:
                abort(400)

            # Create field key set
            allowed_fields = COMMON_FIELDS | GOAL_FIELDS[goal_type]

            if goal_type == "pb":

                pb_type = request.form.get("pb_type")

                if pb_type not in PB_FIELDS:
                    abort(400)

                # Add PB-specific fields
                allowed_fields |= PB_FIELDS[pb_type]

            submitted_fields = set(request.form.keys())

            if submitted_fields != allowed_fields:
                abort(400)

            # Reject duplicate form keys
            if len(request.form) != len(submitted_fields):
                abort(400)

        return f(*args, **kwargs)
    
    # Return wrapped POST request to execute
    return wrapper
            
