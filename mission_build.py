from dataclasses import dataclass


@dataclass
class Report:
    """Repräsentiert einen Bericht"""
    timestamp: str
    source: str
    content: str
    report_type: str  # "normal", "urgent", "witnessed"


def _load_sample_reports(self):
     """Lädt Beispiel-Berichte"""
     sample_reports = [
        Report("14:23", "DIREKTE BEOBACHTUNG", 
                "Ich sehe durch mein Fernglas: Regiment 226 formiert sich neu hinter dem Hügel. Die Männer wirken erschöpft, aber diszipliniert. Oberst Mueller scheint die Lage im Griff zu haben.",
                "witnessed"),
        Report("14:15", "EILBERICHT VON MAJOR WEBER",
                "General! Der linke Flügel ist unter schwerem Beschuss. Regiment 187 hat bereits 30% Verluste. Hauptmann Fischer bittet um sofortige Verstärkung oder Rückzugsbefehl!",
                "urgent"),
        Report("14:10", "MELDUNG VON LEUTNANT BRAUN",
                "Regiment 142 hat Position Delta erreicht. Kein Feindkontakt. Warten auf weitere Befehle. Munition bei 80%.",
                "normal"),
        Report("14:05", "AUFKLÄRUNG VON SERGEANT KLEIN",
                "Feindliche Kavallerie gesichtet, etwa 200 Mann, 2km südöstlich von unserem Hauptquartier. Bewegungsrichtung unklar.",
                "normal"),
    ]
     

    

