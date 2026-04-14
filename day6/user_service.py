from database import get_connection


class UserService:
    def create_user(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (username, password, token)
                VALUES (?, ?, NULL)
            """, (username, password))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return self.get_user_by_id(user_id)
        except Exception:
            conn.close()
            return None

    def get_user_by_id(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password, token
            FROM users
            WHERE id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_user_by_username(self, username):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password, token
            FROM users
            WHERE username = ?
        """, (username,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_user_by_token(self, token):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password, token
            FROM users
            WHERE token = ?
        """, (token,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def update_user_token(self, user_id, token):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET token = ?
            WHERE id = ?
        """, (token, user_id))

        conn.commit()
        conn.close()

    def clear_user_token(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET token = NULL
            WHERE id = ?
        """, (user_id,))

        conn.commit()
        conn.close()