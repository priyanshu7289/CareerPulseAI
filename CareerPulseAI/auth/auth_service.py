"""
Authentication service for CareerPulse AI
"""

from sqlalchemy import text

from database.db_connection import get_session
from auth.password import hash_password, verify_password


def get_user_by_email(email: str):
    session = get_session()

    try:
        result = session.execute(
            text("""
                SELECT *
                FROM users
                WHERE email = :email
            """),
            {"email": email}
        )

        return result.fetchone()

    finally:
        session.close()


def register_user(
    full_name: str,
    email: str,
    password: str,
    target_role: str
):
    session = get_session()

    try:

        existing = get_user_by_email(email)

        if existing:
            return False, "Email already registered."

        hashed_password = hash_password(password)

        session.execute(
            text("""
                INSERT INTO users
                (full_name, email, password_hash, target_role)
                VALUES
                (:name, :email, :password, :role)
            """),
            {
                "name": full_name,
                "email": email,
                "password": hashed_password,
                "role": target_role,
            },
        )

        session.commit()

        return True, "Registration successful."

    except Exception as e:

        session.rollback()

        return False, str(e)

    finally:

        session.close()


def login_user(email: str, password: str):

    user = get_user_by_email(email)

    if user is None:
        return False, None

    if verify_password(password, user.password_hash):
        return True, user

    return False, None