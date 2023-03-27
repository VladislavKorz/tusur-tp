from geopy.geocoders import Nominatim
import geopy.distance as dist


def get_city(x,y):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(x)+","+str(y))
    return (location.raw['address']['country'],
            location.raw['address']['state'])


def get_distance(x_A,y_A,x_B,y_B):
    return dist.geodesic((x_A, y_A),(x_B,y_B))
