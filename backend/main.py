from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import random
import asyncio

app = FastAPI()

# Serve the static frontend (index.html, script.js, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def get_index():
    return FileResponse("frontend/index.html")

# Simulated AI endpoint (connects to your JS function later)
@app.get("/chat")
async def get_ai_response(message: str):
    responses = [
        "That's an interesting question! Let me think about that...",
        "I understand what you're asking. Here's what I think...",
        "Great question! Based on my knowledge, I would say...",
        "I'm here to help! Let me provide you with some information...",
        "That's a thoughtful inquiry. Here's my perspective..."
    ]
    await asyncio.sleep(random.uniform(1, 2))
    response = random.choice(responses)
    return {"response": f'{response} You said: "{message}".'}

