from lib.db.connections import initialize_db
from lib.db.seed import seed_database

def main():
    print("Initializing database...")
    initialize_db()
    print("Seeding database with sample data...")
    seed_database()
    print("Database setup complete!")

if __name__ == "__main__":
    main()