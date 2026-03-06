# Summarization logic using HuggingFace transformers

from transformers import pipeline

# create a global summarizer pipeline; it may download model on first use
_summarizer = None

def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        # using a small model to keep resource usage reasonable
        _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return _summarizer


def generate_summary(transcript: str) -> str:
    """Generate a summary text from the transcript."""
    if not transcript:
        return ""
    summarizer = _get_summarizer()
    # HuggingFace summarizer has a max token length; split if very long
    max_chunk = 1000  # characters approximate
    chunks = [transcript[i:i+max_chunk] for i in range(0, len(transcript), max_chunk)]
    summaries = []
    for chunk in chunks:
        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summaries.append(result[0]['summary_text'])
    return "\n".join(summaries)
