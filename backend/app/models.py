from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    preferences = Column(Text)  # Store user preferences as JSON

    decks = relationship("Deck", back_populates="owner")

    def get_preferences(self):
        """Return preferences as a dictionary."""
        if self.preferences:
            return json.loads(self.preferences)
        return {}

    def set_preferences(self, new_preferences):
        """Store preferences as a JSON string."""
        self.preferences = json.dumps(new_preferences)

    def get_theme(self):
        """Get the theme preference ('light' or 'dark')."""
        preferences = self.get_preferences()
        return preferences.get("theme", "light")  # Default to light theme

    def set_theme(self, theme: str):
        """Set the theme preference."""
        preferences = self.get_preferences()
        preferences["theme"] = theme
        self.set_preferences(preferences)

class Deck(Base):
    __tablename__ = "decks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="decks")
    flashcards = relationship("Flashcard", back_populates="deck")

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    front_text = Column(Text)
    back_text = Column(Text)
    deck_id = Column(Integer, ForeignKey("decks.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    review_data = Column(Text)

    deck = relationship("Deck", back_populates="flashcards")
