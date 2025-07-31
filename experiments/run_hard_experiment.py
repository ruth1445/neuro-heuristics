import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import random
from datetime import datetime
from openai import OpenAI

from heuristics.strong_heuristics import apply_strong_heuristic, StrongHeuristicType
from tasks.hard_analogies import HARD_ANALOGY_QUESTIONS

client = OpenAI()

def query_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def run_experiment(heuristic_name, heuristic_type):
    results = []
    for item in HARD_ANALOGY_QUESTIONS:
        question = item["question"]
        answer = item["answer"]

        modified_prompt = apply_strong_heuristic(question, heuristic_type)
        response = query_llm(modified_prompt)

        print("\nPrompt:")
        print("-" * 40)
        print(modified_prompt)
        print("\nResponse:", response)

        results.append({
            "question": question,
            "expected": answer,
            "response": response,
            "heuristic": heuristic_name,
        })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{heuristic_name}_hard_results_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {filename}")

if __name__ == "__main__":
    print("\nRunning STRONG SATISFICING...")
    run_experiment("strong_satisficing", StrongHeuristicType.SATISFICING)

    print("\nRunning STRONG RECENCY...")
    run_experiment("strong_recency", StrongHeuristicType.RECENCY)

