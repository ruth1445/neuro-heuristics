import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "outputs"

def load_and_score(file_path):
    with open(file_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    # Drop mock responses
    df = df[df["response"] != "[Mocked LLM response here]"]

    df["correct"] = df.apply(
    lambda row: row["expected"].strip().lower() in row["response"].strip().lower(),
    axis=1
    )

    df["response_length"] = df["response"].apply(lambda r: len(r.split()))
    df["contains_uncertainty"] = df["response"].str.lower().str.contains(
    "maybe|probably|i think|perhaps|not sure|could be"
    )

    df["anchor_type"] = file_path.split("_results_")[1].split("_")[0]
    df["correct"] = df.apply(
    lambda row: row["expected"].strip().lower() in row["response"].strip().lower(),
    axis=1
    )
    df = df[df["response"] != "[Mocked LLM response here]"]

    return df

dfs = []
for filename in os.listdir(OUTPUT_DIR):
    if filename.endswith(".json") and "anchoring_results" in filename:
        full_path = os.path.join(OUTPUT_DIR, filename)
        df = load_and_score(full_path)
        dfs.append(df)

full_df = pd.concat(dfs, ignore_index=True)

df = full_df.copy()
df["anchored_prompt"] = df["anchored_prompt"].str.replace("\n", " ")
df["response"] = df["response"].str.replace("\n", " ")
df.to_csv("outputs/scored_all_cleaned.csv", index=False)
print(" Cleaned CSV saved as: outputs/scored_all_cleaned.csv")

print("\n Accuracy by anchor type:")
print(full_df.groupby("anchor_type")["correct"].mean())

plt.figure(figsize=(6,4))
full_df.groupby("anchor_type")["correct"].mean().plot(kind="bar", color="skyblue")
plt.title("Accuracy by Anchoring Heuristic")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "anchor_accuracy.png"))
plt.show()

plt.figure(figsize=(8, 5))
sns.barplot(data=full_df, x="anchor_type", y="correct", ci=None, palette="muted")
plt.title("Accuracy by Anchor Type")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("outputs/plot_accuracy_by_anchor.png")

plt.figure(figsize=(8, 5))
sns.boxplot(data=full_df, x="anchor_type", y="response_length", palette="pastel")
plt.title("Response Length by Anchor Type")
plt.ylabel("Word Count")
plt.tight_layout()
plt.savefig("outputs/plot_length_by_anchor.png")

plt.figure(figsize=(8, 5))
sns.barplot(data=full_df, x="anchor_type", y="contains_uncertainty", ci=None, palette="coolwarm")
plt.title("Uncertainty Language Frequency by Anchor Type")
plt.ylabel("Proportion of Responses with Hedging")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("outputs/plot_uncertainty_by_anchor.png")

