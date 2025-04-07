
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from whisper_transcriber import transcribe_audio
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(file_location)
    os.remove(file_location)
    return {"transcription": text}
