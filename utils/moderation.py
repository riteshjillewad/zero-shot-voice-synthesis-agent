import re
from transformers import pipeline

# Lazy load model only once
moderator = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

# Violence / hate keywords
BLOCK_WORDS = [
    "kill", "murder", "bomb", "shoot",
    "rape", "terrorist", "destroy",
    "genocide", "slaughter"
]

# Suspicious phrases
PATTERNS = [
    r"kill all",
    r"attack .* people",
    r"wipe out",
    r"burn them"
]


def keyword_check(text):
    txt = text.lower()

    for word in BLOCK_WORDS:
        if word in txt:
            return False, f"Blocked keyword: {word}"

    for pattern in PATTERNS:
        if re.search(pattern, txt):
            return False, "Blocked violent phrase"

    return True, "Safe"


def ai_check(text):
    result = moderator(text)[0]

    label = result["label"].lower()
    score = result["score"]

    if "toxic" in label and score > 0.75:
        return False, f"Toxic content detected ({score:.2f})"

    return True, "Safe"


def is_safe_text(text):
    # Layer 1: keyword filter
    safe, msg = keyword_check(text)

    if not safe:
        return False, msg

    # Layer 2: AI model only for longer text
    if len(text.split()) >= 4:
        safe, msg = ai_check(text)
        if not safe:
            return False, msg

    return True, "Safe"
