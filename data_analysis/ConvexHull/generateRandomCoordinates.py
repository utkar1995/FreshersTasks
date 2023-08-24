import random


# Function to generate random latitude and longitude within Andheri area
def generate_random_coordinates():
    # Latitude and Longitude ranges for Andheri, Mumbai
    min_latitude, max_latitude = 19.1080, 19.1355
    min_longitude, max_longitude = 72.8230, 72.8520

    # Generate random coordinates
    latitude = round(random.uniform(min_latitude, max_latitude), 6)
    longitude = round(random.uniform(min_longitude, max_longitude), 6)

    return latitude, longitude


# Generate 20 random coordinates
random_coordinates = [generate_random_coordinates() for _ in range(20)]

print("Random Coordinates:")
for i, (lat, lon) in enumerate(random_coordinates, start=1):
    print(f"{i}. Latitude: {lat}, Longitude: {lon}")
