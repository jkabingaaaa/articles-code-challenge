# Correct import structure
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connections import get_connection  

class Article:
    def __init__(self, title, author, magazine, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    def save(self):
        if not self.title:
            raise ValueError("Article title cannot be empty")
        if not hasattr(self.author, 'id') or not hasattr(self.magazine, 'id'):
            raise ValueError("Author and magazine must be saved first")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                   
                    (self.title, self.author.id, self.magazine.id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
            
                    (self.title, self.author.id, self.magazine.id, self.id)
                )
            conn.commit()

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
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
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (author_id,)
            )
            return cursor.fetchall()

    @classmethod
    def find_by_magazine(cls, magazine_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (magazine_id,)
            )
            return cursor.fetchall()

    def __repr__(self):
        return f"<Article id={self.id} title='{self.title}' author_id={self.author.id} magazine_id={self.magazine.id}>"




 