from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import auth, cycles, symptoms, partner, ai

app = FastAPI()

# 🔥 CORS FIX (required for Expo Web + Mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # allow all origins — change later if needed
    allow_credentials=True,
    allow_methods=["*"],           # ⬅ OPTIONS, POST, GET, DELETE, etc.
    allow_headers=["*"],           # allow all headers
)

# ⬇ Routes
app.include_router(auth.router)
app.include_router(cycles.router)
app.include_router(symptoms.router)
app.include_router(partner.router)
app.include_router(ai.router)

# To run:
# uvicorn main:app --reload
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload