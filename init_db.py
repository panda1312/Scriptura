from app import db, User, app
from werkzeug.security import generate_password_hash  # Important to hash passwords!

def init_db():
    """Initialize the database without dropping existing data."""
    with app.app_context():
        try:
            # Create tables if they don't already exist
            db.create_all()
            print("Tables created or verified.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            return

        # Check if the admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists.")
        else:
            try:
                # Create default admin user with a password if it doesn't exist
                admin = User(
                    username='admin',
                    password=generate_password_hash('admin', method='sha256'),
                    dark_mode=False
                )
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created.")
            except Exception as e:
                print(f"Error creating admin user: {e}")

if __name__ == "__main__":
    init_db()
