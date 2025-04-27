import os
import json
import random
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secret key for session management

# Global variable for caching flashcards
flashcards_cache = {}

# Session timeout duration (in seconds)
SESSION_TIMEOUT = 900  # 15 minutes

# Helper function to get the file path for the current user
def get_user_file():
    """Return the path to the flashcard file for the logged-in user."""
    username = session.get('username')
    if username:
        return os.path.join('flashcards', f'{username}.json')  # Example path, adjust as necessary
    return None

# Check if the session has expired
def is_session_expired():
    """Check if the session has expired based on last activity time."""
    last_activity = session.get('last_activity')
    if not last_activity:
        return True

    # Check if the session has expired
    elapsed_time = time.time() - last_activity
    if elapsed_time > SESSION_TIMEOUT:
        return True

    return False

# Update session's last activity time
def update_session_activity():
    """Update the session activity time."""
    session['last_activity'] = time.time()

# Load flashcards from file, with caching
def load_flashcards():
    """Load flashcards for the logged-in user."""
    username = session.get('username')

    # Check if flashcards are already cached for this user
    if username in flashcards_cache:
        return flashcards_cache[username]

    user_file = get_user_file()
    if not user_file or not os.path.exists(user_file):
        flashcards_cache[username] = []  # Cache empty list if no file exists
        return []

    try:
        # Load flashcards from file
        with open(user_file, "r") as f:
            flashcards = json.load(f)
        flashcards_cache[username] = flashcards  # Cache the flashcards for future use
        return flashcards
    except (json.JSONDecodeError, IOError) as e:
        flashcards_cache[username] = []  # Cache empty list in case of an error
        print(f"Error loading flashcards for user {username}: {e}")
        return []

# Save flashcards to file
def save_flashcards(cards):
    """Save flashcards to the user's file."""
    user_file = get_user_file()
    if user_file:
        with open(user_file, 'w') as f:
            json.dump(cards, f)

# Route to manage flashcards
@app.route("/", methods=["GET", "POST"])
def index():
    """Display the flashcards and allow the user to add new ones."""
    if 'username' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('login'))

    # Check session timeout
    if is_session_expired():
        flash('Your session has expired. Please log in again.', 'error')
        session.pop('username', None)
        return redirect(url_for('login'))

    update_session_activity()  # Update session activity time

    flashcards = load_flashcards()

    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        if not question or not answer:
            flash('Please provide both a question and an answer.', 'error')
        else:
            new_flashcard = {"front": question, "back": answer}
            flashcards.append(new_flashcard)
            save_flashcards(flashcards)
            flash('Flashcard added successfully!', 'success')

    return render_template("index.html", flashcards=flashcards)

# Route to review flashcards
@app.route("/review", methods=["GET", "POST"])
def review():
    """Review mode where users can practice flashcards."""
    if 'username' not in session:
        flash('Please log in first!', 'error')
        return redirect(url_for('login'))

    # Check session timeout
    if is_session_expired():
        flash('Your session has expired. Please log in again.', 'error')
        session.pop('username', None)
        return redirect(url_for('login'))

    update_session_activity()  # Update session activity time

    flashcards = load_flashcards()

    if request.method == "POST":
        num_cards = int(request.form.get("num_cards", len(flashcards)))
        selected_cards = random.sample(flashcards, min(num_cards, len(flashcards)))
        return render_template("review_session.html", flashcards=selected_cards)

    return render_template("review_select.html", total=len(flashcards))

# Route to get all flashcards via the API
@app.route("/api/flashcards", methods=["GET"])
def get_flashcards():
    """API route to get all flashcards."""
    return jsonify(load_flashcards())

# Route to add a new flashcard via the API
@app.route("/api/flashcards", methods=["POST"])
def add_flashcard():
    """API route to add a new flashcard."""
    try:
        data = request.json
        question = data.get("front")
        answer = data.get("back")
        
        if not question or not answer:
            return jsonify({"status": "error", "message": "Missing 'front' or 'back'."}), 400
        
        flashcards = load_flashcards()
        flashcards.append(data)
        save_flashcards(flashcards)
        return jsonify({"status": "success"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session['username'] = username
            session['last_activity'] = time.time()  # Set initial activity time
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please enter a username.', 'error')

    return render_template("login.html")

# Route to logout
@app.route("/logout")
def logout():
    """Logout the user."""
    session.pop('username', None)
    session.pop('last_activity', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
