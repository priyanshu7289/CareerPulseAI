from database.db_connection import get_session
from sqlalchemy import text

session = get_session()

try:
    result = session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))

    print("Tables in database:\n")

    for row in result:
        print(row[0])

finally:
    session.close()