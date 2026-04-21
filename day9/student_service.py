from database import get_connection


class StudentService:
    def calculate_average(self, math_marks, science_marks, english_marks):
        total = math_marks + science_marks + english_marks
        return round(total / 3, 2)

    def calculate_result(self, math_marks, science_marks, english_marks):
        if math_marks >= 35 and science_marks >= 35 and english_marks >= 35:
            return "Pass"
        return "Fail"

    def calculate_grade(self, average):
        if average >= 90:
            return "A"
        elif average >= 75:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        return "F"

    def get_all_students(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, math_marks, science_marks, english_marks, average, result, grade
            FROM students
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_student_by_id(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, math_marks, science_marks, english_marks, average, result, grade
            FROM students
            WHERE id = ?
        """, (student_id,))

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def get_topper(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, math_marks, science_marks, english_marks, average, result, grade
            FROM students
            ORDER BY average DESC, id ASC
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def create_student(self, name, math_marks, science_marks, english_marks):
        average = self.calculate_average(math_marks, science_marks, english_marks)
        result = self.calculate_result(math_marks, science_marks, english_marks)
        grade = self.calculate_grade(average)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (
                name, math_marks, science_marks, english_marks, average, result, grade
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, math_marks, science_marks, english_marks, average, result, grade))

        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        return self.get_student_by_id(student_id)

    def update_student(self, student_id, name, math_marks, science_marks, english_marks):
        average = self.calculate_average(math_marks, science_marks, english_marks)
        result = self.calculate_result(math_marks, science_marks, english_marks)
        grade = self.calculate_grade(average)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET name = ?, math_marks = ?, science_marks = ?, english_marks = ?, average = ?, result = ?, grade = ?
            WHERE id = ?
        """, (name, math_marks, science_marks, english_marks, average, result, grade, student_id))

        conn.commit()
        updated_count = cursor.rowcount
        conn.close()

        if updated_count == 0:
            return None

        return self.get_student_by_id(student_id)

    def delete_student(self, student_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE id = ?
        """, (student_id,))

        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()

        return deleted_count > 0