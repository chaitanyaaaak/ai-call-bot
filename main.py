from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from langdetect import detect

app = FastAPI()

@app.post("/voice")
async def handle_voice(
    From: str = Form(...),
    To: str = Form(...),
    SpeechResult: str = Form("Hello, is Chaitanya available?")
):
    try:
        lang = detect(SpeechResult)
    except:
        lang = "en"

    # Hindi response
    if lang == "hi":
        response_text = (
            "नमस्ते, मैं चैत्यन्य की सहायक हूं। वह अभी उपलब्ध नहीं हैं। "
            "मैं उन्हें सूचित कर दूंगी कि आपने कॉल किया था। धन्यवाद!"
        )
        voice = "Polly.Aditi"  # Indian female voice
        language = "hi-IN"
    else:
        # English polite assistant response
        response_text = (
            "Hello! I’m Chaitanya’s assistant. He is currently unavailable. "
            "Please let me know your message and I will notify him. "
            "Note: I cannot share personal information."
        )
        voice = "Polly.Joanna"
        language = "en-US"

    # TwiML response
    twiml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="{voice}" language="{language}">
            {response_text}
        </Say>
        <Pause length="2"/>
        <Say voice="{voice}" language="{language}">
            Thank you for calling. Goodbye.
        </Say>
    </Response>
    """

    return PlainTextResponse(content=twiml, media_type="application/xml")
