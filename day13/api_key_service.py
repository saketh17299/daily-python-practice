import uuid
from datetime import datetime

from database import get_connection


class ApiKeyService:
    def generate_api_key(self, label=None):
        api_key = str(uuid.uuid4())
        created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO api_keys (api_key, label, is_active, created_at)
            VALUES (?, ?, 1, ?)
        """, (api_key, label, created_at))

        conn.commit()
        key_id = cursor.lastrowid
        conn.close()

        return self.get_key_by_id(key_id)

    def get_key_by_id(self, key_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, api_key, label, is_active, created_at
            FROM api_keys
            WHERE id = ?
        """, (key_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_all_keys(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, api_key, label, is_active, created_at
            FROM api_keys
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def is_valid_key(self, api_key):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM api_keys
            WHERE api_key = ? AND is_active = 1
        """, (api_key,))

        row = cursor.fetchone()
        conn.close()

        return row is not None