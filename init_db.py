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
        try:
            db.drop_all()
            print("Dropped all tables.")
        except Exception as e:
            print(f"Error dropping tables: {e}")
            return
        
        # Recreate all tables
        try:
            db.create_all()
            print("Created new tables.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            return
        
        # Check if the admin user already exists before creating it
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists.")
        else:
            try:
                # Create default admin user if it doesn't exist
                admin = User(username='admin', dark_mode=False)
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created.")
            except Exception as e:
                print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    init_db()
