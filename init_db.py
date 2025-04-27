from app import db, User, app

def init_db():
    """Reset and initialize the database."""
    with app.app_context():
        # Ask user for confirmation before dropping tables
        confirmation = input("Are you sure you want to reset the database? This will delete all data. (y/n): ")
        if confirmation.lower() != 'y':
            print("Database reset cancelled.")
            return
        
        # Drop all existing tables
        db.drop_all()
        print("Dropped all tables.")
        
        # Recreate all tables
        db.create_all()
        print("Created new tables.")
        
        # Create default admin user
        admin = User(username='admin', dark_mode=False)
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created.")

if __name__ == "__main__":
    init_db()
