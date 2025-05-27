from math import radians, cos, sin, sqrt, atan2

def calculate_distance(coord1, coord2):
    # Υπολογισμός απόστασης Haversine (σε km)
    R = 6371.0
    lat1, lon1 = radians(coord1.latitude), radians(coord1.longitude)
    lat2, lon2 = radians(coord2.latitude), radians(coord2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c  # σε km
