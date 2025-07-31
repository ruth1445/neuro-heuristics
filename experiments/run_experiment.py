import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from datetime import datetime
from openai import OpenAI
from heuristics.anchoring import apply_anchor, AnchorType
from tasks.analogies import get_analogy_tasks

MODEL = "gpt-4o"
MAX_BUDGET = 5.00  
USE_MOCK = False  
MAX_TOKENS = 10

COST_PER_1K_INPUT = 0.005
COST_PER_1K_OUTPUT = 0.015
client = OpenAI()
total_cost = 0.0

def query_llm(prompt: str, model=MODEL) -> str:
    global total_cost

    if USE_MOCK:
        print(f"\n Mock LLM received prompt:\n{'-'*40}\n{prompt}\n{'-'*40}")
        return "[Mocked LLM response here]"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=MAX_TOKENS,
    )

    usage = response.usage
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    cost = (input_tokens / 1000 * COST_PER_1K_INPUT) + (output_tokens / 1000 * COST_PER_1K_OUTPUT)
    total_cost += cost

    print(f"\n Prompt: {prompt[:50]}...")
    print(f" Tokens — Input: {input_tokens}, Output: {output_tokens}")
    print(f" Cost this call: ${cost:.5f} | Total: ${total_cost:.4f}")

    if total_cost > MAX_BUDGET:
        raise RuntimeError(" Cost limit exceeded!")

    return response.choices[0].message.content.strip()

def run(anchor_type: AnchorType):
    tasks = get_analogy_tasks()
    results = []

    for task in tasks:
        from heuristics.anchoring import ANCHOR_TEMPLATES
        anchor_text = random.choice(ANCHOR_TEMPLATES[anchor_type])
        anchored_prompt = f"{anchor_text}\n\nWhat is the best answer to this analogy?\n{task['input']}"

        try:
            response = query_llm(anchored_prompt)
        except RuntimeError as e:
            print(e)
            break

        results.append({
            "prompt": task["input"],
            "anchored_prompt": anchored_prompt,
            "anchor_text": anchor_text,
            "response": response,
            "expected": task["expected"]
        })

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/anchoring_results_{anchor_type.value}_{timestamp}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f" Results saved to: {output_file}")

if __name__ == "__main__":
    for anchor in [AnchorType.NUMERIC, AnchorType.SEMANTIC, AnchorType.ABSURD]:
        print(f"\n Running experiment with anchor: {anchor.value.upper()}")
        run(anchor)

    print(f"\n Finished all anchor types. Total cost: ${total_cost:.4f}")

