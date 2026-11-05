"""
routing.py - Multi-airport routing engine.
Expands geographical regions (e.g., countries or cities) into specific airport codes,
and generates all possible flight routes between two regions.
"""

# Single authority for regional airport expansion. Add new regions here only.
REGION_AIRPORTS = {
    "Switzerland": ["ZRH", "BSL", "GVA", "BRN"],
    "Norway": ["OSL", "BGO", "SVG", "TOS"],
    "Italy": ["FCO", "MXP", "VCE", "NAP"],
    "London": ["LHR", "LGW", "STN", "LTN", "LCY"],
    "Paris": ["CDG", "ORY", "BVA"],
}


def get_airports_for_region(region_name):
    """
    Returns a list of airport codes for a given region.
    If the region is not found, assumes the input is already an airport code.
    """
    # Case insensitive lookup
    for key, airports in REGION_AIRPORTS.items():
        if key.lower() == region_name.lower():
            return airports

    # Default to assuming it's already an IATA code if not in mapping
    return [region_name.upper()]


def generate_routes(origin_region, dest_region):
    """
    Generates all possible route pairs between an origin region and a destination region.
    Returns a list of tuples: (origin_airport, destination_airport)
    """
    origins = get_airports_for_region(origin_region)
    destinations = get_airports_for_region(dest_region)

    routes = []
    for o in origins:
        for d in destinations:
            routes.append((o, d))

    return routes
