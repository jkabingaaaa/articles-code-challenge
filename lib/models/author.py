from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def save(self):
        if not self.name:
            raise ValueError("Author name cannot be empty")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    (self.name,)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    (self.name, self.id)
                )
            conn.commit()

    def articles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return cursor.fetchall()

    def magazines(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return cursor.fetchall()

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be a Magazine instance")
            
        article = Article(title, self, magazine)
        article.save()
        return article

    def topic_areas(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return [row[0] for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[0])
            return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (name,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[0])
            return None

    def __repr__(self):
        return f"<Author id={self.id} name='{self.name}'>"