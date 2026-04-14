from datetime import datetime
from database import get_connection


class TaskService:
    def get_all_tasks(self, user_id, status=None, priority=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, title, description, status, priority, due_date, user_id
            FROM tasks
            WHERE user_id = ?
        """
        params = [user_id]

        if status:
            query += " AND status = ?"
            params.append(status)

        if priority:
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY due_date ASC, id ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_task_by_id(self, task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, description, status, priority, due_date, user_id
            FROM tasks
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_task(self, title, description, status, priority, due_date, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, description, status, priority, due_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, due_date, user_id))

        conn.commit()
        task_id = cursor.lastrowid
        conn.close()

        return self.get_task_by_id(task_id, user_id)

    def update_task(self, task_id, title, description, status, priority, due_date, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority = ?, due_date = ?
            WHERE id = ? AND user_id = ?
        """, (title, description, status, priority, due_date, task_id, user_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_task_by_id(task_id, user_id)

    def update_task_status(self, task_id, status, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ? AND user_id = ?
        """, (status, task_id, user_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_task_by_id(task_id, user_id)

    def delete_task(self, task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0

    def get_summary(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM tasks
            WHERE user_id = ?
            GROUP BY status
            ORDER BY count DESC, status ASC
        """, (user_id,))
        status_summary = cursor.fetchall()

        cursor.execute("""
            SELECT priority, COUNT(*) as count
            FROM tasks
            WHERE user_id = ?
            GROUP BY priority
            ORDER BY count DESC, priority ASC
        """, (user_id,))
        priority_summary = cursor.fetchall()

        conn.close()

        return {
            "status_summary": [dict(row) for row in status_summary],
            "priority_summary": [dict(row) for row in priority_summary]
        }

    def get_overdue_tasks(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()

        today = datetime.today().strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT id, title, description, status, priority, due_date, user_id
            FROM tasks
            WHERE user_id = ? AND due_date < ? AND status != 'completed'
            ORDER BY due_date ASC, id ASC
        """, (user_id, today))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]