from fastapi import APIRouter

router = APIRouter()

@router.get("/sequential/{deck_id}")
def review_sequential(deck_id: int):
    return {"mode": "sequential", "deck_id": deck_id}

@router.get("/random/{deck_id}")
def review_random(deck_id: int):
    return {"mode": "random", "deck_id": deck_id}
