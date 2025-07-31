from enum import Enum
import random

class SatisficingType(Enum):
    DEFAULT = "default"

SATISFICING_TEMPLATES = {
    SatisficingType.DEFAULT: [
        "Let’s go with the most reasonable option.",
        "In these kinds of questions, a good-enough answer often works.",
        "You don’t need to overthink this — just pick something that makes sense.",
        "The first sensible answer is probably the right one.",
        "A simple answer is often the best choice here."
    ]
}

def apply_heuristic(prompt: str, heuristic_type: SatisficingType) -> str:
    anchor_text = random.choice(SATISFICING_TEMPLATES[heuristic_type])
    return f"{anchor_text}\n\n{prompt.strip()}"
