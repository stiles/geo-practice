import os
import requests
from rich import print

# Fetch the API key from the environment
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Ensure the key is available
if not google_maps_api_key:
    raise ValueError("Google Maps API Key not found in the environment!")

# Headers for the request
headers = {
    'sec-ch-ua-platform': '"macOS"',
    'X-User-Agent': 'grpc-web-javascript/0.1',
    'Referer': 'https://www.geoguessr.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'X-Goog-Maps-Channel-Id': '',
    'sec-ch-ua-mobile': '?0',
    'X-Goog-Api-Key': google_maps_api_key,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Content-Type': 'application/json+protobuf',
}

# Define the ID
location_id = "taBqqmQBmTsRpSnuJj2HHQ"

# Request payload
data = f'[["apiv3",null,null,null,"US",null,null,null,null,null,[[0]]],["en"],[[[2,"{location_id}"]]],[[1,2,3,4,8,6]]]'

# Make the request
response = requests.post(
    'https://maps.googleapis.com/$rpc/google.internal.maps.mapsjs.v1.MapsJsInternalService/GetMetadata',
    headers=headers,
    data=data,
)

# Parse the response JSON
response_json = response.json()

# Extract location
try:
    location = response_json[1][0][3][2][1][0]
    coordinates = (
        response_json[1][0][5][0][1][0][2],
        response_json[1][0][5][0][1][0][3],
    )
    print(f"Location: {location}")
    print(f"Coordinates: {coordinates}")
except (IndexError, TypeError) as e:
    print("Error extracting data:", e)
