"""
contact_finder.py

Find contact information from business websites:
- phone numbers
- emails
"""

import re
import requests
from bs4 import BeautifulSoup


def extract_contacts(url):
    """
    Visit website and extract emails and phone numbers.
    """

    contacts = {
        "email": "",
        "phone": ""
    }

    if not url:
        return contacts

    try:
        # Make website request
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        html = response.text

        # Extract emails
        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            html
        )

        if emails:
            contacts["email"] = emails[0]


        # Extract phone numbers
        phones = re.findall(
            r"\+?\d[\d\s\-\(\)]{7,}\d",
            html
        )

        if phones:
            contacts["phone"] = phones[0]


    except Exception as e:
        print(
            f"Could not scan {url}: {e}"
        )


    return contacts



def enrich_leads(leads):
    """
    Add phone and email information to every lead.
    """

    print("\nFinding contact information...")

    for lead in leads:

        website = lead.get(
            "website",
            ""
        )

        contacts = extract_contacts(
            website
        )

        lead["email"] = contacts["email"]
        lead["phone"] = contacts["phone"]

        print(
            f"{lead.get('company')} -> "
            f"{lead['phone']} "
            f"{lead['email']}"
        )

    return leads