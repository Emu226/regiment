import pygame
import pygame.freetype
import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum
import gui
import mission_build

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
     
     
class ReportManager:
    """Verwaltet die Reports und deren Daten"""
    
    def __init__(self):
        self.reports: List[Report] = []
        self._load_sample_reports()
    
    def add_report(self, report: Report):
        """Fügt einen neuen Report hinzu"""
        self.reports.append(report)
    
    def get_reports(self) -> List[Report]:
        """Gibt alle Reports zurück"""
        return self.reports
    
    def _load_sample_reports(self):
        """Lädt Beispiel-Reports"""
        mission_build._load_sample_reports()
        self.reports = mission_build.sample_reports


class CommandProcessor:
    """Verarbeitet eingegebene Befehle"""
    
    def __init__(self, report_manager: ReportManager):
        self.report_manager = report_manager
        self.available_commands = [
            "BEWEGEN [Regiment] [Position]",
            "ANGRIFF [Regiment] [Ziel]",
            "VERSTÄRKEN [Regiment] [Unterstützung]",
            "RÜCKZUG [Regiment] [Position]"
        ]
    
    def process_command(self, command: str) -> Report:
        """Verarbeitet einen Befehl und erstellt Report"""
        # Hier könnte komplexere Befehlslogik stehen
        report = Report(
            "14:30",
            "BEFEHLSBESTÄTIGUNG", 
            f"Befehl empfangen: {command}",
            "normal"
        )
        self.report_manager.add_report(report)
        return report
    
    def get_help_text(self) -> List[str]:
        """Gibt Hilfetext für verfügbare Befehle zurück"""
        return ["Verfügbare Befehle:"] + [f"• {cmd}" for cmd in self.available_commands]
    

