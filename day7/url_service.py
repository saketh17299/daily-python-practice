import random
import string
from datetime import datetime

from database import get_connection


class URLService:
    def generate_short_code(self, length=6):
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=length))

    def short_code_exists(self, short_code):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM urls
            WHERE short_code = ?
        """, (short_code,))

        row = cursor.fetchone()
        conn.close()

        return row is not None

    def generate_unique_short_code(self):
        while True:
            short_code = self.generate_short_code()
            if not self.short_code_exists(short_code):
                return short_code

    def create_short_url(self, original_url):
        short_code = self.generate_unique_short_code()
        created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO urls (original_url, short_code, created_at)
            VALUES (?, ?, ?)
        """, (original_url, short_code, created_at))

        conn.commit()
        url_id = cursor.lastrowid
        conn.close()

        return self.get_url_by_id(url_id)

    def get_url_by_id(self, url_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, original_url, short_code, created_at
            FROM urls
            WHERE id = ?
        """, (url_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_url_by_short_code(self, short_code):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, original_url, short_code, created_at
            FROM urls
            WHERE short_code = ?
        """, (short_code,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_all_urls(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, original_url, short_code, created_at
            FROM urls
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
