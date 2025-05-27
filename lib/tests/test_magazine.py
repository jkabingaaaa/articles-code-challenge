import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connections import get_connection

class TestMagazine:
    @classmethod
    def setup_class(cls):
        """Setup test data"""
        cls.author1 = Author("Magazine Test Author 1")
        cls.author1.save()
        cls.author2 = Author("Magazine Test Author 2")
        cls.author2.save()
        cls.magazine = Magazine("Test Magazine", "Testing")
        cls.magazine.save()
        
        # Create multiple articles
        cls.article1 = Article("Test Article 1", cls.author1, cls.magazine)
        cls.article1.save()
        cls.article2 = Article("Test Article 2", cls.author1, cls.magazine)
        cls.article2.save()
        cls.article3 = Article("Test Article 3", cls.author2, cls.magazine)
        cls.article3.save()

    def test_magazine_creation(self):
        """Test magazine creation and saving"""
        assert self.magazine.id is not None
        assert self.magazine.name == "Test Magazine"
        assert self.magazine.category == "Testing"

    def test_find_by_id(self):
        """Test finding magazine by ID"""
        found = Magazine.find_by_id(self.magazine.id)
        assert found.id == self.magazine.id
        assert found.name == self.magazine.name
        assert found.category == self.magazine.category

    def test_articles(self):
        """Test getting magazine's articles"""
        articles = self.magazine.articles()
        assert len(articles) == 3
        article_ids = [a[0] for a in articles]  # id is first column
        assert self.article1.id in article_ids
        assert self.article2.id in article_ids
        assert self.article3.id in article_ids

    def test_contributors(self):
        """Test getting magazine's contributors"""
        contributors = self.magazine.contributors()
        assert len(contributors) == 2
        contributor_ids = [c[0] for c in contributors]  # id is first column
        assert self.author1.id in contributor_ids
        assert self.author2.id in contributor_ids

    def test_article_titles(self):
        """Test getting magazine's article titles"""
        titles = self.magazine.article_titles()
        assert len(titles) == 3
        assert "Test Article 1" in titles
        assert "Test Article 2" in titles
        assert "Test Article 3" in titles

    def test_contributing_authors(self):
        """Test finding contributing authors (with >2 articles)"""
        # Author1 has 2 articles, Author2 has 1 in this test
        contributors = self.magazine.contributing_authors()
        assert len(contributors) == 0  # No authors with >2 articles
        
        # Add one more article to author1 to trigger the condition
        Article("Test Article 4", self.author1, self.magazine).save()
        contributors = self.magazine.contributing_authors()
        assert len(contributors) == 1
        assert contributors[0][0] == self.author1.id  # id is first column

    def test_top_publisher(self):
        """Test finding top publisher"""
        # Create a second magazine with fewer articles
        mag2 = Magazine("Other Magazine", "Other")
        mag2.save()
        Article("Other Article", self.author1, mag2).save()
        
        top = Magazine.top_publisher()
        assert top.id == self.magazine.id
        assert top.name == "Test Magazine"

    @classmethod
    def teardown_class(cls):
        """Clean up test data"""
        with get_connection() as conn:
            conn.execute("DELETE FROM articles WHERE magazine_id = ?", (cls.magazine.id,))
            conn.execute("DELETE FROM magazines WHERE id = ?", (cls.magazine.id,))
            conn.execute("DELETE FROM authors WHERE id IN (?, ?)", (cls.author1.id, cls.author2.id))
            conn.commit()