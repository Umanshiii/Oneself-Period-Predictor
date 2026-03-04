from fastapi import APIRouter
from database import users_collection, symptoms_collection, cycles_collection

router = APIRouter()

@router.get("/partner_view")
def partner_view(girl_email: str):
    # Find the girl by email
    girl = users_collection.find_one({"email": girl_email})
    if not girl:
        return {"error": "User not found"}

    # Convert ObjectId to string
    girl["_id"] = str(girl["_id"])

    # Fetch last symptom entry
    last_symptom = symptoms_collection.find_one(
        {"user_id": girl["_id"]},
        sort=[("_id", -1)]
    )
    if last_symptom:
        last_symptom["_id"] = str(last_symptom["_id"])

    # Fetch last cycle entry
    last_cycle = cycles_collection.find_one(
        {"user_id": girl["_id"]},
        sort=[("_id", -1)]
    )
    if last_cycle:
        last_cycle["_id"] = str(last_cycle["_id"])

    return {
        "name": girl["name"],
        "email": girl["email"],
        "last_phase_data": last_cycle,
        "last_symptom_data": last_symptom
    }
