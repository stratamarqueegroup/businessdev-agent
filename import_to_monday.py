import csv
from monday import create_item

CSV_FILE = "output/leads_2026-07-24_20-15.csv"

with open(CSV_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for i, lead in enumerate(reader):

        if i >= 10:   # Change to 500 later (or remove this line)
            break

        notes = f"""
Country: {lead['country']}
Industry: {lead['industry']}
Address: {lead['address']}
Phone: {lead['phone']}
Website: {lead['website']}
Score: {lead['score']}

Reasons:
{lead['score_reasons']}
"""

        create_item(
            company=lead["company"],
            notes=notes
        )

print("Finished!")