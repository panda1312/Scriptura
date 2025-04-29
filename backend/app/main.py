from fastapi import FastAPI
from app.api import users, decks, flashcards, review
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(decks.router, prefix="/decks", tags=["decks"])
app.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])
app.include_router(review.router, prefix="/review", tags=["review"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Scriptura"}
