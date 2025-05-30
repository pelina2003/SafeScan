# models/ai_models.py

def estimate_risk(report, text_result=None):
    description = report.text.lower()
    location_name = report.location_name.lower()
    coordinates = report.coordinates  # αντικείμενο Coordinates ή None

    base_risk = 40  # default base risk
    category = "άλλο"

    # Βασισμένο σε λέξεις-κλειδιά της περιγραφής
    if any(word in description for word in ["φωτιά", "πυρκαγιά", "καπνός"]):
        base_risk = 70
        category = "φυσική καταστροφή"
    elif any(word in description for word in ["πλημμύρα", "νερά", "βροχή"]):
        base_risk = 60
        category = "φυσική καταστροφή"
    elif any(word in description for word in ["τραυματισμός", "επίθεση", "καυγάς"]):
        base_risk = 65
        category = "κοινωνικός κίνδυνος"
    elif any(word in description for word in ["καλώδιο", "ρεύμα", "διαρροή"]):
        base_risk = 55
        category = "τεχνικό πρόβλημα"

    # Προσαρμογή ανάλογα με την AI σιγουριά (από text_result)
    if text_result: 
        confidence = text_result.confidence
        adjusted_risk = int(base_risk * (0.8 + 0.4 * confidence))  # από 80% έως 120%
    else:
        adjusted_risk = base_risk

    # BONUS: αν είσαι σε "ειδική" τοποθεσία (π.χ. δάσος), αύξησε τον κίνδυνο λίγο
    if coordinates:
        if coordinates.latitude > 37.9 and coordinates.latitude < 38.1:
            adjusted_risk += 5  # προαιρετικό boost για test
        adjusted_risk = min(adjusted_risk, 100)

    print(f"📊 Υπολογισμός κινδύνου: {adjusted_risk}% | Κατηγορία: {category}")
    return adjusted_risk, category
