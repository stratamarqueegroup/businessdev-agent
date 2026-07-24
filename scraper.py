"""
scraper.py
Fetches REAL business data from OpenStreetMap's Nominatim search API.
Free, public, no API key or billing account required.

Usage policy: max 1 request per second, and a descriptive User-Agent
is required. Both are handled below.
"""

import requests
import time
from config import RESULTS_PER_QUERY

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    # Nominatim's usage policy requires a real identifying User-Agent.
    "User-Agent": "BusinessLeadAgent/1.0 (personal project)"
}


def search_places(query, country):
    """
    Search OpenStreetMap for businesses matching a query in a country.
    Returns a list of raw place dicts from the API.
    """
    # Nominatim doesn't allow mixing free-text "q" with a separate
    # structured "country" field - combine them into one query string.
    params = {
        "q": f"{query}, {country}",
        "format": "jsonv2",
        "addressdetails": 1,
        "extratags": 1,
        "limit": RESULTS_PER_QUERY,
    }

    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=15)

    if response.status_code != 200:
        print(f"  Warning: request failed for '{query}' in {country} (status {response.status_code})")
        return []

    return response.json()


def scrape_businesses(countries, industries):
    """
    Main entry point: loops over every country + industry combo,
    fetches real businesses from OpenStreetMap, and returns clean dicts.
    """
    all_businesses = []

    for country in countries:
        for industry in industries:
            print(f"Searching: {industry} in {country}...")
            places = search_places(industry, country)

            for place in places:
                extratags = place.get("extratags") or {}
                address = place.get("address") or {}

                business = {
                    "company": place.get("name") or place.get("display_name", "Unknown").split(",")[0],
                    "country": country,
                    "industry": industry,
                    "address": place.get("display_name", ""),
                    "phone": extratags.get("phone") or extratags.get("contact:phone", ""),
                    "website": extratags.get("website") or extratags.get("contact:website", ""),
                    "has_house_number": bool(address.get("house_number")),
                }
                all_businesses.append(business)

            # Respect Nominatim's rate limit: max 1 request per second.
            time.sleep(1)

    return all_businesses