"""Network boundary for Airbnb searches via pyairbnb.

All live network calls live here. The rest of the code works with plain dictionaries.
"""

import logging
from datetime import date

import pyairbnb

logger = logging.getLogger(__name__)


def search_listings(url, currency="CHF", language="en", timeout=90, max_results=None):
    """Fetch search results for an Airbnb URL, optionally capped to max_results."""
    logger.info("Searching Airbnb in %s: %s", currency, url)
    results = pyairbnb.search_all_from_url(
        url, currency=currency, language=language, timeout=timeout
    )
    if max_results is not None:
        results = results[:max_results]
    logger.info("Retrieved %d listings.", len(results))
    return results


def _as_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def get_listing_details(
    room_id,
    check_in,
    check_out,
    adults=1,
    currency="CHF",
    language="en",
    timeout=90,
):
    """Fetch listing details, returning an empty dict on failure.

    pyairbnb's detail path expects ``datetime.date`` objects even though its
    public signature says ``str``.
    """
    try:
        return pyairbnb.get_details(
            room_id=room_id,
            check_in=_as_date(check_in),
            check_out=_as_date(check_out),
            adults=adults,
            currency=currency,
            language=language,
            timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001 - details enrichment is optional
        logger.warning("Could not enrich listing %s: %s", room_id, exc)
        return {}
