import os
from datetime import datetime
from database import get_connection


UPLOAD_FOLDER = "uploads"


class FileService:
    def save_file_metadata(self, filename, stored_name, file_size):
        conn = get_connection()
        cursor = conn.cursor()

        uploaded_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO files (filename, stored_name, file_size, uploaded_at)
            VALUES (?, ?, ?, ?)
        """, (filename, stored_name, file_size, uploaded_at))

        conn.commit()
        file_id = cursor.lastrowid
        conn.close()

        return self.get_file_by_id(file_id)

    def get_all_files(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, filename, stored_name, file_size, uploaded_at
            FROM files
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_file_by_id(self, file_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, filename, stored_name, file_size, uploaded_at
            FROM files
            WHERE id = ?
        """, (file_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None