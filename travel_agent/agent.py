"""
Travel agent with Custom Function Tools
Demonstrates multiple custom tools working together.

Reference: https://google.github.io/adk-docs/tools-custom/function-tools
"""

from google.adk.agents.llm_agent import Agent

# Tool 1: Search flights
def search_flights(destination: str, departure_date: str) -> dict:
    """Searches for available flights to a destination on a specific date.

    Use this tool when a customer wants to know flight options.

    Args:
        destination (str): The destination city (e.g., "Paris", "Tokyo")
        departure_date (str): Departure date in YYYY-MM-DD format

    Returns:
        dict: Flight search results.
        On success: {'status': 'success', 'flights': [...], 'count': N}
        On error: {'status': 'error', 'error_message': 'explanation'}
    """
    # Simulated flight data
    available_flights = {
        "paris": [
            {"flight_number": "AF123", "price_usd": 450, "duration_hours": 8},
            {"flight_number": "BA456", "price_usd": 480, "duration_hours": 7.5}
        ],
        "tokyo": [
            {"flight_number": "JL789", "price_usd": 850, "duration_hours": 13},
            {"flight_number": "NH101", "price_usd": 820, "duration_hours": 12.5}
        ]
    }

    dest_key = destination.lower()
    if dest_key not in available_flights:
        return {
            "status": "error",
            "error_message": f"No flights found to '{destination}'. Try Paris or Tokyo."}

    return {
        "status": "success",
        "destination": destination,
        "departure_date": departure_date,
        "flights": available_flights[dest_key],
        "count": len(available_flights[dest_key])
    }

# Tool 2: Search hotels
def search_hotels(city: str, check_in_date: str) -> dict:
    """Searches for available hotels in a city for a specific check-in date.

    Use this tool when a customer needs accommodation.

    Args:
        city (str): The city name (e.g., "Paris", "Tokyo").
        check_in_date (str): Check-in date in YYYY-MM-DD format.

    Returns:
        dict: Hotel search results.
            On success: {'status': 'success', 'hotels': [...], 'count': N}
            On error: {'status': 'error', 'error_message': 'explanation'}
    """

    # Simulated hotel data
    available_hotels = {
        "paris": [
            {"name": "Hotel Eiffel", "price_per_night_usd": 200, "rating": 4.5},
            {"hotel_name": "Eiffel Stay", "price_usd": 180, "rating": 4.0}
        ],
        "tokyo": [
            {"hotel_name": "Tokyo Inn", "price_usd": 150, "rating": 4.2},
            {"hotel_name": "Shinjuku Hotel", "price_usd": 170, "rating": 4.3}
        ]
    }

    dest_key = destination.lower()
    if dest_key not in available_hotels:
        return {
            "status": "error",
            "error_message": f"No hotels found to '{destination}'. Try Paris or Tokyo."}

    return {
        "status": "success",
        "destination": destination,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "hotels": available_hotels[dest_key],
        "count": len(available_hotels[dest_key])
    }

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
