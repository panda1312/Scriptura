from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from sqlalchemy.exc import IntegrityError
import random  # For review random sampling

# --- Configuration and Setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Use a secure key in production
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

    def check_password(self, password):
        return self.username == password  # (You should replace with real password hashing later)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(200), nullable=False)
    back = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Flashcard {self.front} -> {self.back}>"

# --- Helper Functions ---
def get_user():
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])

def load_flashcards():
    user = get_user()
    if not user:
        return []
    return Flashcard.query.filter_by(user_id=user.id).all()

def save_flashcard(front, back):
    user = get_user()
    if user:
        new_flashcard = Flashcard(front=front, back=back, owner=user)
        db.session.add(new_flashcard)
        db.session.commit()

def is_admin():
    user = get_user()
    return user and user.username == 'admin'

# --- Routes ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash("Username does not exist", "error")
    return render_template("login.html")

@app.route("/")
def index():
    """Default page: automatically login as admin and go to add user page."""
    admin = User.query.filter_by(username='admin').first()

    if admin:
        session.permanent = True
        session['user_id'] = admin.id
        return redirect(url_for('add_user'))
    else:
        flash("Admin user not found. Please create one.", "error")
        return redirect(url_for('login'))

@app.route("/review", methods=["GET", "POST"])
def review():
    user = get_user()
    if not user:
        flash('Please log in first!', 'error')
        return redirect(url_for('login'))

    flashcards = load_flashcards()

    if request.method == "POST":
        num_cards = int(request.form.get("num_cards", len(flashcards)))
        selected_cards = random.sample(flashcards, min(num_cards, len(flashcards)))
        return render_template("review_session.html", flashcards=selected_cards)

    return render_template("review_select.html", total=len(flashcards))

@app.route("/api/flashcards", methods=["GET"])
def get_flashcards_api():
    return jsonify([flashcard.front + " -> " + flashcard.back for flashcard in load_flashcards()])

@app.route("/api/flashcards", methods=["POST"])
def add_flashcard_api():
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
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route("/settings", methods=["GET", "POST"])
def settings():
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
    if not is_admin():
        flash("You must be an admin to view this page.", "error")
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template("manage_users.html", users=users)

@app.route("/admin/users/add", methods=["GET", "POST"])
def add_user():
    if not is_admin():
        flash("You must be an admin to perform this action.", "error")
        return redirect(url_for('index'))

    if request.method == "POST":
        username = request.form.get("username")
        dark_mode = request.form.get("dark_mode") == "on"
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
    if not is_admin():
        flash("You must be an admin to perform this action.", "error")
        return redirect(url_for('index'))

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('manage_users'))

# --- Auto-login Admin in Development Mode ---
@app.before_request
def auto_login_admin():
    if app.debug:
        if 'user_id' not in session:
            admin = User.query.filter_by(username='admin').first()
            if admin:
                session['user_id'] = admin.id
                if request.endpoint != 'static':
                    return redirect(request.path)


# --- Main entry point ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Make sure tables are created
    app.run(host="0.0.0.0", port=5000, debug=True)
