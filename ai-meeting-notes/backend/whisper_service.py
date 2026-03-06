import os
import ffmpeg

# for actual whisper functionality we'll import the model lazily to avoid heavy startup

def convert_to_wav(input_path: str) -> str:
    """If the input is a video file, convert it to a WAV audio file and return its path.
    Otherwise, return the original path."""
    ext = os.path.splitext(input_path)[1].lower()
    if ext in (".mp4", ".mov", ".mkv"):
        output_path = os.path.splitext(input_path)[0] + ".wav"
        # simple conversion using ffmpeg-python wrapper
        try:
            ffmpeg.input(input_path).output(output_path, format="wav", acodec="pcm_s16le", ac=1, ar="16000").run(overwrite_output=True)
        except ffmpeg.Error as e:
            # provide more context if ffmpeg isn't found or fails
            raise RuntimeError(f"ffmpeg conversion failed: {e.stderr.decode() if hasattr(e, 'stderr') else e}")
        return output_path
    return input_path


def transcribe_audio(file_path: str) -> str:
    """Transcribe the given audio file using Whisper and return the text."""
    # lazy import of whisper to avoid import time if not needed
    try:
        import whisper
    except ImportError:
        raise RuntimeError("whisper library is not installed")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result.get("text", "")
