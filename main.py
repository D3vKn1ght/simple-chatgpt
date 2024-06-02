from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from g4f.client import Client

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class TextRequest(BaseModel):
    text: str

class Message(BaseModel):
    role: str 
    content: str

class ChatRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: list[Message] = [Message(role="user", content="Hello")]

client = Client()

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

@app.post("/ask")
def answer(request: QuestionRequest):
    return ask(request.question)

@app.post("/chat/")
def chat(chat_request: ChatRequest):
    try:
        messages=[{"role": message.role, "content": message.content} for message in chat_request.messages]
        print(messages)
        response = client.chat.completions.create(
            model=chat_request.model,
            messages=messages
        )        
        if response.choices:
            return response.choices[0].message.content
        else:
            return "Không nhận được phản hồi từ API."
    except Exception as e:
        raise HTTPException(status_code=500, detail="Có lỗi xảy ra, vui lòng thử lại sau")
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
