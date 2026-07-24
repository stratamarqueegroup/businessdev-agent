"""
config.py
Holds all settings for the agent: search terms and scoring rules.
No API key needed - uses OpenStreetMap (free, public, no signup).
"""

# ---- US search settings: all 50 states ----
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
]

# Nominatim needs the full "State, United States" format to search correctly.
US_LOCATIONS = [state + ", United States" for state in US_STATES]

US_INDUSTRIES = [
    "marketing agency",
    "law firm",
    "dental clinic",
]

# ---- El Salvador search settings ----
EL_SALVADOR_LOCATIONS = [
    "El Salvador",
]

EL_SALVADOR_INDUSTRIES = [
    "hotel",
    "restaurant",
    "retail store",
    "local business",
    "tourism agency",
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