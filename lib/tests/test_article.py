import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connections import get_connection

class TestArticle:
    @classmethod
    def setup_class(cls):
        """Setup test data"""
        cls.author = Author("Test Article Author")
        cls.author.save()
        cls.magazine = Magazine("Test Article Magazine", "Testing")
        cls.magazine.save()
        cls.article = Article("Test Article", cls.author, cls.magazine)
        cls.article.save()

    def test_article_creation(self):
        """Test article creation and saving"""
        assert self.article.id is not None
        assert self.article.title == "Test Article"
        assert self.article.author.id == self.author.id
        assert self.article.magazine.id == self.magazine.id

    def test_find_by_id(self):
        """Test finding article by ID"""
        found = Article.find_by_id(self.article.id)
        assert found.id == self.article.id
        assert found.title == self.article.title
        assert found.author.id == self.author.id
        assert found.magazine.id == self.magazine.id

    def test_find_by_author(self):
        """Test finding articles by author"""
        articles = Article.find_by_author(self.author.id)
        assert len(articles) >= 1
        assert any(a[0] == self.article.id for a in articles)  # id is first column

    def test_find_by_magazine(self):
        """Test finding articles by magazine"""
        articles = Article.find_by_magazine(self.magazine.id)
        assert len(articles) >= 1
        assert any(a[0] == self.article.id for a in articles)

    @classmethod
    def teardown_class(cls):
        """Clean up test data"""
        with get_connection() as conn:
            conn.execute("DELETE FROM articles WHERE id = ?", (cls.article.id,))
            conn.execute("DELETE FROM authors WHERE id = ?", (cls.author.id,))
            conn.execute("DELETE FROM magazines WHERE id = ?", (cls.magazine.id,))
            conn.commit()