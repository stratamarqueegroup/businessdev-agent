"""
config.py
Central configuration for the Business Development Agent.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Monday.com
# ============================================================

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY", "")
BOARD_ID = int(os.getenv("BOARD_ID", "18423732757"))

# ============================================================
# Email
# ============================================================

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
REPORT_TO_EMAIL = os.getenv("REPORT_TO_EMAIL", "")

# ============================================================
# OpenStreetMap
# ============================================================

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

USER_AGENT = "StrataMarqueeGroupLeadAgent/2.0"

REQUEST_TIMEOUT = 20

REQUEST_DELAY = 1

RESULTS_PER_QUERY = 10

# ============================================================
# Search Locations
# ============================================================

US_STATES = [
    "Alabama","Alaska","Arizona","Arkansas","California",
    "Colorado","Connecticut","Delaware","Florida","Georgia",
    "Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland",
    "Massachusetts","Michigan","Minnesota","Mississippi","Missouri",
    "Montana","Nebraska","Nevada","New Hampshire","New Jersey",
    "New Mexico","New York","North Carolina","North Dakota","Ohio",
    "Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
    "South Dakota","Tennessee","Texas","Utah","Vermont",
    "Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

US_LOCATIONS = [f"{state}, United States" for state in US_STATES]

EL_SALVADOR_LOCATIONS = [
    "El Salvador"
]

# ============================================================
# Industries
# ============================================================

US_INDUSTRIES = [
    "marketing agency",
    "law firm",
    "dental clinic",
    "roofing contractor",
    "plumbing company",
    "HVAC contractor",
    "construction company",
    "restaurant",
    "hotel",
    "medical clinic",
]

EL_SALVADOR_INDUSTRIES = [
    "hotel",
    "restaurant",
    "retail store",
    "tourism agency",
    "construction company",
    "law firm",
    "dental clinic",
]

# ============================================================
# Lead Scoring
# ============================================================

SCORE_WEIGHTS = {

    "no_website": 30,

    "has_phone": 20,

    "has_full_address": 10,

}