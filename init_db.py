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
                # Create default admin user with a hashed password if it doesn't exist
                admin = User(
                    username='admin',
                    dark_mode=True
                )
                admin.set_password('admin')  # Use the set_password method to hash the password
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created.")
            except Exception as e:
                print(f"Error creating admin user: {e}")
