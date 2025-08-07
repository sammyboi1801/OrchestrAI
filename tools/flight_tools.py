import os
import json
import requests
from dotenv import load_dotenv
from typing import Literal, Optional
from langchain_core.tools import tool

load_dotenv()


@tool
def FLIGHT_INFORMATION(
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
        travel_type: Optional[Literal[1, 2, 3]] = 1

    ) -> dict:
    """
    This tool fetches flight information between two airport locations using the SerpAPI Google Flights engine.

    :param departure_id: IATA airport code of the departure location (e.g., 'BOM' for Mumbai).
    :param arrival_id: IATA airport code of the arrival location (e.g., 'DEL' for Delhi).
    :param outbound_date: Date of departure in YYYY-MM-DD format (e.g., '2025-08-10').
    :param travel_type: Type of trip. Options:
                        1 - Round-trip (default)
                        2 - One-way
                        3 - Multi-city

    :return: A dictionary containing flight search results retrieved from SerpAPI.
    """
    api_key = os.getenv('SERP_API_KEY')

    params = {
        "api_key": api_key,
        "engine": "google_flights",
        "type" : travel_type,
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
    }

    search =requests.get("https://serpapi.com/search", params=params)
    response = search.json()
    # print(json.dumps(response, indent=2))
    return response