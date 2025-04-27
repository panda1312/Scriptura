from app import db, User, app

def init_db():
    """Reset and initialize the database."""
    with app.app_context():
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
