class DonationPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._total_amount = 1000.0
        return cls._instance

    def has_funds(self, amount: float) -> bool:
        return self._total_amount >= amount
    
    def get_total_amount(self) -> float:
        return self._total_amount

    def deduct_amount(self, amount: float) -> bool:
        if self.has_funds(amount):
            self._total_amount -= amount
            return True
        return False