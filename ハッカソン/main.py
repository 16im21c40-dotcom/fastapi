from fastapi import FastAPI
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Prompt(BaseModel):
    message: str

@app.post("/chat")
def chat(prompt: Prompt):
    url = f"{os.getenv('AOAI_ENDPOINT')}/openai/deployments/{os.getenv('AOAI_DEPLOYMENT')}/chat/completions?api-version=2024-05-01"
    headers = {
        "api-key": os.getenv("AOAI_API_KEY"),
        "Content-Type": "application/json"
    }
    body = {
        "messages": [{"role": "user", "content": prompt.message}],
        "temperature": 0.7
    }
    res = requests.post(url, headers=headers, json=body)
    reply = res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}