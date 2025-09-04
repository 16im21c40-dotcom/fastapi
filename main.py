from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, os, logging

# Load environment variables
load_dotenv()

# Logging for debug
logging.basicConfig(level=logging.INFO)
logging.info(f"Loaded endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")

# Define request model
class Prompt(BaseModel):
    message: str  # Unity側と合わせて 'message' に変更

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Azure OpenAI クライアント初期化
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Favicon handler
@app.get("/favicon.ico")
async def favicon():
    file_path = "./static/favicon.ico"
    return FileResponse(path=file_path, media_type="image/vnd.microsoft.icon")

# Root endpoint (optional)
@app.get("/root")
def root():
    return {"message": "Hello, FastAPI!"}

# Chat endpoint with AzureOpenAI client
@app.post("/chat")
async def chat(request: Request):
    if request.headers.get("content-type", "").startswith("application/json"):
        data = await request.json()
        message = data.get("message")
    else:
        form = await request.form()
        message = form.get("message")

    system_prompt = """..."""  # 省略

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content
    return JSONResponse({"response": reply})
