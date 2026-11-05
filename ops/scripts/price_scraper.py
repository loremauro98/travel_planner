"""
price_scraper.py - Data ingestion pipeline.

Glues together the routing engine, flight API, database manager, and analytics engine.
This module orchestrates /src engines; it does not own the math.
"""

import logging
import sys
import time
from pathlib import Path

# Ensure src modules can be imported when running ops/scripts
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.database.db_manager import (
    get_historical_prices,
    insert_flight_prices,
    setup_database,
)
from src.services.analytics import calculate_moving_average, detect_price_dips
from src.services.flight_api import fetch_flights
from src.services.routing import generate_routes

logger = logging.getLogger(__name__)


def _filter_flights(flights, field, limit, route_origin, route_dest, label=None):
    """Apply one filter and log exactly how many flights that criterion dropped."""
    before = len(flights)
    kept = [flight for flight in flights if flight.get(field, 0) <= limit]
    dropped = before - len(kept)
    logger.info(
        "Filter %s<=%s dropped %d of %d flights for %s->%s",
        label or field,
        limit,
        dropped,
        before,
        route_origin,
        route_dest,
    )
    return kept


def run_pipeline(
    origin,
    destination,
    date,
    dip_threshold=0.10,
    ma_window=3,
    max_stops=None,
    max_travel_time=None,
    api_pause_seconds=4.0,
):
    """
    Runs the full ingestion and analysis pipeline for a given origin/destination region.
    Filters flights based on max_stops and max_travel_time.
    Returns a list of alerts for detected price dips.

    All analytical and operational parameters are explicit: dip_threshold, ma_window,
    max_stops, max_travel_time, and api_pause_seconds.
    """
    alerts = []

    # 1. Expand regions to specific airport routes
    routes = generate_routes(origin, destination)
    logger.info("Expanded %s -> %s into %d routes.", origin, destination, len(routes))

    # Ensure database is set up
    setup_database()

    for route_origin, route_dest in routes:
        # 2. Fetch current prices
        logger.info("Fetching %s -> %s...", route_origin, route_dest)
        flights = fetch_flights(route_origin, route_dest, date)

        # Respect rate limits for free APIs
        time.sleep(api_pause_seconds)

        # Filter flights by constraints before inserting/analyzing.
        # Each criterion logs its own drop count (transparent-data-masker).
        if max_stops is not None:
            flights = _filter_flights(
                flights, "stops", max_stops, route_origin, route_dest, label="max_stops"
            )
        if max_travel_time is not None:
            flights = _filter_flights(
                flights,
                "travel_time_minutes",
                max_travel_time,
                route_origin,
                route_dest,
                label="max_travel_time",
            )

        if not flights:
            logger.info(
                "No flights after filters for %s->%s.", route_origin, route_dest
            )
            continue

        # 3. Insert into database
        insert_flight_prices(flights)

        # 4. Analyze historical data for dips
        hist_df = get_historical_prices(route_origin, route_dest, date)

        if len(hist_df) >= ma_window:
            # We have enough data for a moving average
            df_with_ma = calculate_moving_average(hist_df, window_size=ma_window)
            ma_col = f"ma_{ma_window}"

            dips_df = detect_price_dips(
                df_with_ma, ma_col, threshold_percentage=dip_threshold
            )

            # Check if the most recent scraped flight is a dip
            if not dips_df.empty:
                latest_dip = dips_df.iloc[-1]
                # If the dip happened on our current run
                if latest_dip["price"] == flights[0]["price"] or (
                    len(flights) > 1 and latest_dip["price"] == flights[1]["price"]
                ):
                    alert = (
                        f"🚨 PRICE DIP ALERT: {route_origin}->{route_dest} on {date}. "
                        f"Price is {latest_dip['price']} (MA: {latest_dip[ma_col]:.2f})"
                    )
                    alerts.append(alert)

    return alerts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger.info("Running Data Ingestion Pipeline...")
    alerts = run_pipeline("Switzerland", "Norway", "2026-12-15")
    for alert in alerts:
        logger.info(alert)
    logger.info("Pipeline finished.")
