from database import get_connection


class NoteService:
    def get_all_notes(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, content, tags
            FROM notes
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_note_by_id(self, note_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, content, tags
            FROM notes
            WHERE id = ?
        """, (note_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_note(self, title, content, tags):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notes (title, content, tags)
            VALUES (?, ?, ?)
        """, (title, content, tags))

        conn.commit()
        note_id = cursor.lastrowid
        conn.close()

        return self.get_note_by_id(note_id)

    def update_note(self, note_id, title, content, tags):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE notes
            SET title = ?, content = ?, tags = ?
            WHERE id = ?
        """, (title, content, tags, note_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_note_by_id(note_id)

    def delete_note(self, note_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM notes
            WHERE id = ?
        """, (note_id,))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0

    def search_notes(self, query):
        conn = get_connection()
        cursor = conn.cursor()

        search_pattern = f"%{query}%"

        cursor.execute("""
            SELECT id, title, content, tags
            FROM notes
            WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
            ORDER BY id DESC
        """, (search_pattern, search_pattern, search_pattern))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_notes_by_tag(self, tag):
        conn = get_connection()
        cursor = conn.cursor()

        search_pattern = f"%{tag}%"

        cursor.execute("""
            SELECT id, title, content, tags
            FROM notes
            WHERE tags LIKE ?
            ORDER BY id DESC
        """, (search_pattern,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]