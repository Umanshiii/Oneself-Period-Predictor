from fastapi import APIRouter, Depends, HTTPException
from database import cycles_collection
from utils.jwt_handler import decode_jwt
from datetime import datetime
from utils.ml_helper import predict_next_period   # ⬅ NEW (ML PREDICTION)

router = APIRouter()

def get_user(token):
    decoded = decode_jwt(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")
    return decoded["user_id"]


# ---------------- Log cycle dates ---------------- #
@router.post("/add_period")
def add_period(token: str, start_date: str, end_date: str):
    user_id = get_user(token)
    cycles_collection.insert_one({
        "user_id": user_id,
        "start": start_date,
        "end": end_date
    })
    return {"msg": "Logged"}


# ---------------- Get Current Phase ---------------- #
@router.get("/phase")
def get_phase(token: str):
    user_id = get_user(token)
    last_cycle = cycles_collection.find({"user_id": user_id}).sort("_id", -1).limit(1)

    last_cycle = list(last_cycle)
    if not last_cycle:
        return {"phase": "unknown", "msg": "Log at least 1 cycle"}

    start = datetime.strptime(last_cycle[0]["start"], "%Y-%m-%d")
    current_date = datetime.utcnow()
    cycle_day = (current_date - start).days + 1

    if 1 <= cycle_day <= 5:
        phase = "Menstrual"
    elif 6 <= cycle_day <= 14:
        phase = "Follicular"
    elif cycle_day == 15:
        phase = "Ovulation"
    else:
        phase = "Luteal"

    return {"current_day": cycle_day, "phase": phase}


# ---------------- Predict Next Period (ML Model) ---------------- #
@router.get("/predict_next")
def predict_next_period_api(token: str):
    user_id = get_user(token)

    last_cycle = cycles_collection.find({"user_id": user_id}).sort("_id", -1).limit(1)
    last_cycle = list(last_cycle)

    if not last_cycle:
        raise HTTPException(status_code=400, detail="Not enough data for prediction")

    last_start = last_cycle[0]["start"]
    start_date = datetime.strptime(last_start, "%Y-%m-%d")

    # Estimate cycle length = difference between last logged start & end
    end_date = datetime.strptime(last_cycle[0]["end"], "%Y-%m-%d")
    cycle_length = (end_date - start_date).days + 1

    try:
        next_date = predict_next_period(last_start, cycle_length)
        return {
            "last_cycle_start": last_start,
            "cycle_length_estimated": cycle_length,
            "predicted_next_period": next_date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Error: {str(e)}")
