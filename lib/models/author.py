from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        """Save the author to the database"""
        if not self.name:
            raise ValueError("Author name cannot be empty")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )
            conn.commit()

    def articles(self):
        """Get all articles written by this author"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (self.id,)
            )
            return cursor.fetchall()

    def magazines(self):
        """Get all magazines this author has contributed to"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self.id,)
            )
            return cursor.fetchall()

    def add_article(self, magazine, title):
        """Create a new article for this author"""
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be a Magazine instance")
            
        article = Article(title, self, magazine)
        article.save()
        return article

    def topic_areas(self):
        """Get unique categories of magazines author has contributed to"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
                """,
                (self.id,)
            )
            return [row[0] for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[0])
            return None

    @classmethod
    def find_by_name(cls, name):
        """Find an author by name"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE name = ?",
                (name,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[0])
            return None

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"