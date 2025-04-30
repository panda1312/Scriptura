from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class DeckBase(BaseModel):
    name: str

class DeckCreate(DeckBase):
    pass

class DeckOut(DeckBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class FlashcardBase(BaseModel):
    front_text: str
    back_text: str

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardOut(FlashcardBase):
    id: int
    deck_id: int
    class Config:
        orm_mode = True

class ThemeUpdate(BaseModel):
    theme: str
