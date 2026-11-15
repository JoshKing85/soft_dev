from pathlib import Path
from database.postgres_db import get_connection

def setup_postgres_database():

    # Path for postgres schema file.
    schema_path = Path(__file__).parent / "schema" / "postgres_schema.sql"

    sql = schema_path.read_text(encoding="utf-8")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
    
    print("Postgre SQL schema created successfully")


if __name__ == "__main__":
    setup_postgres_database()