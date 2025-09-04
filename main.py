from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv


class Prompt(BaseModel):
    prompt: str

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})
def root():
    return {"message": "Hello, FastAPI!"}

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

@app.post("/hello", name="hello")
async def hello(request: Request):
    return HTMLResponse(content="Hello received!", status_code=200)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

