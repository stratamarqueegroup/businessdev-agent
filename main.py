"""
main.py
Business Development Agent v2
"""

import json
from pathlib import Path


from config import (
    US_LOCATIONS,
    US_INDUSTRIES,
    EL_SALVADOR_LOCATIONS,
    EL_SALVADOR_INDUSTRIES,
)

from scraper import scrape_businesses
from leads import dedupe_leads
from scoring import score_all
from exporters import export_to_csv
from emailer import send_report_email

MAX_LEADS = 528
SENT_LEADS_FILE = Path("outputs/sent_leads.json")


def lead_identity(lead):
    """Build a stable key to prevent emailing the same business again."""
    company = " ".join(lead.get("company", "").lower().split())
    address = " ".join(lead.get("address", "").lower().split())
    return f"{company}|{address}"


def load_sent_leads():
    """Load identities of leads included in successfully emailed reports."""
    try:
        data = json.loads(SENT_LEADS_FILE.read_text())
        return set(data) if isinstance(data, list) else set()
    except FileNotFoundError:
        return set()
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(
            f"Cannot safely read sent-leads history at {SENT_LEADS_FILE}: {exc}"
        ) from exc


def save_sent_leads(sent):
    SENT_LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
    temp_file = SENT_LEADS_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(sorted(sent), indent=2))
    temp_file.replace(SENT_LEADS_FILE)


def run_agent():

    print("=" * 60)
    print("🚀 Strata Marquee Group Business Development Agent")
    print("=" * 60)

    print("\nSearching United States...")
    us_businesses = scrape_businesses(
        US_LOCATIONS,
        US_INDUSTRIES,
    )

    print("\nSearching El Salvador...")
    es_businesses = scrape_businesses(
        EL_SALVADOR_LOCATIONS,
        EL_SALVADOR_INDUSTRIES,
    )

    businesses = us_businesses + es_businesses

    print(f"\nFound {len(businesses)} businesses.")

    businesses = dedupe_leads(businesses)
    print(f"{len(businesses)} unique businesses in this run.")

    sent = load_sent_leads()
    new_businesses = [
        lead for lead in businesses
        if lead_identity(lead) not in sent
    ]
    print(f"{len(new_businesses)} businesses not previously emailed.")
    print(f"Skipping {len(businesses) - len(new_businesses)} previously emailed businesses.")

    businesses = score_all(new_businesses)
    top_leads = businesses[:MAX_LEADS]

    if not top_leads:
        print("\nNo new leads to email. Try expanding locations or industries.")
        return

    print(f"\nPreparing email report with {len(top_leads)} new leads...")

    csv_path = export_to_csv(top_leads)

    email_sent = send_report_email(csv_path, len(top_leads))

    if email_sent:
        sent.update(lead_identity(lead) for lead in top_leads)
        save_sent_leads(sent)
        print(f"Saved {len(top_leads)} emailed leads to {SENT_LEADS_FILE}.")
    else:
        print("Email failed; leads were NOT added to sent history and can be retried.")

    print("\n✅ Agent run complete.")


if __name__ == "__main__":
    run_agent()