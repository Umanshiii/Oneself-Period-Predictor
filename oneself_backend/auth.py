from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from database import users_collection
from utils.jwt_handler import sign_jwt

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------- Request Body Models ----------
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


# -------- SIGNUP API ----------
@router.post("/signup")
def signup(data: SignupRequest):
    name = data.name
    email = data.email
    password = data.password[:72]  # Prevent bcrypt crash (>72 bytes)

    # Check duplicate email
    existing = users_collection.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = pwd_context.hash(password)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed
    })

    return {"message": "Signup successful, please login."}


# -------- LOGIN API ----------
@router.post("/login")
def login(data: LoginRequest):
    email = data.email
    password = data.password[:72]

    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = sign_jwt(str(user["_id"]))
    return {"message": "Login successful", "token": token}
