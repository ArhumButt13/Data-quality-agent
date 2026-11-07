import os
import pandas as pd
from checks import load_suppliers, missing_fields, is_valid_vat, is_valid_email, find_duplicates

df = load_suppliers()
issues = []

for _, row in df.iterrows():
    supplier_id = row["supplier_id"]

    for field in missing_fields(row):
        issues.append({"supplier_id": supplier_id, "issue": f"missing {field}"})

    if row["vat_id"] and not is_valid_vat(row["vat_id"]):
        issues.append({"supplier_id": supplier_id, "issue": "invalid VAT format"})

    if row["email"] and not is_valid_email(row["email"]):
        issues.append({"supplier_id": supplier_id, "issue": "invalid email"})

    duplicates = find_duplicates(df, supplier_id)
    if duplicates:
        issues.append({"supplier_id": supplier_id, "issue": f"possible duplicate of {', '.join(duplicates)}"})

os.makedirs("output", exist_ok=True)
report = pd.DataFrame(issues)
report.to_csv("output/issues_report.csv", index=False)

print(report)
print(f"\n{report['supplier_id'].nunique()} of {len(df)} suppliers have issues.")
