class User:
    def __init__(self, id: int, name: str, coordinates, location_enabled=True, push_enabled=True, device_token=None):
        self.id = id
        self.name = name
        self.coordinates = coordinates  # Coordinates object
        self.location_enabled = location_enabled
        self.push_enabled = push_enabled
        self.device_token = device_token
