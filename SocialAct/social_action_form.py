from datetime import datetime

class SocialActionForm:
    def __init__(self, description: str, date_of_action: datetime, location: str, required_amount: float):
        self._description = description
        self._date_of_action = date_of_action
        self._location = location
        self._required_amount = required_amount

    def is_valid(self) -> bool:
        return (
            bool(self._description.strip())
            and bool(self._location.strip())
            and self._required_amount > 0
            and isinstance(self._date_of_action, datetime)
        )
