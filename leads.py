"""
leads.py
Cleans up the lead list: removes duplicates and empty entries.
"""


def dedupe_leads(businesses):
    seen = set()
    unique = []
    for b in businesses:
        key = (b.get("company", "").strip().lower(), b.get("address", "").strip().lower())
        if key not in seen and b.get("company"):
            seen.add(key)
            unique.append(b)
    return unique


def filter_top_leads(businesses, min_score=0):
    return [b for b in businesses if b.get("score", 0) >= min_score]