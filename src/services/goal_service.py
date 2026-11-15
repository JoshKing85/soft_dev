from src.repositories.mongodb_repo import(insert_goal, delete_goal)


# Validate goal dict data
def validate_goal_data_type(goal_data):
     
    GOALS_SCHEMAS = {
        
        "classes" : {
            "activity_target": int
        },

        "weight": {
            "current_weight": float,
            "target_weight": float,
            "weight_unit": str,
            "duration": int
        },

        "pb":{

            "pb_type": str
        }
    }
     
    PB_SCHEMAS = {
        "running": {
            "pb_current_time": str,
        },

        "rowing": {
            "pb_current_time": str,
        },

        "bench_press": {
            "pb_current_weight": float,
        },

        "pull_ups": {
            "pb_current_reps": int,
        }
    }

    goal_type = goal_data.get("goal_type")
    schema = GOALS_SCHEMAS.get(goal_type)
    
    if schema is None:
        return False

    if goal_type == "pb":
        activity = goal_data.get("pb_type")
        pb_schema = PB_SCHEMAS.get(activity)

        if pb_schema is None:
            return False

        schema = {**schema, **pb_schema}

    for field, expected_type in schema.items():
        try:
            goal_data[field] = expected_type(goal_data[field])

        except (KeyError, ValueError, TypeError):
            return False

    return True

# validate that goal data is within business rules.
def validate_goal_rules(goal_data):

    goal_type = goal_data["goal_type"]

    match goal_type:

        # CLASSES
        case "classes":
            target = goal_data["activity_target"]

            if target not in (10, 15, 20):
                return False

            return True

        # WEIGHT
        case "weight":
            unit = goal_data["weight_unit"]

            if unit not in ("kg", "st"):
                return False

            current_weight = goal_data["current_weight"]
            target_weight = goal_data["target_weight"]
            duration = goal_data["duration"]

            # Validate permitted duration
            if duration not in (3, 6, 9, 12):
                return False

            # Validate weight boundaries
            if unit == "kg":
                if not 30 <= current_weight <= 250:
                    return False

                if not 30 <= target_weight <= 250:
                    return False

            elif unit == "st":
                if not 4.72 <= current_weight <= 39.37:
                    return False

                if not 4.72 <= target_weight <= 39.37:
                    return False

            return True

        # PERSONAL BEST
        case "pb":
            activity = goal_data["pb_type"]

            match activity:

                # RUNNING / ROWING
                case "running" | "rowing":
                    time_value = goal_data["pb_current_time"]

                    try:
                        hours, minutes, seconds = map(
                            int, time_value.split(":")
                        )
                    except (ValueError, TypeError):
                        return False

                    # Validate time format
                    if not (0 <= minutes < 60 and 0 <= seconds < 60):
                        return False

                    total_seconds = (
                        hours * 3600
                        + minutes * 60
                        + seconds
                    )

                    # Provisional boundary: 1 second to 24 hours
                    if not 1 <= total_seconds <= 86400:
                        return False

                # BENCH PRESS
                case "bench_press":
                    weight = goal_data["pb_current_weight"]

                    # Provisional record-based upper limit
                    if not 0 < weight <= 372.75:
                        return False

                # PULL-UPS
                case "pull_ups":
                    reps = goal_data["pb_current_reps"]

                    # Provisional upper limit
                    if not 1 <= reps <= 150:
                        return False

                case _:
                    return False

            return True

        # INVALID GOAL TYPE
        case _:
            return False




# Dash preview data for dashboard service
def get_dash_model(user_id):

    return None

# Current models for goal service and goal life cycles clean
def get_current_model(user_id):
    return None

# Points model for goal service
def get_points_model(user_id):
    return None

# Create new goal
def create_goal(user_id, goal_data):
    if validate_goal_data_type(goal_data):
        if validate_goal_rules(goal_data):
            if insert_goal(user_id, goal_data):
                return True, "Success! Your Goal is ready track"
            else:
                return False, f"Sorry a goal for {goal_data["goal_type"]} is already in progress. Delete goal to start a new journey"
        else:
            return False, "Sorry, an invalid value has been given. Please try again."
    else:
        return False, "Sorry, an invalid data type has been given. Please try again."

# Update Goal like pb 
def update_goal(user_id):
    return None