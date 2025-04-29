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

# Endpoint to create a new deck
@router.post("/", response_model=schemas.DeckOut)
def create_deck(
    deck: schemas.DeckCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_deck = models.Deck(name=deck.name, user_id=current_user.id)
    db.add(new_deck)
    db.commit()
    db.refresh(new_deck)
    return new_deck

# Endpoint to read all decks for the current user
@router.get("/", response_model=List[schemas.DeckOut])
def read_decks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Deck).filter(models.Deck.user_id == current_user.id).all()
