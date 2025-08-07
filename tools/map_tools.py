import googlemaps
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from typing import Literal, Optional

load_dotenv()
maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

utube_vid = "https://www.youtube.com/watch?v=6xcbDEU_tWk&ab_channel=ProgrammingKnowledge"

gmaps = googlemaps.Client(key=maps_api_key)

@tool
def GEOCODE_ADDRESS(address: str) -> list:
    """
    This tool can be used to get the latitude and longitude of any address.
    :param address: an address to geocode (getting latitude and longitude)
    """
    geocode_result = gmaps.geocode(address)
    return geocode_result

@tool
def REVERSE_GEOCODE(lat: float, lng: float) -> list:
    """
    This tool can be used to get the actual address based on the provided latitude and longitude.
    :param lat: latitude of the address as a float variable
    :param lng: longitude of the address as a float variable
    """
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    return reverse_geocode_result

@tool
def CALCULATE_DISTANCE(
        origin: str,
        destination: str,
        mode: Literal["driving", "walking", "bicycling", "transit" ] = "driving",
        transit_mode: Optional[Literal["bus", "subway", "train", "tram", "rail"]] = None) -> tuple:
    """
    This tool can be used to calculate distance between two addresses.
    :param origin: place of departure
    :param destination: place of arrival
    :param mode: a string specifying mode of transportation. Options: [driving, walking, bicycling, transit for public transport]. Defaults to 'driving'.
    :param transit_mode: Specifies one or more preferred modes of transit. This parameter may only be specified for transit directions. Options: [bus, subway, train, tram, rail]
    Returns (distance in km, duration in hours/mins)
    """
    distance_matrix = gmaps.distance_matrix(origin, destination, mode=mode, transit_mode=transit_mode)
    distance = distance_matrix['rows'][0]['elements'][0]['distance']['text']
    duration = distance_matrix['rows'][0]['elements'][0]['duration']['text']
    return (distance, duration)

@tool
def GET_DIRECTIONS(
        origin: str,
        destination: str,
        mode: Literal["driving", "walking", "bicycling", "transit"] = "driving",
        transit_mode: Optional[Literal["bus", "subway", "train", "tram", "rail"]] = None) -> list:
    """
    This tool can be used to get directions between two addresses.
    :param origin: place of departure
    :param destination: place of arrival
    :param mode: a string specifying mode of transportation. Options: [driving, walking, bicycling, transit for public transport]. Defaults to 'driving'.
    :param transit_mode: Specifies one or more preferred modes of transit. This parameter may only be specified for transit directions. Options: [bus, subway, train, tram, rail]
    Returns google maps response for directions
    """

    kwargs = {
        "origin": origin,
        "destination": destination,
        "mode": mode
    }

    if mode == "transit" and transit_mode is not None:
        kwargs["transit_mode"] = transit_mode

    directions = gmaps.directions(**kwargs)
    return directions
    # steps = directions[0]['legs'][0]['steps']
    # for step in steps:
    #     print(step['html_instructions'])

@tool
def FIND_NEARBY_PLACES(location: str,
                       radius: int,
                       place_type: str) -> list:
    """
    Finds and prints the names of nearby places of a specified type using Google Maps Places API.
    :param location (str): The latitude/longitude coordinates of the center point (e.g., "19.0760,72.8777").
    :param radius (int): The search radius in meters (maximum is 50,000 meters).
    :param place_type (str): restaurant, hotel, etc.
    Returns:
        list of tuples: Each tuple contains:
            - name (str): The name of the place
            - business_status (str): The operational status of the place (e.g., "OPERATIONAL")
            - location (dict): Dictionary with latitude and longitude of the place
            - vicinity (str): A human-readable address of the place
    """
    places = gmaps.places_nearby(location, radius, type=place_type)
    places_list = []
    for place in places['results']:
        places_list.append((place['name'], place['business_status'], place['geometry']['location'], place['vicinity']))

    return places_list

# print(find_nearby_places((19.1536223,72.8859818), 1000,'restaurant'))
# print(get_directions("Churchgate Station, Mumbai", "Andheri Station, Mumbai", mode = "transit"))

# directions = gmaps.directions("Bombay Scottish School", "Royal Palms, mumbai", mode="driving")
# print(directions)