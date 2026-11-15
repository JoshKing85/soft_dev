from database.mongo_db import db


from database.mongo_db import db


def setup_database():

    # Profile schema
    profile_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "fitness", "advertising_consent"],
            "properties": {
                "user_id": {
                    "bsonType": "long"
                },
                "fitness": {
                    "bsonType": "object",
                    "required": [
                        "exercise_types",
                        "classes",
                        "preferred_time"
                    ],
                    "properties": {
                        "exercise_types": {
                            "bsonType": "array",
                            "items": {"bsonType": "string"}
                        },
                        "classes": {
                            "bsonType": "array",
                            "items": {"bsonType": "string"}
                        },
                        "preferred_time": {
                            "bsonType": "string"
                        }
                    }
                },
                "advertising_consent": {
                    "bsonType": "bool"
                }
            }
        }
    }

    # Goals schema - individual goals remain flexible
    goals_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["user_id", "goal_type"],
            "properties": {
                "user_id": {"bsonType": ["int", "long"]},
                "goal_type": {
                    "enum": ["classes", "weight", "pb"]
                }
            }
        }
    }

    collections = {
        "profiles": profile_schema,
        "goals": goals_schema,
        "advertisements": None
    }

    existing = db.list_collection_names()

    for name, schema in collections.items():

        if name not in existing:
            options = {"validator": schema} if schema else {}
            db.create_collection(name, **options)

        elif schema:
            db.command({
                "collMod": name,
                "validator": schema,
                "validationLevel": "strict",
                "validationAction": "error"
            })

    # Unique profile and goals documents per user
    db.profiles.create_index("user_id", unique=True)
    db.goals.create_index("user_id", unique=True)

    print("MongoDB database setup complete.")


if __name__ == "__main__":
    setup_database()


