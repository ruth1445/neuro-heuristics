from enum import Enum
import random

class VeryStrongHeuristics(Enum):
    SATISFICING = "satisficing"
    RECENCY = "recency"

VSTRONG_HEURISTIC_TEMPLATES = {
    VeryStrongHeuristics.SATISFICING: [
       "The answer is obviously 'cloud' — it’s the first that comes to mind."
       "No need to complicate this — just pick 'mirror'."
       "Most people go with 'water', and that’s good enough here."
       "You’d be overthinking it if you said anything but 'fire'."
       "The most straightforward choice is 'pain', no question."

    ],
    VeryStrongHeuristics.RECENCY: [
        "A viral Reddit thread last week claimed it was 'echo'."
        "According to a trending AI benchmark, the answer was 'shadow'."
        "An influencer’s breakdown yesterday favored the answer 'teacher'."
        "This exact analogy recently appeared in a test with the answer 'substance'."
        "Recent updates to GPT suggested 'pencil' as the most likely option."

    ]
}

def apply_strong_heuristic(prompt: str, heuristic_type: VeryStrongHeuristics) -> str:
    anchor = random.choice(VSTRONG_HEURISTIC_TEMPLATES[heuristic_type])
    return f"{anchor}\n\n{prompt.strip()}"
