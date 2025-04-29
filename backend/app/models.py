from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    preferences = Column(Text)

    decks = relationship("Deck", back_populates="owner")

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
