"""
flight_api.py - Interface for fetching flight data.

Connects to SerpApi to scrape live Google Flights data.
"""

import logging
import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def fetch_flights(origin, destination, departure_date, return_date=None):
    """
    Fetches real flight data from Google Flights via SerpApi.
    """
    if not SERPAPI_KEY or SERPAPI_KEY == "your_serpapi_key_here":
        logger.warning("SERPAPI_KEY not set. Cannot fetch %s->%s.", origin, destination)
        return []

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": departure_date,
        "currency": "USD",
        "hl": "en",
        "api_key": SERPAPI_KEY,
        "type": "1" if return_date else "2",
    }

    if return_date:
        params["return_date"] = return_date

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.warning(
            "Error fetching data from SerpApi for %s->%s: %s", origin, destination, e
        )
        return []

    flights_list = []

    # SerpApi returns 'best_flights' and 'other_flights' arrays
    flight_categories = data.get("best_flights", []) + data.get("other_flights", [])

    for f in flight_categories:
        try:
            price = f.get("price")
            if not price:
                continue

            # Parse layovers and duration
            legs = f.get("flights", [])
            stops = max(0, len(legs) - 1)
            travel_time = f.get("total_duration", 0)
            provider = legs[0].get("airline", "Unknown") if legs else "Unknown"

            flights_list.append(
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "price": float(price),
                    "currency": "USD",
                    "stops": stops,
                    "travel_time_minutes": travel_time,
                    "provider": provider,
                }
            )
        except (AttributeError, KeyError, TypeError, ValueError) as e:
            logger.warning(
                "Skipping malformed flight entry for %s->%s: %s", origin, destination, e
            )
            continue

    return flights_list


if __name__ == "__main__":
    print("Testing SerpApi integration...")
    results = fetch_flights("BSL", "OSL", "2026-12-15")
    print(f"Found {len(results)} flights!")
    for r in results[:3]:
        print(
            f"{r['provider']}: {r['origin']} -> {r['destination']} | {r['stops']} stops | {r['travel_time_minutes']} mins | {r['price']} {r['currency']}"
        )
