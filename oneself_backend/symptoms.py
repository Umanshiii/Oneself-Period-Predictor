from fastapi import APIRouter
from database import symptoms_collection
from utils.jwt_handler import decode_jwt

router = APIRouter()

@router.post("/add_symptom")
def add_symptom(token: str, cramps: int = 0, mood: str = "", energy: int = 0):
    user = decode_jwt(token)
    symptoms_collection.insert_one({
        "user_id": user["user_id"],
        "cramps": cramps,
        "mood": mood,
        "energy": energy
    })
    return {"msg": "Symptom logged"}
