# main.py
from map_view import MapView
from user import User

if __name__ == "__main__":
    user = User("guest")
    MapView(user)
