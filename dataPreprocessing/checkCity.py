from geopy.geocoders import Nominatim

# Function to get city from latitude and longitude
def get_city_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((lat, lon), language="en")
    address = location.address
    return address.split(",")[-3].strip()  # Extracting the city from the address

# Example usage
latitude = 37.7749295
longitude = -122.4194155

city = get_city_from_coordinates(latitude, longitude)
print(f"The city at latitude {latitude}, longitude {longitude} is: {city}")