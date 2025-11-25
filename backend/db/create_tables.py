# create_tables.py

from backend.db.database import engine, Base
from backend.db.models import * # Import all your models so Base knows about them

def create_db_and_tables():
    print("Attempting to create all tables in the database...")
    
    # This reads all classes inheriting from Base and sends the CREATE TABLE commands to PostgreSQL
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()