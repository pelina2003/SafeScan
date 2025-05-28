from models.user import User
from models.report import Coordinates

def get_active_users():
    return [
        User(1, "Γιώργος", Coordinates(37.9845, 23.7280), location_enabled=True, push_enabled=True, device_token="token1"),
        User(2, "Μαρία", Coordinates(38.0, 23.73), location_enabled=False, push_enabled=True, device_token="token2"),
        User(3, "Άννα", Coordinates(37.9830, 23.7260), location_enabled=True, push_enabled=False, device_token="token3"),
        User(4, "Κώστας", Coordinates(38.2466, 21.7346), location_enabled=True, push_enabled=True, device_token="token4")
    ]
