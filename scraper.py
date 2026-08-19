"""
scraper.py
Business Development Agent

Fetches real business data from OpenStreetMap's Nominatim API.

Supports:
1. Nationwide/state batch searches
2. Targeted searches by city/state
"""

import requests
import time

from config import (
    NOMINATIM_URL,
    USER_AGENT,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    RESULTS_PER_QUERY,
)


HEADERS = {
    "User-Agent": USER_AGENT
}


# ============================================================
# BASIC NOMINATIM SEARCH
# ============================================================

def search_places(query, location):
    """
    Search OpenStreetMap for businesses matching a query
    inside a location.

    Example:
        query    = "restaurant"
        location = "Florida, United States"
    """

    params = {
        "q": f"{query}, {location}",
        "format": "jsonv2",
        "addressdetails": 1,
        "extratags": 1,
        "limit": RESULTS_PER_QUERY,
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            print(
                f"Warning: request failed for "
                f"'{query}' in '{location}' "
                f"(status {response.status_code})"
            )
            return []

        return response.json()

    except requests.RequestException as error:
        print(
            f"Warning: request error for "
            f"'{query}' in '{location}': {error}"
        )
        return []


# ============================================================
# ADDRESS
# ============================================================

def format_address(address):
    """
    Builds a clean readable address.
    """

    street_parts = [
        address.get("house_number", ""),
        address.get("road", ""),
    ]

    street = " ".join(
        part for part in street_parts if part
    ).strip()

    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or ""
    )

    state = address.get("state", "")
    postcode = address.get("postcode", "")
    country = address.get("country", "")

    pieces = [
        street,
        city,
        state,
        postcode,
        country,
    ]

    return ", ".join(
        piece for piece in pieces if piece
    )


# ============================================================
# PHONE
# ============================================================

def extract_phone(extratags):
    """
    Extract phone numbers from common OSM fields.
    """

    phone = (
        extratags.get("phone")
        or extratags.get("contact:phone")
        or extratags.get("contact:mobile")
        or extratags.get("mobile")
        or ""
    )

    return phone.strip()


# ============================================================
# CONVERT PLACE TO BUSINESS
# ============================================================

def place_to_business(place, industry, location):
    """
    Convert an OpenStreetMap result into a STRATA lead.
    """

    extratags = place.get("extratags") or {}
    address = place.get("address") or {}

    clean_address = format_address(address)

    company = (
        place.get("name")
        or place.get("display_name", "").split(",")[0]
        or "Unknown"
    )

    phone = extract_phone(extratags)

    website = (
        extratags.get("website")
        or extratags.get("contact:website")
        or ""
    )

    return {
        "company": company.strip(),
        "location": location,
        "industry": industry,
        "address": (
            clean_address
            if clean_address
            else place.get("display_name", "")
        ),
        "phone": phone,
        "website": website,
        "has_house_number": bool(
            address.get("house_number")
        ),
    }


# ============================================================
# EXISTING NATIONWIDE SCRAPER
# ============================================================

def scrape_businesses(countries, industries):
    """
    Existing nationwide/state batch scraper.

    This is intentionally kept compatible with your
    current main.py.
    """

    all_businesses = []

    for country in countries:

        for industry in industries:

            print(
                f"Searching: "
                f"{industry} in {country}..."
            )

            places = search_places(
                industry,
                country,
            )

            for place in places:

                business = place_to_business(
                    place,
                    industry,
                    country,
                )

                all_businesses.append(
                    business
                )

            # Nominatim rate limit.
            time.sleep(REQUEST_DELAY)

    return all_businesses


# ============================================================
# TARGETED SCRAPER
# ============================================================

def scrape_targeted(
    location,
    industry,
    limit=10,
    require_website=None,
):
    """
    Targeted search for STRATA commands.

    Example:

        scrape_targeted(
            "Miami, Florida, United States",
            "restaurant",
            10
        )

    require_website:
        None  = don't filter
        True  = only businesses with websites
        False = only businesses without websites
    """

    print("\n" + "=" * 60)
    print("STRATA TARGETED SEARCH")
    print("=" * 60)

    print(f"Location : {location}")
    print(f"Industry : {industry}")
    print(f"Target   : {limit}")

    if require_website is False:
        print("Website  : WITHOUT website")

    elif require_website is True:
        print("Website  : WITH website")

    print("=" * 60)

    businesses = []

    # Ask for more results than needed because
    # filters may remove some.
    request_limit = min(
        max(limit, RESULTS_PER_QUERY),
        50,
    )

    places = search_places(
        industry,
        location,
    )

    print(
        f"OpenStreetMap returned "
        f"{len(places)} results."
    )

    for place in places:

        business = place_to_business(
            place,
            industry,
            location,
        )

        website = business.get(
            "website",
            ""
        ).strip()

        if require_website is False and website:
            continue

        if require_website is True and not website:
            continue

        businesses.append(business)

        if len(businesses) >= limit:
            break

    time.sleep(REQUEST_DELAY)

    print(
        f"Targeted search produced "
        f"{len(businesses)} leads."
    )

    return businesses