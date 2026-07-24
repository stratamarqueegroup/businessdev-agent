"""
config.py
Holds all settings for the agent: search terms and scoring rules.
No API key needed - uses OpenStreetMap (free, public, no signup).
"""

# ---- What to search for ----
# Each combination of country + industry becomes a search query.
COUNTRIES = [
    "United States",
    "United Kingdom",
    "Canada",
]

INDUSTRIES = [
    "marketing agency",
    "law firm",
    "dental clinic",
]

# ---- How many results per search ----
RESULTS_PER_QUERY = 10

# ---- Scoring weights ----
# OpenStreetMap doesn't have ratings/reviews like Google does, so scoring
# is based on what OSM actually provides: contact info completeness.
SCORE_WEIGHTS = {
    "no_website": 30,        # no website listed = strong opportunity
    "has_phone": 20,         # contactable
    "has_full_address": 10,  # complete listing = more established business
}