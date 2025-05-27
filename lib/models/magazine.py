from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        """Save the magazine to the database"""
        if not self.name or not self.category:
            raise ValueError("Name and category cannot be empty")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            conn.commit()

    def articles(self):
        """Get all articles in this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return cursor.fetchall()

    def contributors(self):
        """Get all authors who have contributed to this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                """,
                (self.id,)
            )
            return cursor.fetchall()

    def article_titles(self):
        """Get all article titles in this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return [row[0] for row in cursor.fetchall()]

    def contributing_authors(self):
        """Get authors with more than 2 articles in this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.*, COUNT(ar.id) as article_count
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING article_count > 2
                """,
                (self.id,)
            )
            return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[2], row[0])
            return None

    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE name = ?",
                (name,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[2], row[0])
            return None

    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT m.*, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY article_count DESC
                LIMIT 1
                """
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[2], row[0])
            return None

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"