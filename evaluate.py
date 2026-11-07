import os
import pandas as pd
from agent import run_agent, df

labels = pd.read_csv("data/labels.csv", dtype=str)
rows = []

for _, label in labels.iterrows():
    supplier_id = label["supplier_id"]
    record = df[df["supplier_id"] == supplier_id].iloc[0].to_dict()
    result = run_agent(record, show_steps=False)
    expected = label["expected_clean"] == "yes"
    rows.append({
        "supplier_id": supplier_id,
        "expected_clean": expected,
        "agent_clean": result["clean"],
        "correct": result["clean"] == expected,
        "agent_issues": "; ".join(result["issues"]),
    })
    print(supplier_id, "correct" if rows[-1]["correct"] else "WRONG")

results = pd.DataFrame(rows)
os.makedirs("output", exist_ok=True)
results.to_csv("output/evaluation.csv", index=False)

accuracy = results["correct"].mean()
print(f"\nAccuracy: {accuracy:.0%} ({results['correct'].sum()} of {len(results)} correct)")
