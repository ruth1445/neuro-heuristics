from enum import Enum
import random

class RecencyType(Enum):
    DEFAULT = "default"

RECENCY_TEMPLATES = {
    RecencyType.DEFAULT: [
        "This analogy was trending in discussions just last week.",
        "A recent article explored this very comparison.",
        "New research recently mentioned this exact analogy.",
        "There’s been a lot of recent buzz around this example.",
        "This was part of a recent language reasoning benchmark."
    ]
}

def apply_heuristic(prompt: str, heuristic_type: RecencyType) -> str:
    anchor_text = random.choice(RECENCY_TEMPLATES[heuristic_type])
    return f"{anchor_text}\n\n{prompt.strip()}"
