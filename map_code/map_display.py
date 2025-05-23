import folium
from db_manager import get_confirmed_reports

def create_risk_map():
    try:
        reports = get_confirmed_reports()
    except Exception as e:
        print(f"⚠️ DB error (try block): {e}")
        return "db_error"

    if reports is None:
        print("⚠️ DB error: Η reports είναι None.")
        return "db_error"

    if len(reports) == 0:
        print("ℹ️ Δεν υπάρχουν επιβεβαιωμένες αναφορές.")
        empty_map = folium.Map(location=[37.9838, 23.7275], zoom_start=7)
        folium.Marker(
            location=[37.9838, 23.7275],
            popup="Δεν υπάρχουν επιβεβαιωμένοι κίνδυνοι προς το παρόν.",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(empty_map)
        empty_map.save("risk_map.html")
        return "empty"

    # Κανονικός χάρτης
    risk_map = folium.Map(location=[37.9838, 23.7275], zoom_start=7)

    skipped = 0
    for report in reports:
        report_id, r_type, lat, lon = report
        if lat is None or lon is None:
            skipped += 1
            continue
        folium.Marker(
            location=[lat, lon],
            popup=f"Αναφορά #{report_id} - Τύπος: {r_type}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(risk_map)

    risk_map.save("risk_map.html")

    # Προσθήκη auto-refresh
    with open("risk_map.html", "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("<head>", '<head>\n<meta http-equiv="refresh" content="30">')
    with open("risk_map.html", "w", encoding="utf-8") as f:
        f.write(html)

    if skipped > 0:
        print(f"⚠️ Παραλείφθηκαν {skipped} αναφορές με άκυρα γεωγραφικά δεδομένα.")

    return "ok"

