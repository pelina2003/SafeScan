class Authority:
    def __init__(self, name: str, category: str, api_url: str):
        self.name = name
        self.category = category  # π.χ. "φυσική καταστροφή", "τεχνικό πρόβλημα"
        self.api_url = api_url
