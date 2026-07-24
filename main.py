"""
main.py
Runs the full lead-generation agent:
1. Scrape real businesses from Google Places
2. Clean/dedupe them
3. Score them as leads
4. Export the results to CSV
"""

from config import COUNTRIES, INDUSTRIES
from scraper import scrape_businesses
from leads import dedupe_leads, filter_top_leads
from scoring import score_all
from exporters import export_to_csv


def run_agent():
    print("=" * 50)
    print("Business Lead Agent - starting run")
    print("=" * 50)

    # 1. Get real businesses
    businesses = scrape_businesses(COUNTRIES, INDUSTRIES)
    print(f"\nFound {len(businesses)} raw results.")

    # 2. Remove duplicates
    businesses = dedupe_leads(businesses)
    print(f"{len(businesses)} unique businesses after deduping.")

    # 3. Score every lead
    businesses = score_all(businesses)

    # 4. Keep only decent leads (score 10+), tweak as you like
    top_leads = filter_top_leads(businesses, min_score=10)
    print(f"{len(top_leads)} businesses scored 10+.")

    # 5. Show top 5 in the terminal
    print("\nTop leads:")
    for b in top_leads[:5]:
        print(f"  {b['company']} ({b['country']}) - score {b['score']} - {b['score_reasons']}")

    # 6. Export to CSV
    export_to_csv(top_leads)

    print("\n✅ Agent run complete.")


if __name__ == "__main__":
    run_agent()