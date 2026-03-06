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
    # save the incoming file
    filename = file.filename
    if not filename.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    file_path = os.path.join(RECORDINGS_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # convert video to audio if needed
    try:
        from .whisper_service import convert_to_wav, transcribe_audio
        from .summarizer import generate_summary
        from .action_items import extract_action_items
        from .database import SessionLocal
        from .models import Meeting
        import json
    except Exception as e:
        # import failure
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    try:
        audio_path = convert_to_wav(file_path)
        # transcribe using Whisper (may take some time)
        transcript = transcribe_audio(audio_path)
        # generate summary and actions
        summary = generate_summary(transcript)
        actions = extract_action_items(transcript)
    except Exception as e:
        # log to console
        import traceback, sys
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

    try:
        db = SessionLocal()
        meeting = Meeting(
            filename=filename,
            transcript=transcript,
            summary=summary,
            actions=json.dumps(actions),
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return {
    "meeting_id": meeting.id,
    "filename": filename,
    "transcript": transcript,
    "summary": summary,
    "action_items": actions
}
