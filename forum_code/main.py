# main.py
from forum_view import ForumView
from user import User

if __name__ == "__main__":
    user = User("danae")
    ForumView(user)
