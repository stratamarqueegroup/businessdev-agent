"""
scoring.py
Scores each business as a lead based on signals OpenStreetMap provides:
- no website -> they likely need your services (high opportunity)
- has phone -> easy to contact
- has full address (house number) -> more established, verifiable business
"""

from config import SCORE_WEIGHTS


def score_business(business):
    score = 0
    reasons = []

    if not business.get("website"):
        score += SCORE_WEIGHTS["no_website"]
        reasons.append("No website (opportunity)")

    if business.get("phone"):
        score += SCORE_WEIGHTS["has_phone"]
        reasons.append("Phone number available")

    if business.get("has_house_number"):
        score += SCORE_WEIGHTS["has_full_address"]
        reasons.append("Full street address (established business)")

    business["score"] = score
    business["score_reasons"] = ", ".join(reasons) if reasons else "No strong signals"
    return business


def score_all(businesses):
    scored = [score_business(b) for b in businesses]
    # Highest score first = best leads at the top
    scored.sort(key=lambda b: b["score"], reverse=True)
    return scored