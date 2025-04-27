from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from sqlalchemy.exc import IntegrityError

# --- Configuration and Setup ---
app = Flask(__name__)
# Set the path to store the database in the /data/ folder
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'site.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # For session security

# Session timeout after 30 minutes of inactivity
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    dark_mode = db.Column(db.Boolean, default=False)
    flashcards = db.relationship('Flashcard', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(200), nullable=False)
    back = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Flashcard {self.front} -> {self.back}>"

# --- Helper functions ---
def get_user():
    """Returns the User object for the current session."""
    if 'username' not in session:
        return None
    user = User.query.filter_by(username=session['username']).first()
    return user

def load_flashcards():
    """Load flashcards for the logged-in user."""
    user = get_user()
    if not user:
        return []
    return Flashcard.query.filter_by(user_id=user.id).all()

def save_flashcard(front, back):
    """Save a new flashcard for the logged-in user."""
    user = get_user()
    if user:
        new_flashcard = Flashcard(front=front, back=back, owner=user)
        db.session.add(new_flashcard)
        db.session.commit()

def is_admin():
    """Check if the current user is an admin."""
    if 'username' not in session or session['username'] != 'admin':
        return False
    return True

# --- Routes ---
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page where users can enter a username."""
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        flash("Username does not exist", "error")
    return render_template("login.html")

@app.route("/")
def index():
    """Main page showing the list of flashcards."""
    if 'username' not in session:
        return redirect(url_for('login'))

    flashcards = load_flashcards()
    user = get_user()
    return render_template("index.html", flashcards=flashcards, dark_mode=user.dark_mode)

@app.route("/review", methods=["GET", "POST"])
def review():
    """Review mode where users can practice flashcards."""
    if 'username' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('login'))

    flashcards = load_flashcards()

    if request.method == "POST":
        num_cards = int(request.form.get("num_cards", len(flashcards)))
        selected_cards = random.sample(flashcards, min(num_cards, len(flashcards)))
        return render_template("review_session.html", flashcards=selected_cards)

    return render_template("review_select.html", total=len(flashcards))

@app.route("/api/flashcards", methods=["GET"])
def get_flashcards():
    """API route to get all flashcards."""
    return jsonify([flashcard.front + " -> " + flashcard.back for flashcard in load_flashcards()])

@app.route("/api/flashcards", methods=["POST"])
def add_flashcard():
    """API route to add a new flashcard."""
    try:
        data = request.json
        front = data.get("front")
        back = data.get("back")
        
        if not front or not back:
            return jsonify({"status": "error", "message": "Missing 'front' or 'back'."}), 400

        save_flashcard(front, back)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/logout")
def logout():
    """Logout current user."""
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Settings page where users can toggle dark mode."""
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    if request.method == "POST":
        dark_mode = request.form.get("dark_mode") == "on"
        user.dark_mode = dark_mode
        db.session.commit()
        flash('Settings saved!', 'success')

    return render_template("settings.html", dark_mode=user.dark_mode)

@app.route("/admin/users")
def manage_users():
    """Display a list of all users."""
    if not is_admin():
        flash("You must be an admin to view this page.", "error")
        return redirect(url_for('index'))

    users = User.query.all()  # Get all users
    return render_template("manage_users.html", users=users)


@app.route("/admin/users/add", methods=["GET", "POST"])
def add_user():
    """Add a new user (admin only)."""
    if not is_admin():
        flash("You must be an admin to perform this action.", "error")
        return redirect(url_for('index'))

    if request.method == "POST":
        username = request.form.get("username")
        dark_mode = request.form.get("dark_mode") == "on"  # Toggle dark_mode
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.", "error")
        else:
            new_user = User(username=username, dark_mode=dark_mode)
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully.", "success")
            return redirect(url_for('manage_users'))

    return render_template("add_user.html")


@app.route("/admin/users/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    """Edit an existing user (admin only)."""
    if not is_admin():
        flash("You must be an admin to perform this action.", "error")
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.username = request.form.get("username")
        user.dark_mode = request.form.get("dark_mode") == "on"
        db.session.commit()
        flash("User details updated successfully.", "success")
        return redirect(url_for('manage_users'))

    return render_template("edit_user.html", user=user)


@app.route("/admin/users/delete/<int:id>")
def delete_user(id):
    """Delete a user (admin only)."""
    if not is_admin():
        flash("You must be an admin to perform this action.", "error")
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('manage_users'))

# --- Ensure the default admin user exists ---
def create_default_admin():
    """Create a default admin user if none exists."""
    if not os.path.exists('site.db'):  # Check if the database exists
        db.create_all()  # Create the database and tables
    # Check if the admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', dark_mode=False)
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created.")

# --- Main entry point ---
if __name__ == "__main__":
    create_default_admin()  # Ensure default admin user is created
    app.run(host="0.0.0.0", port=5000, debug=True)
