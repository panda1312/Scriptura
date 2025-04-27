from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import random
import os

app = Flask(__name__)  # Initialize the Flask app

DATA_FILE = "/data/flashcards.json"  # JSON file to store flashcards

# Function to load flashcards from the JSON file
def load_flashcards():
    if not os.path.exists(DATA_FILE):  # If the file doesn't exist yet
        return []  # Return an empty list
    with open(DATA_FILE, "r") as f:
        return json.load(f)  # Load and return the list of flashcards

# Function to save flashcards to the JSON file
def save_flashcards(cards):
    with open(DATA_FILE, "w") as f:
        json.dump(cards, f, indent=2)  # Save with indentation for readability

# Route to serve the main web page
@app.route("/")
def index():
    return render_template("index.html")  # Serves the HTML page

# Route to serve the review page
@app.route("/review", methods=["GET", "POST"])
def review():
    with open(DATA_FILE, 'r') as f:
        flashcards = json.load(f)

    if request.method == "POST":
        num_cards = int(request.form.get("num_cards", len(flashcards)))
        selected_cards = random.sample(flashcards, min(num_cards, len(flashcards)))
        return render_template("review_session.html", flashcards=selected_cards)

    return render_template("review_select.html", total=len(flashcards))

# API route to return all flashcards as JSON
@app.route("/api/flashcards", methods=["GET"])
def get_flashcards():
    return jsonify(load_flashcards())

# API route to add a new flashcard (called via JavaScript POST request)
@app.route("/api/flashcards", methods=["POST"])
def add_flashcard():
    data = request.json  # Get flashcard data sent by frontend
    cards = load_flashcards()  # Load current cards
    cards.append(data)  # Add the new one
    save_flashcards(cards)  # Save updated list
    return jsonify({"status": "success"}), 201  # Return a success response

# Run the app in debug mode when executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
