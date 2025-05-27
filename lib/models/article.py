from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    def save(self):
        """Save the article to the database"""
        if not self.title:
            raise ValueError("Article title cannot be empty")
        if not hasattr(self.author, 'id') or not hasattr(self.magazine, 'id'):
            raise ValueError("Author and magazine must be saved first")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author.id, self.magazine.id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author.id, self.magazine.id, self.id)
                )
            conn.commit()

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT a.*, au.name as author_name, m.name as magazine_name, m.category
                FROM articles a
                JOIN authors au ON a.author_id = au.id
                JOIN magazines m ON a.magazine_id = m.id
                WHERE a.id = ?
                """,
                (id,)
            )
            row = cursor.fetchone()
            if row:
                author = Author(row[6], row[2])  # Using author_name and author_id
                magazine = Magazine(row[7], row[8], row[3])  # Using magazine_name, category, magazine_id
                return cls(row[1], author, magazine, row[0])
            return None

    @classmethod
    def find_by_author(cls, author_id):
        """Find all articles by a specific author"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (author_id,)
            )
            return cursor.fetchall()

    @classmethod
    def find_by_magazine(cls, magazine_id):
        """Find all articles in a specific magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (magazine_id,)
            )
            return cursor.fetchall()

    def __repr__(self):
        return f"<Article id={self.id} title='{self.title}' author_id={self.author.id} magazine_id={self.magazine.id}>"