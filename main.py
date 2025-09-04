from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, os, uvicorn

# Load environment variables
load_dotenv()

# Define request model
class Prompt(BaseModel):
    message: str  # Unity側と合わせて 'message' に変更

# Initialize FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Azure OpenAI 초기화
client = AzureOpenAI(
    api_key=os.getenv("CL5Dg9EWcCnVG4GltHwfOTYsutRnrFFW9cr8IAotSyLkwv8hAkTwJQQJ99BIACHYHv6XJ3w3AAAAACOGs0SY"),
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("https://ps050-mf4p2jno-eastus2.cognitiveservices.azure.com/")
)


@app.post("/chat")
async def chat(message: str = Form(...)):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": message}]
    )
    answer = response.choices[0].message.content
    return JSONResponse({"response": answer})

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Request for index page received")
    return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/", response_class=HTMLResponse)
# async def get_form(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# # Index page
# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     print('Request for index page received')
#     return templates.TemplateResponse('index.html', {"request": request})

# Favicon handler
@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

# Root endpoint (optional)
@app.get("/root")
def root():
    return {"message": "Hello, FastAPI!"}

# Chat endpoint with Azure OpenAI integration
@app.post("/chat")
async def chat(prompt: Prompt):
    system_prompt = """
    あなたは会話分析の専門家です。以下のユーザー発言から、
    1. 要点を簡潔に抽出し、
    2. 論理的・感情的・利他的な視点から応答を構築してください。
    出力は以下の形式で：
    {
      "summary": "...",
      "perspectives": {
        "logical": "...",
        "emotional": "...",
        "altruistic": "..."
      }
    }
    """

    body = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt.message}
        ],
        "temperature": 0.7
    }

    url = f"{os.getenv('AOAI_ENDPOINT')}/openai/deployments/{os.getenv('AOAI_DEPLOYMENT')}/chat/completions?api-version=2024-05-01"
    headers = {
        "api-key": os.getenv("AOAI_API_KEY"),
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=body)

    if res.status_code != 200:
        return {"error": f"Azure OpenAI API failed with status {res.status_code}", "details": res.text}

    reply = res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}

# Simple hello endpoint
@app.post("/hello", name="hello")
async def hello(request: Request):
    return HTMLResponse(content="Hello received!", status_code=200)

# Run the app
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
