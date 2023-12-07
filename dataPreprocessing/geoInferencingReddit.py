import pandas as pd
from functools import lru_cache
import requests

# Load data
data = pd.read_csv('output_reddit_data_extracted_location_improved-1.csv')

API_KEY = '***'

@lru_cache(maxsize=1024) 
def geo_code(location: str):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        result = data['results'][0]
        geometry = result['geometry']['location']
        return geometry['lat'], geometry['lng']
    else:
        return None


data['lat_lon'] = data['combined_locations'].apply(geo_code)

# Create separate 'lat' and 'lon' columns
data['lat'] = data['lat_lon'].str[0]
data['lon'] = data['lat_lon'].str[1]


# Save the updated DataFrame to a CSV file
data.to_csv('output_file_with_lat_lon-1.csv', index=False)

