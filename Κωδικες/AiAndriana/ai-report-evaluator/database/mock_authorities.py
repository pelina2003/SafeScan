from models.authority import Authority

def get_authorities():
    return [
        Authority("Πυροσβεστική", "φυσική καταστροφή", "https://api.fire-service.gr/report"),
        Authority("ΕΚΑΒ", "κοινωνικός κίνδυνος", "https://api.ekab.gr/report"),
        Authority("ΔΕΔΔΗΕ", "τεχνικό πρόβλημα", "https://api.deddie.gr/report"),
        Authority("112", "default", "https://api.112.gov.gr/report")
    ]
