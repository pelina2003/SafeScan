from enum import Enum
from datetime import datetime
from typing import List, Optional

# Enum για το status της δωρεάς
class Status(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"

# Κλάση User
class User:
    def __init__(self, userId: int, username: str, email: str):
        self.userId = userId
        self.username = username
        self.email = email
        self.donations: List[Donation] = []

    def getUserName(self) -> str:
        return self.username

    def getEmail(self) -> str:
        return self.email

    def addDonation(self, donation: 'Donation'):
        self.donations.append(donation)

    def getDonations(self) -> List['Donation']:
        return self.donations

# Κλάση PaymentSystem
class PaymentSystem:
    def __init__(self, name: str, maxAmount: float):
        self.name = name
        self.maxAmount = maxAmount

    def validateAmount(self, amount: float) -> bool:
        return 0 < amount <= self.maxAmount

    def getName(self) -> str:
        return self.name

# Κλάση SocialAction
class SocialAction:
    def __init__(self, actionId: int, title: str, category: str, location: str):
        self.actionId = actionId
        self.title = title
        self.category = category
        self.location = location

    def getTitle(self) -> str:
        return self.title

    def getCategory(self) -> str:
        return self.category

    def getLocation(self) -> str:
        return self.location

# Κλάση EnvironmentalOrganization
class EnvironmentalOrganization:
    def __init__(self, orgId: int, name: str, category: str):
        self.orgId = orgId
        self.name = name
        self.category = category

    def getName(self) -> str:
        return self.name

    def getCategory(self) -> str:
        return self.category

# Κλάση Donation
class Donation:
    def __init__(self, donationId: int, amount: float, date: datetime,
                 paymentMethod: str, user: User,
                 socialAction: Optional[SocialAction] = None,
                 environmentalOrganization: Optional[EnvironmentalOrganization] = None):
        self.donationId = donationId
        self.amount = amount
        self.date = date
        self.paymentMethod = paymentMethod
        self.status = Status.PENDING
        self.user = user
        self.socialAction = socialAction
        self.environmentalOrganization = environmentalOrganization
        user.addDonation(self)

    def confirmDonation(self):
        self.status = Status.CONFIRMED

    def failDonation(self):
        self.status = Status.FAILED

    def getStatus(self) -> Status:
        return self.status

