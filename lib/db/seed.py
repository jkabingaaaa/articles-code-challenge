from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Create authors
    a1 = Author("John Doe")
    a1.save()
    a2 = Author("Jane Smith")
    a2.save()
    a3 = Author("Bob Johnson")
    a3.save()

    # Create magazines
    m1 = Magazine("Tech Today", "Technology")
    m1.save()
    m2 = Magazine("Science Weekly", "Science")
    m2.save()
    m3 = Magazine("Sports Digest", "Sports")
    m3.save()

    # Create articles
    Article("Python Programming", a1, m1).save()
    Article("Machine Learning", a1, m1).save()
    Article("Quantum Physics", a2, m2).save()
    Article("Neuroscience", a2, m2).save()
    Article("Football Tactics", a3, m3).save()
    Article("Basketball Strategies", a3, m3).save()
    Article("AI Ethics", a1, m2).save()
    Article("Space Exploration", a2, m1).save()