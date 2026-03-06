# AI Meeting Notes Generator

This repository contains a full-stack web application that generates meeting notes from audio/video uploads using AI.

## Features

- Upload meeting recordings (mp3, wav, mp4)
- Convert video to audio with FFmpeg
- Transcribe using Whisper
- Generate summaries and action items
- Store data in SQLite
- Dashboard to view transcripts, summaries, and tasks

## Structure

```
ai-meeting-notes/
│
├── backend
│   ├── main.py
│   ├── whisper_service.py
│   ├── summarizer.py
│   ├── action_items.py
│   ├── database.py
│   └── models.py
├── frontend
│   ├── src
│       ├── UploadPage.jsx
│       ├── Dashboard.jsx
│       └── MeetingView.jsx
├── recordings
├── scripts
│   └── git_reminder.py
├── requirements.txt
└── README.md
```

## Running Backend

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # on Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have the FFmpeg binary installed and available on your PATH. On Windows you can download from https://ffmpeg.org/download.html and add `ffmpeg.exe` to your path.

4. Start the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Open `http://localhost:8000` to see the welcome message.

## API Endpoints

* `POST /upload` – upload a `.mp3`, `.wav` or `.mp4` file. Returns meeting ID.
* `GET /meetings` – list all imported meetings (id + filename).
* `GET /meetings/{id}` – retrieve a single meeting record with transcript, summary, and actions.

Sample curl to fetch a meeting:

```bash
curl http://localhost:8000/meetings/1
```
