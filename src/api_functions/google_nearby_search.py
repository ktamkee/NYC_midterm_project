import requests
import os
import pandas as pd
import time

## load Google Authentication for places
google_places_key = os.environ['GOOGLE_PLACES_API_KEY']

## Define query function
def gPlaceSearch(latitude, longitude, radius, query):
    """
    Takes lat & long with coma, a query and a radius, returns a list of up to three response objects.

    latitude (str): latitude
    longitude (str): longitude
    radius (int): value in meters to confine search
    query (str): string query to specify search
    """

    ## set paramaters
    google_places_key = os.environ["GOOGLE_PLACES_API_KEY"]

    google_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    gplace_params = {
        "key": google_places_key,
        "location": latitude+','+longitude,
        "radius": radius,
        "keyword": query
    }

    ## Get initial response
    response_list = []
    response = (requests.get(google_url, params=gplace_params))
    response_list.append(response.json())

    ## Check for next page to be added to response list
    try:
        next_page_token = response.json()['next_page_token']
        time.sleep(2)
        # while len(next_page_token) > 10:
        while next_page_token:

            ## New request to next page with token
            next_page_params = {
                "pagetoken": next_page_token,
                "key": google_places_key
            }
            next_response = requests.get(google_url, params=next_page_params)
            response_list.append(next_response.json())

            time.sleep(2)

            ## Assign New Token, if doesn't exist, return
            try:
                next_page_token = next_response.json()['next_page_token']
            except KeyError:
                return response_list
    except KeyError:
        pass
    return response_list