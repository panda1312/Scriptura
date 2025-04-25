from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)  # Initialize the Flask app

DATA_FILE = "flashcards.json"  # JSON file to store flashcards

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
    app.run(debug=True)
