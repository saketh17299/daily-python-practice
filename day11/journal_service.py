from database import get_connection


class JournalService:
    def get_all_entries(self, mood=None, start_date=None, end_date=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, entry_date, weather, mood, productivity_score, notes
            FROM journal_entries
            WHERE 1=1
        """
        params = []

        if mood:
            query += " AND mood = ?"
            params.append(mood)

        if start_date:
            query += " AND entry_date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND entry_date <= ?"
            params.append(end_date)

        query += " ORDER BY entry_date DESC, id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_entry_by_id(self, entry_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, entry_date, weather, mood, productivity_score, notes
            FROM journal_entries
            WHERE id = ?
        """, (entry_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_entry(self, entry_date, weather, mood, productivity_score, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO journal_entries (
                entry_date, weather, mood, productivity_score, notes
            )
            VALUES (?, ?, ?, ?, ?)
        """, (entry_date, weather, mood, productivity_score, notes))

        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()

        return self.get_entry_by_id(entry_id)

    def update_entry(self, entry_id, entry_date, weather, mood, productivity_score, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE journal_entries
            SET entry_date = ?, weather = ?, mood = ?, productivity_score = ?, notes = ?
            WHERE id = ?
        """, (entry_date, weather, mood, productivity_score, notes, entry_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_entry_by_id(entry_id)

    def delete_entry(self, entry_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM journal_entries
            WHERE id = ?
        """, (entry_id,))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0