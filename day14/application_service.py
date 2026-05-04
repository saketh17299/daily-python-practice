from database import get_connection


class ApplicationService:
    def get_all_applications(self, status=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, company, role, status, applied_date, notes
            FROM applications
            WHERE 1=1
        """
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY applied_date DESC, id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_application_by_id(self, application_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, company, role, status, applied_date, notes
            FROM applications
            WHERE id = ?
        """, (application_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_application(self, company, role, status, applied_date, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO applications (company, role, status, applied_date, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (company, role, status, applied_date, notes))

        conn.commit()
        application_id = cursor.lastrowid
        conn.close()

        return self.get_application_by_id(application_id)

    def update_application(self, application_id, company, role, status, applied_date, notes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE applications
            SET company = ?, role = ?, status = ?, applied_date = ?, notes = ?
            WHERE id = ?
        """, (company, role, status, applied_date, notes, application_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_application_by_id(application_id)

    def delete_application(self, application_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM applications
            WHERE id = ?
        """, (application_id,))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0

    def get_analytics(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) as total FROM applications")
        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM applications
            GROUP BY status
            ORDER BY count DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        status_counts = {row["status"]: row["count"] for row in rows}

        return {
            "total_applications": total,
            "status_counts": status_counts
        }