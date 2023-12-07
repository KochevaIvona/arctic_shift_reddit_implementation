import pandas as pd
from sklearn.neighbors import BallTree
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# Load data 
df = pd.read_csv('output_file_with_lat_lon-1.csv')

# Drop rows with NaN values in 'lat' or 'lon'
df = df.dropna(subset=['lat', 'lon'])

# Round 'lat' and 'lon' to the first decimal place
df['lat'] = df['lat'].round(1)
df['lon'] = df['lon'].round(1)

# Load the cities lookup data structure
cities = pd.read_csv('cities_coalesced.csv')

# Round 'lat' and 'lon' in cities to the first decimal place
cities['lat'] = cities['lat'].round(1)
cities['lon'] = cities['lon'].round(1)

# Function to calculate haversine distance between two sets of coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Function to find the closest city label based on haversine distance
def find_closest_city(lat, lon):
    distances = [(haversine(lat, lon, city_lat, city_lon), city_label) for city_lat, city_lon, city_label in zip(cities['lat'], cities['lon'], cities['city_label'])]
    closest_city = min(distances, key=lambda x: x[0])
    return closest_city[1]

# Apply the function to find the closest city label for each row in the DataFrame
df['city_label'] = df.apply(lambda row: find_closest_city(row['lat'], row['lon']), axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('output_file_with_city_label-1.csv', index=False)
