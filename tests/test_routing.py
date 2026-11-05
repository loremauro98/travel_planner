from src.services.routing import generate_routes, get_airports_for_region


def test_get_airports_for_region():
    # Test known region
    swiss_airports = get_airports_for_region("Switzerland")
    assert "ZRH" in swiss_airports
    assert "BSL" in swiss_airports
    assert len(swiss_airports) == 4

    # Test case insensitivity
    norway_airports = get_airports_for_region("norway")
    assert "OSL" in norway_airports

    # Test unknown region (fallback to IATA code)
    unknown = get_airports_for_region("JFK")
    assert unknown == ["JFK"]


def test_generate_routes():
    # 4 Swiss airports * 3 Paris airports = 12 routes
    routes = generate_routes("Switzerland", "Paris")
    assert len(routes) == 12
    assert ("ZRH", "CDG") in routes
    assert ("BSL", "ORY") in routes

    # 1 airport to 1 airport
    routes_single = generate_routes("JFK", "LHR")
    assert len(routes_single) == 1
    assert routes_single[0] == ("JFK", "LHR")
