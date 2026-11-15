from bson.int64 import Int64
from pymongo.errors import PyMongoError
from database.mongo_db import db


def create_profile(user_id, fitness_data, advertising_consent):

    profile = {
        "user_id": Int64(user_id),
        "fitness": {
            "exercise_types": fitness_data.get("exercise_types", []),
            "classes": fitness_data.get("classes", []),
            "preferred_time": fitness_data.get("preferred_time", "")
        },
        "advertising_consent": bool(advertising_consent)
    }

    result = db.profiles.insert_one(profile)

    return result.inserted_id


def delete_profile(user_id):
    db.profiles.delete_one({"user_id": Int64(user_id)})


def get_user_goals(user_id):
    return list(db.goals.find({"user_id": user_id}))

def delete_goal(user_id, goal_type):
    return db.goals.delete_one({
        "user_id": user_id,
        "goal_type": goal_type
    })

def insert_goal(user_id, goal_data):
    goals = get_user_goals(user_id)

    for goal in goals:
        if goal["goal_type"] == goal_data["goal_type"]:
            return False

    goal_data["user_id"] = user_id
    db.goals.insert_one(goal_data)
    return True
