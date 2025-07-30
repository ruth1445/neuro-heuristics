from typing import List, Dict

def get_analogy_tasks() -> List[Dict[str, str]]:
    return [
        {"input": "doctor is to hospital as teacher is to", "expected": "school"},
        {"input": "fire is to hot as ice is to", "expected": "cold"},
        {"input": "bird is to fly as fish is to", "expected": "swim"},
        {"input": "painter is to brush as writer is to", "expected": "pen"},
    ]
