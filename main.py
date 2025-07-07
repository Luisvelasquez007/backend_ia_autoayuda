from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import openai
import os
from dotenv import load_dotenv
import io

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Permitir llamadas desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza con tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(prompt: str = Form(...)):
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un coach de autoayuda empático, cálido y profesional."},
            {"role": "user", "content": prompt}
        ]
    )
    respuesta = completion.choices[0].message["content"]
    return JSONResponse(content={"response": respuesta})

@app.post("/voz")
async def voz(texto: str = Form(...)):
    audio = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=texto
    )
    return StreamingResponse(io.BytesIO(audio.content), media_type="audio/mpeg")
