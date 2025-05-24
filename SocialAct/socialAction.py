from typing import List
from user import User 
from report import Report
from social_action_form import SocialActionForm
from donation import DonationPool

class SocialAction:
    MAX_ACTIVE_ACTIONS = 5
    active_actions: List['SocialAction'] = []

    def __init__(self, user: User, activity: Report, form: SocialActionForm):
        self._user = user
        self._activity = activity
        self._description = form._description
        self._date_of_action = form._date_of_action
        self._location = form._location
        self._required_amount = form._required_amount
        self._is_active = True

    @classmethod
    def can_create_action(cls) -> bool:
        return len([a for a in cls.active_actions if a._is_active]) < cls.MAX_ACTIVE_ACTIONS

    @classmethod
    def active_count(cls) -> int:
        return len([a for a in cls.active_actions if a._is_active])

    @classmethod
    def create_action(
            cls,
            user: User,
            activity: Report,
            form: SocialActionForm
        ) -> 'SocialAction':
        if not cls.can_create_action():
            raise Exception("Υπερβήθηκε το μέγιστο όριο ενεργών δράσεων.")
        if not form.is_valid():
            raise Exception("Incorrect details in form.")
        pool = DonationPool()
        if not pool.has_funds(form._required_amount):
            raise Exception("Ανεπαρκή donations για τη δράση.")
        action = SocialAction(user, activity, form)
        pool.deduct_amount(form._required_amount)
        cls.active_actions.append(action)
        return action
