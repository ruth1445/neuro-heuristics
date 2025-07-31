import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from datetime import datetime
from openai import OpenAI

from heuristics.anchoring import apply_anchor, AnchorType
from heuristics.satisficing import apply_heuristic as apply_satisficing, SatisficingType
from heuristics.recency import apply_heuristic as apply_recency, RecencyType

from tasks.analogy_tasks import ANALOGY_QUESTIONS

device = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def query_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def run_experiment(heuristic_name, apply_fn, heuristic_type):
    results = []
    for item in ANALOGY_QUESTIONS:
        question = item["question"]
        answer = item["answer"]

        modified_prompt = apply_fn(question, heuristic_type)
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
    filename = f"outputs/{heuristic_name}_results_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {filename}")

if __name__ == "__main__":
    print("Running NUMERIC anchor...")
    run_experiment("anchoring_numeric", apply_anchor, AnchorType.NUMERIC)

    print("\nRunning SATISFICING...")
    run_experiment("satisficing", apply_satisficing, SatisficingType.DEFAULT)

    print("\nRunning RECENCY...")
    run_experiment("recency", apply_recency, RecencyType.DEFAULT)

