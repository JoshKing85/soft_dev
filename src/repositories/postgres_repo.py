from database.postgres_db import get_connection


# ACCOUNT REGISTRATION

# Verify unique user email address.

def email_exists(email, connection):
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM users WHERE LOWER(email) = LOWER(%s)",
            (email,)
        )
        
        return cursor.fetchone() is not None

# Verify password        
def get_password_hash(email, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT password_hash FROM users WHERE LOWER(email) = LOWER(%s)",
            (email,)
        )

        result = cursor.fetchone()
        return result[0] if result else None

# Get user ID
def get_user_ID(email, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM users WHERE LOWER(email) = LOWER(%s)",
            (email,)
        )

        result = cursor.fetchone()
        return result[0] if result else None


# Populate postgres database users table with user data    
def create_user(user_data, connection):
    
    sql = """
        INSERT INTO users (
            first_name,
            last_name,
            email,
            phone_number,
            address,
            date_of_birth,
            gender,
            password_hash
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING user_id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql,(

            user_data["first_name"],
            user_data["last_name"],
            user_data["email"],
            user_data["phone_number"],
            user_data["address"],
            user_data["date_of_birth"],
            user_data["gender"],
            user_data["password_hash"]
            ))

            user_id = cursor.fetchone()[0]
    
    return user_id


# Verify membership is unique

def membership_exists(user_id, connection):
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM memberships WHERE user_id = %s",
            (user_id,)
        )
        
        return cursor.fetchone() is not None


# Populate memberships with unique user membership

def add_membership(mem_data, connection):

    sql = """
        INSERT INTO memberships (
            user_id,
            memp_id,
            start_date,
            end_date
        )
        VALUES (
            %s,
            %s,
            CURRENT_DATE,
            CURRENT_DATE + INTERVAL '12 months'
        )
        RETURNING user_id;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (
            mem_data["user_id"],
            mem_data["memp_id"]
        ))

        user_id = cursor.fetchone()[0]

    return user_id
