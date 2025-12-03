# create_tables.py

from database import engine, Base
from models import *  # Ensure all models are imported so they are registered with Base

def create_db_and_tables():
    print("Attempting to create all tables in the database...")
    
    # This reads all classes inheriting from Base and sends the CREATE TABLE commands to PostgreSQL
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()