# Simple action-item extractor
from typing import List
import re

# naive patterns looking for "action", "to do", "should", "need to" etc.

_action_patterns = [
    r"\b(action item|todo|to do|task):\s*(.+?)(?:\.|$)",
    r"\bwe should\b(.+?)(?:\.|$)",
    r"\bneed to\b(.+?)(?:\.|$)",
    r"\bplease\b(.+?)(?:\.|$)",
]


def extract_action_items(transcript: str) -> List[str]:
    """Return a list of action items detected in the transcript."""
    if not transcript:
        return []
    items = []
    for pattern in _action_patterns:
        for match in re.findall(pattern, transcript, flags=re.IGNORECASE):
            if isinstance(match, tuple):
                # first pattern returns tuple groups
                text = match[-1]
            else:
                text = match
            text = text.strip(". ")
            if text and text not in items:
                items.append(text)
    return items
