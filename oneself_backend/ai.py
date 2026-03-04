from fastapi import APIRouter
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/ask_ai")
def ask_ai(query: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return {"answer": response.choices[0].message["content"]}
    except Exception as e:
        return {"error": str(e)}
