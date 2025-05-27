import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connections import get_connection

class TestAuthor:
    @classmethod
    def setup_class(cls):
        """Setup test data"""
        cls.author = Author("Test Author")
        cls.author.save()
        cls.magazine = Magazine("Test Magazine", "Test")
        cls.magazine.save()
        cls.article = Article("Test Article", cls.author, cls.magazine)
        cls.article.save()

    def test_author_creation(self):
        """Test author creation and saving"""
        assert self.author.id is not None
        assert self.author.name == "Test Author"

    def test_find_by_id(self):
        """Test finding author by ID"""
        found = Author.find_by_id(self.author.id)
        assert found.id == self.author.id
        assert found.name == self.author.name

    def test_articles(self):
        """Test getting author's articles"""
        articles = self.author.articles()
        assert len(articles) >= 1
        assert articles[0][1] == "Test Article"  # title is second column

    def test_magazines(self):
        """Test getting author's magazines"""
        magazines = self.author.magazines()
        assert len(magazines) >= 1
        assert magazines[0][1] == "Test Magazine"  # name is second column

    def test_add_article(self):
        """Test adding an article"""
        new_mag = Magazine("New Test Mag", "Test")
        new_mag.save()
        article = self.author.add_article(new_mag, "New Test Article")
        assert article.id is not None
        assert article.title == "New Test Article"

    def test_topic_areas(self):
        """Test getting author's topic areas"""
        topics = self.author.topic_areas()
        assert "Test" in topics