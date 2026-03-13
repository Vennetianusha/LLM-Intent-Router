from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from router import process_message
import os

app = FastAPI(title="LLM Prompt Router API")

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    intent: str
    confidence: float
    response: str

@app.get("/")
async def root():
    return {"message": "LLM Prompt Router is running. Use /classify endpoint to route messages."}

@app.post("/classify", response_model=MessageResponse)
async def classify_and_route(request: MessageRequest):
    try:
        response_text, classification = process_message(request.message)
        return MessageResponse(
            intent=classification["intent"],
            confidence=classification["confidence"],
            response=response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
