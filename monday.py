import json
import time
import requests

from config import BOARD_ID, MONDAY_API_KEY

URL = "https://api.monday.com/v2"

HEADERS = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json",
}


def create_item(
    company,
    address="",
    industry="",
    phone="",
    email="",
    website="",
    notes="",
):

    # Store phone in notes because the board uses a Numbers column.
    full_notes = f"""Phone: {phone}

{notes}
"""

    column_values = {
        "text_mm5kts6w": company,
        "text_mm5kgfc6": address,
        "text_mm5kaqkw": industry,

        # Leave Numbers column empty
        "numeric_mm5ktr19": None,

        "text_mm5kkapz": email,
        "text_mm5kt0xy": website,
        "text": full_notes,
    }

    query = """
    mutation ($board: ID!, $name: String!, $values: JSON!) {
      create_item(
        board_id: $board,
        item_name: $name,
        column_values: $values
      ) {
        id
      }
    }
    """

    variables = {
        "board": BOARD_ID,
        "name": company,
        "values": json.dumps(column_values),
    }

    for attempt in range(3):
        try:
            response = requests.post(
                URL,
                headers=HEADERS,
                json={
                    "query": query,
                    "variables": variables,
                },
                timeout=30,
            )

            if response.status_code == 429:
                print("Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
                continue

            response.raise_for_status()

            data = response.json()

            if "errors" in data:
                print(json.dumps(data, indent=2))
                return False

            print(f"✅ Uploaded: {company}")

            return True

        except Exception as e:
            print(f"Error uploading {company}: {e}")
            time.sleep(5)

    return False