from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.openai_chat import ask_openai


app = FastAPI()

class PromtRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: PromtRequest):
    try:
        response = ask_openai(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))