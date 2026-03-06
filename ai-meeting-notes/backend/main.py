from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI(title="AI Meeting Notes API")

from .database import engine
from .models import Base

# create database tables
Base.metadata.create_all(bind=engine)

RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'recordings')
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

@app.get("/")
def read_root():
    return {"message": "AI Meeting Notes API is running"}

@app.post("/upload")
async def upload_meeting(file: UploadFile = File(...)):
    # simple file save
    filename = file.filename
    if not filename.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = os.path.join(RECORDINGS_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": filename, "status": "saved"}
