# map_controller.py
from db_manager import DBManager
import folium

class MapController:
    def __init__(self):
        self.reports = []

    def update_map(self):
        self.reports = DBManager.get_confirmed_reports()
        if self.reports is None:
            return "db_error"
        if len(self.reports) == 0:
            return "no_reports"

        skipped = 0
        risk_map = folium.Map(location=[37.9838, 23.7275], zoom_start=7)

        for report in self.reports:
            if report.latitude is None or report.longitude is None:
                skipped += 1
                continue
            folium.Marker(
                location=[report.latitude, report.longitude],
                popup=f"Αναφορά #{report.id} - Τύπος: {report.type}",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(risk_map)

        risk_map.save("risk_map.html")
        with open("risk_map.html", "r", encoding="utf-8") as f:
            html = f.read()
        html = html.replace("<head>", '<head>\n<meta http-equiv="refresh" content="30">')
        with open("risk_map.html", "w", encoding="utf-8") as f:
            f.write(html)

        if skipped > 0:
            return "partial_data"
        return "ok"
