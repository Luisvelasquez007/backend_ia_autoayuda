from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
import io

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Permitir llamadas desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(prompt: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un coach de autoayuda empático, cálido y profesional."},
                {"role": "user", "content": prompt}
            ]
        )
        respuesta = response.choices[0].message.content
        return JSONResponse(content={"response": respuesta})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/voz")
async def voz(texto: str = Form(...)):
    try:
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=texto
        )
        return StreamingResponse(io.BytesIO(speech_response.content), media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

