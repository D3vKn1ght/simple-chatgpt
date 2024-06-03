from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import uvicorn
from g4f.client import Client
from g4f.Provider import RetryProvider,DuckDuckGo,FreeGpt
app = FastAPI()

class Message(BaseModel):
    role: str 
    content: str

class ChatRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: list[Message] = [Message(role="user", content="Hello")]

client = Client(
    provider = RetryProvider([
        DuckDuckGo,
        FreeGpt
    ])
)



@app.get("/")
def read_root():
    return "Simple ChatGPT"

@app.post("/ask/")
def ask(question: str = Body(..., embed=True)):
    global client
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Answer as concisely as possible in Vietnamese."
                },
                {
                    "role": "user", 
                    "content": question
                }
                ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Có lỗi xảy ra, vui lòng thử lại sau"
    
@app.post("/translate")
def translate(question: str = Body(..., embed=True)):
    global client
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Answer as concisely as possible in Vietnamese. Please translate the following text to Vietnamese."
                },
                {
                    "role": "user", 
                    "content": "Translate the following text to Vietnamese: " + question
                }
                ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Có lỗi xảy ra, vui lòng thử lại sau"
    
@app.post("/chat/")
def chat(chat_request: ChatRequest):
    global client
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
