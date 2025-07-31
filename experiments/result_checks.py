import pandas as pd

# Load your cleaned results
df = pd.read_csv("outputs/scored_all_cleaned.csv")

print("Data Preview:")
print(df.head(5))
print("\nNumber of Rows:", len(df))

# 1. Check anchor type counts
print("\nAnchor Types Count:")
print(df["anchor_type"].value_counts(dropna=False))

# 2. Check for mock responses
print("\nMock Responses Present?")
print(df["response"].str.contains("Mocked LLM", na=False).value_counts())

# 3. Check unique anchor phrases
if "anchor_text" in df.columns:
    print("\nUnique Anchor Texts:")
    print(df["anchor_text"].dropna().unique())
else:
    print("\n'anchor_text' column missing")

# 4. Check correctness logic
print("\nCorrectness Breakdown:")
print(df["correct"].value_counts(dropna=False))

# 5. Compare response vs. expected
print("\nSample Expected vs Response:")
sample = df[["expected", "response", "correct"]].sample(n=min(5, len(df)))
print(sample.to_string(index=False))

# 6. Check response lengths
if "response_length" in df.columns:
    print("\nResponse Lengths (summary):")
    print(df["response_length"].describe())
else:
    print("\n'response_length' column missing")

# 7. Check uncertainty flag
if "contains_uncertainty" in df.columns:
    print("\nUncertainty Flag Breakdown:")
    print(df["contains_uncertainty"].value_counts(dropna=False))
else:
    print("\n'contains_uncertainty' column missing")

