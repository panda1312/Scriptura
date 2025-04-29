from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database, auth

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new flashcard
@router.post("/{deck_id}", response_model=schemas.FlashcardOut)
def create_flashcard(
    deck_id: int,
    flashcard: schemas.FlashcardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_flashcard = models.Flashcard(
        front_text=flashcard.front_text,
        back_text=flashcard.back_text,
        deck_id=deck_id
    )
    db.add(new_flashcard)
    db.commit()
    db.refresh(new_flashcard)
    return new_flashcard

# Endpoint to read all flashcards for a given deck
@router.get("/{deck_id}", response_model=List[schemas.FlashcardOut])
def read_flashcards(
    deck_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Flashcard).filter(models.Flashcard.deck_id == deck_id).all()
