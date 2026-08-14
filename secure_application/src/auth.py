from database import get_connection


def login():
    """Authenticate a user and return their information."""

    print("\n========== LOGIN ==========")

    username = input("Username: ")
    password = input("Password: ")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT user_id, username, role
        FROM users
        WHERE username = ? AND password = ?
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    connection.close()

    if user:
        print("\nLogin successful!")
        print(f"Welcome, {user['username']}!")
        print(f"Role: {user['role']}")

        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }

    print("\nInvalid username or password.")

    return None