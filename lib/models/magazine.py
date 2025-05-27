from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        if not self.name or not self.category:
            raise ValueError("Name and category cannot be empty")
            
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    (self.name, self.category, self.id)
                )
            conn.commit()

    def articles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return cursor.fetchall()

    def contributors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return cursor.fetchall()

    def article_titles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return [row[0] for row in cursor.fetchall()]

    def contributing_authors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (self.id,)
            )
            return cursor.fetchall()

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                (id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[2], row[0])
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
                return cls(row[1], row[2], row[0])
            return None

    @classmethod
    def top_publisher(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
            )
            row = cursor.fetchone()
            if row:
                return cls(row[1], row[2], row[0])
            return None

    def __repr__(self):
        return f"<Magazine id={self.id} name='{self.name}' category='{self.category}'>"