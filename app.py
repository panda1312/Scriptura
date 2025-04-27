from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session security

DATA_FOLDER = "/data"  # All flashcard data stored per user here

# --- Helper functions ---

def get_user_file():
    """Returns the flashcard file path for the current user."""
    username = session.get('username')
    if not username:
        return None
    return os.path.join(DATA_FOLDER, f"{username}_flashcards.json")

def load_flashcards():
    """Load flashcards for the logged-in user."""
    user_file = get_user_file()
    if not user_file or not os.path.exists(user_file):
        return []
    with open(user_file, "r") as f:
        return json.load(f)

def save_flashcards(cards):
    """Save flashcards for the logged-in user."""
    user_file = get_user_file()
    if user_file:
        with open(user_file, "w") as f:
            json.dump(cards, f, indent=2)

# --- Routes ---

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page where users can enter a username."""
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/")
def index():
    """Main page showing the list of flashcards."""
    if 'username' not in session:
        return redirect(url_for('login'))

    flashcards = load_flashcards()
    return render_template("index.html", flashcards=flashcards)

@app.route("/review", methods=["GET", "POST"])
def review():
    """Review mode where users can practice flashcards."""
    if 'username' not in session:
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
    return jsonify(load_flashcards())

@app.route("/api/flashcards", methods=["POST"])
def add_flashcard():
    """API route to add a new flashcard."""
    data = request.json
    cards = load_flashcards()
    cards.append(data)
    save_flashcards(cards)
    return jsonify({"status": "success"}), 201

# --- Main entry point ---

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
