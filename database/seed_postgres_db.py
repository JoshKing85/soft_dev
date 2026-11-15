from database.postgres_db import get_connection
from werkzeug.security import generate_password_hash


def seed_user():

    email = "testuser@viafitness.com"

    password_hash = generate_password_hash("TestPassword123!")

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
        SELECT %s, %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM users WHERE LOWER(email) = LOWER(%s)
        )
        RETURNING user_id;
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(sql, (
                "Test",
                "User",
                email,
                "07123456789",
                "123 Example Street",
                "1995-06-15",
                "Other",
                password_hash,
                email
            ))

            result = cursor.fetchone()

            if result:
                print(f"Test user created. ID: {result[0]}")
            else:
               print("Test user already exists. Skipping.")

               
def seed_membership_plans():

    sql = """
        INSERT INTO membership_plans (
            memp_id,
            memp_name,
            memp_cost
        )
        VALUES (%s, %s, %s)
        ON CONFLICT (memp_id) DO NOTHING;
    """

    membership_plans = [
        (1, "Standard", 15.99),
        (2, "Plus", 29.99),
        (3, "Premium", 39.99)
    ]

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.executemany(sql, membership_plans)

    print("Membership plans seeded successfully.")


if __name__ == "__main__":
    seed_user()
    seed_membership_plans()