from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from gtts import gTTS
from langdetect import detect
import os

app = FastAPI()

@app.post("/voice")
async def voice_handler():
    # Simulate what caller says (replace this later with real input)
    caller_text = "Namaste, kya Chaitanya available hain?"

    try:
        lang = detect(caller_text)
    except:
        lang = 'en'

    # Define response based on language
    if lang == 'hi':
        response_text = "Sorry, this assistant currently supports only English. Please call again in English."
    else:
        response_text = (
            "Hello, this is Chaitanya's assistant. "
            "He is currently unavailable. Please call back later. "
            "Note: This is an automated system and cannot share any personal information."
        )

    # Create static folder if not exists
    os.makedirs("static", exist_ok=True)

    # Save response audio
    tts = gTTS(text=response_text, lang='en')
    filename = "static/response.mp3"
    tts.save(filename)

    # Return TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Play>https://ai-call-bot-4id2.onrender.com/static/response.mp3</Play>
</Response>"""


    return PlainTextResponse(content=twiml, media_type="application/xml")
