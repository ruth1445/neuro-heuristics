import openai
import os
from heuristics.anchoring import apply_anchor, AnchorType
from tasks.analogies import get_analogy_tasks
from datetime import datetime
import json

openai.api_key = os.getenv("OPENAI_API_KEY")  # Assumes your key is set in env

def query_llm(prompt: str, model="gpt-3.5-turbo") -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def run(anchor_type: AnchorType):
    tasks = get_analogy_tasks()
    results = []

    for task in tasks:
        anchored_prompt = apply_anchor(f"What is the best answer to this analogy?\n{task['input']}", anchor_type)
        response = query_llm(anchored_prompt)
        results.append({
            "prompt": task["input"],
            "anchored_prompt": anchored_prompt,
            "response": response,
            "expected": task["expected"]
        })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"outputs/anchoring_results_{anchor_type.value}_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    run(AnchorType.NUMERIC)  # You can change this to SEMANTIC or ABSURD
