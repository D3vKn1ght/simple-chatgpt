from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from g4f.client import Client

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class TextRequest(BaseModel):
    text: str

client = Client(api_key="your_api_key_here")

def ask(question):
    global client
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Có lỗi xảy ra, vui lòng thử lại sau"

@app.get("/")
def read_root():
    return "Simple ChatGPT"

@app.post("/explain")
def explain(request: QuestionRequest):
    return ask(f"Explain in Vietnamese: {request.question}?")

@app.post("/translate")
def translate(request: TextRequest):
    return ask(f"Translate to Vietnamese: {request.text}")

@app.post("/ask-vi")
def answer(request: QuestionRequest):
    return ask(f"Answer my question in Vietnamese: {request.question}")

@app.post("/ask")
async def chat(request: QuestionRequest):
    return ask(request.question)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
