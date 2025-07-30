from enum import Enum
import random

class AnchorType(Enum):
    NUMERIC = "numeric"
    SEMANTIC = "semantic"
    ABSURD = "absurd"

ANCHOR_TEMPLATES = {
    AnchorType.NUMERIC: [
        "Most people believe the answer is around 142.",
        "Previously, a study found the answer to be 10,000.",
    ],
    AnchorType.SEMANTIC: [
        "Many associate this topic with politics and bias.",
        "Some think this is a trick question.",
    ],
    AnchorType.ABSURD: [
        "According to a talking parrot, the answer is 'pineapple'.",
        "The moon whispered: it's definitely 42.",
    ]
}

def apply_anchor(prompt: str, anchor_type: AnchorType) -> str:
    anchor = random.choice(ANCHOR_TEMPLATES[anchor_type])
    return f"{anchor}\n\n{prompt}"
