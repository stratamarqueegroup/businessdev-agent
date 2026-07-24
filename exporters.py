"""
exporters.py
Saves the final lead list to a CSV file you can open in Excel/Google Sheets.
"""

import csv
import os
from datetime import datetime


def export_to_csv(businesses, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filepath = os.path.join(output_dir, f"leads_{timestamp}.csv")

    fieldnames = [
        "company", "country", "industry", "address",
        "phone", "website", "score", "score_reasons",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in businesses:
            writer.writerow({k: b.get(k, "") for k in fieldnames})

    print(f"✅ Exported {len(businesses)} leads to {filepath}")
    return filepath