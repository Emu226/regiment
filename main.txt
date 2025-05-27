import pygame
import pygame.freetype
import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum

# Initialisierung von pygame
pygame.init()

# Konstanten
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

# Farbschema (militärisch-dunkel)
class Colors:
    BACKGROUND = (28, 28, 28)          # #1c1c1c
    PANEL_BG = (37, 37, 37)            # #252525
    BORDER = (139, 115, 85)            # #8b7355
    TEXT_PRIMARY = (212, 212, 212)     # #d4d4d4
    TEXT_SECONDARY = (139, 115, 85)    # #8b7355
    HEADER_BG = (139, 115, 85)         # #8b7355
    HEADER_TEXT = (30, 30, 30)         # #1e1e1e
    URGENT_BORDER = (255, 68, 68)      # #ff4444
    WITNESSED_BORDER = (68, 255, 68)   # #44ff44
    INPUT_BG = (30, 30, 30)            # #1e1e1e

@dataclass
class Report:
    """Repräsentiert einen Bericht"""
    timestamp: str
    source: str
    content: str
    report_type: str  # "normal", "urgent", "witnessed"
    
class TextPanel:
    """Linkes Panel für Berichte und Befehle"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.reports: List[Report] = []
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Font-Setup
        self.font = pygame.freetype.Font(None, 14)
        self.header_font = pygame.freetype.Font(None, 16)
        
        # Bereiche definieren
        header_height = 40
        command_height = 200
        
        self.header_rect = pygame.Rect(x, y, width, header_height)
        self.reports_rect = pygame.Rect(x, y + header_height, width, height - header_height - command_height)
        self.command_rect = pygame.Rect(x, y + height - command_height, width, command_height)
        
        # Eingabefeld
        self.input_text = ""
        self.input_active = False
        self.cursor_pos = 0
        
        # Beispiel-Berichte laden
        self._load_sample_reports()
    
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
        self.reports = sample_reports
        self._calculate_scroll_bounds()
    
    def _calculate_scroll_bounds(self):
        """Berechnet Scroll-Grenzen basierend auf Anzahl der Berichte"""
        report_height = 80  # Geschätzte Höhe pro Bericht
        total_content_height = len(self.reports) * report_height
        visible_height = self.reports_rect.height
        self.max_scroll = max(0, total_content_height - visible_height)
    
    def handle_scroll(self, direction: int):
        """Behandelt Scrollen (direction: -1 für hoch, 1 für runter)"""
        scroll_speed = 20
        self.scroll_offset += direction * scroll_speed
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
    
    def handle_input(self, event):
        """Behandelt Tastatureingaben"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self._process_command(self.input_text.strip())
                    self.input_text = ""
                    self.cursor_pos = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.input_text = self.input_text[:self.cursor_pos-1] + self.input_text[self.cursor_pos:]
                    self.cursor_pos -= 1
            else:
                # Normale Zeichen hinzufügen
                if event.unicode and event.unicode.isprintable():
                    self.input_text = self.input_text[:self.cursor_pos] + event.unicode + self.input_text[self.cursor_pos:]
                    self.cursor_pos += 1
    
    def _process_command(self, command: str):
        """Verarbeitet eingegebene Befehle (erstmal nur Dummy)"""
        # Füge den Befehl als neuen "Bericht" hinzu
        new_report = Report(
            "14:30", 
            "BEFEHLSBESTÄTIGUNG",
            f"Befehl empfangen: {command}",
            "normal"
        )
        self.reports.append(new_report)
        self._calculate_scroll_bounds()
        # Auto-scroll zu neuesten Nachrichten
        self.scroll_offset = self.max_scroll
    
    def draw(self, screen):
        """Zeichnet das Text-Panel"""
        # Panel-Hintergrund
        pygame.draw.rect(screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, Colors.BORDER, self.rect, 2)
        
        # Header zeichnen
        pygame.draw.rect(screen, Colors.HEADER_BG, self.header_rect)
        header_text = "FELDKOMMANDO - RUNDE 7"
        text_rect = self.header_font.get_rect(header_text)
        x = self.header_rect.centerx - text_rect.width // 2
        y = self.header_rect.centery - text_rect.height // 2
        self.header_font.render_to(screen, (x, y), header_text, Colors.HEADER_TEXT)
        
        # Berichte zeichnen
        self._draw_reports(screen)
        
        # Befehls-Sektion zeichnen
        self._draw_command_section(screen)
    
    def _draw_reports(self, screen):
        """Zeichnet den Berichte-Bereich"""
        # Clipping-Bereich setzen
        screen.set_clip(self.reports_rect)
        
        y_offset = self.reports_rect.y - self.scroll_offset
        
        for report in self.reports:
            report_rect = pygame.Rect(
                self.reports_rect.x + 10,
                y_offset,
                self.reports_rect.width - 20,
                75
            )
            
            # Nur zeichnen wenn sichtbar
            if report_rect.bottom > self.reports_rect.top and report_rect.top < self.reports_rect.bottom:
                self._draw_single_report(screen, report, report_rect)
            
            y_offset += 80
        
        # Clipping zurücksetzen
        screen.set_clip(None)
        
        # Rahmen um Berichte-Bereich
        pygame.draw.rect(screen, Colors.BORDER, self.reports_rect, 1)
    
    def _draw_single_report(self, screen, report: Report, rect: pygame.Rect):
        """Zeichnet einen einzelnen Bericht"""
        # Hintergrund
        pygame.draw.rect(screen, Colors.BACKGROUND, rect)
        
        # Border je nach Report-Typ
        border_color = Colors.BORDER
        if report.report_type == "urgent":
            border_color = Colors.URGENT_BORDER
        elif report.report_type == "witnessed":
            border_color = Colors.WITNESSED_BORDER
        
        pygame.draw.rect(screen, border_color, rect, 2)
        
        # Header
        header_text = f"{report.source} - {report.timestamp}"
        self.font.render_to(screen, (rect.x + 5, rect.y + 5), header_text, Colors.TEXT_SECONDARY)
        
        # Content (mit Zeilenumbruch)
        content_lines = self._wrap_text(report.content, rect.width - 10)
        y_pos = rect.y + 25
        for line in content_lines[:3]:  # Max 3 Zeilen pro Bericht
            self.font.render_to(screen, (rect.x + 5, y_pos), line, Colors.TEXT_PRIMARY)
            y_pos += 16
    
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Bricht Text in Zeilen um"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if self.font.get_rect(test_line).width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _draw_command_section(self, screen):
        """Zeichnet den Befehls-Eingabe-Bereich"""
        # Hintergrund
        pygame.draw.rect(screen, Colors.BACKGROUND, self.command_rect)
        pygame.draw.rect(screen, Colors.BORDER, self.command_rect, 1)
        
        # Header
        header_rect = pygame.Rect(self.command_rect.x, self.command_rect.y, self.command_rect.width, 30)
        pygame.draw.rect(screen, Colors.HEADER_BG, header_rect)
        self.header_font.render_to(screen, (header_rect.x + 10, header_rect.y + 8), "BEFEHLSAUSGABE", Colors.HEADER_TEXT)
        
        # Verfügbare Befehle
        help_text = [
            "Verfügbare Befehle:",
            "• BEWEGEN [Regiment] [Position]",
            "• ANGRIFF [Regiment] [Ziel]", 
            "• VERSTÄRKEN [Regiment] [Unterstützung]",
            "• RÜCKZUG [Regiment] [Position]"
        ]
        
        y_pos = self.command_rect.y + 40
        for line in help_text:
            self.font.render_to(screen, (self.command_rect.x + 10, y_pos), line, Colors.TEXT_PRIMARY)
            y_pos += 18
        
        # Eingabefeld
        input_rect = pygame.Rect(
            self.command_rect.x + 10,
            self.command_rect.bottom - 40,
            self.command_rect.width - 20,
            30
        )
        pygame.draw.rect(screen, Colors.INPUT_BG, input_rect)
        pygame.draw.rect(screen, Colors.BORDER, input_rect, 1)
        
        # Eingabe-Text
        display_text = self.input_text if self.input_text else "Befehl eingeben..."
        text_color = Colors.TEXT_PRIMARY if self.input_text else Colors.TEXT_SECONDARY
        self.font.render_to(screen, (input_rect.x + 5, input_rect.y + 8), display_text, text_color)


class VisualPanel:
    """Rechtes Panel für visuelle Darstellungen"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.freetype.Font(None, 16)
        self.large_font = pygame.freetype.Font(None, 18)
        
        # Bereiche definieren
        header_height = 40
        status_height = 80
        
        self.header_rect = pygame.Rect(x, y, width, header_height)
        self.map_rect = pygame.Rect(x, y + header_height, width, height - header_height - status_height)
        self.status_rect = pygame.Rect(x, y + height - status_height, width, status_height)
    
    def draw(self, screen):
        """Zeichnet das Visual-Panel"""
        # Panel-Hintergrund
        pygame.draw.rect(screen, Colors.BACKGROUND, self.rect)
        pygame.draw.rect(screen, Colors.BORDER, self.rect, 2)
        
        # Header zeichnen
        pygame.draw.rect(screen, Colors.HEADER_BG, self.header_rect)
        header_text = "TAKTISCHE ÜBERSICHT"
        text_rect = self.font.get_rect(header_text)
        x = self.header_rect.centerx - text_rect.width // 2
        y = self.header_rect.centery - text_rect.height // 2
        self.font.render_to(screen, (x, y), header_text, Colors.HEADER_TEXT)
        
        # Karten-Bereich zeichnen
        self._draw_map_area(screen)
        
        # Status-Bar zeichnen
        self._draw_status_bar(screen)
    
    def _draw_map_area(self, screen):
        """Zeichnet den Karten-Bereich mit Placeholder"""
        # Hintergrund mit Gitter-Muster
        pygame.draw.rect(screen, Colors.PANEL_BG, self.map_rect)
        
        # Einfaches Gitter-Muster zeichnen
        grid_size = 20
        for x in range(self.map_rect.x, self.map_rect.right, grid_size):
            pygame.draw.line(screen, (50, 50, 50), (x, self.map_rect.y), (x, self.map_rect.bottom))
        for y in range(self.map_rect.y, self.map_rect.bottom, grid_size):
            pygame.draw.line(screen, (50, 50, 50), (self.map_rect.x, y), (self.map_rect.right, y))
        
        # Placeholder-Box in der Mitte
        placeholder_width = self.map_rect.width // 2
        placeholder_height = self.map_rect.height // 2
        placeholder_rect = pygame.Rect(
            self.map_rect.centerx - placeholder_width // 2,
            self.map_rect.centery - placeholder_height // 2,
            placeholder_width,
            placeholder_height
        )
        
        # Gestrichelte Umrandung
        pygame.draw.rect(screen, Colors.BORDER, placeholder_rect, 2)
        
        # Placeholder-Text
        placeholder_lines = [
            "HIER: Karte des Schlachtfeldes",
            "Regimentsporträts",
            "Geländedarstellungen", 
            "Wetterinfos",
            "",
            "Statische Bilder unterstützen",
            "die Immersion und das Verständnis"
        ]
        
        y_offset = placeholder_rect.y + 20
        for i, line in enumerate(placeholder_lines):
            if line:  # Leere Zeilen überspringen
                text_rect = self.font.get_rect(line)
                x = placeholder_rect.centerx - text_rect.width // 2
                style = pygame.freetype.STYLE_NORMAL if i >= 5 else pygame.freetype.STYLE_NORMAL
                self.font.render_to(screen, (x, y_offset), line, Colors.TEXT_SECONDARY, style=style)
            y_offset += 20
        
        # Rahmen um Karten-Bereich
        pygame.draw.rect(screen, Colors.BORDER, self.map_rect, 1)
    
    def _draw_status_bar(self, screen):
        """Zeichnet die Status-Bar unten"""
        pygame.draw.rect(screen, Colors.PANEL_BG, self.status_rect)
        pygame.draw.rect(screen, Colors.BORDER, self.status_rect, 1)
        
        # Linke Seite: Schlacht-Info
        battle_info = [
            "Tag 3 - Schlacht bei Mühlberg",
            "Zeit: 14:25 | Wetter: Bewölkt, leichter Regen"
        ]
        
        y_pos = self.status_rect.y + 15
        for line in battle_info:
            self.font.render_to(screen, (self.status_rect.x + 15, y_pos), line, Colors.TEXT_PRIMARY)
            y_pos += 20
        
        # Rechte Seite: Befehlspunkte
        command_points_rect = pygame.Rect(
            self.status_rect.right - 120,
            self.status_rect.y + 20,
            100,
            30
        )
        pygame.draw.rect(screen, Colors.HEADER_BG, command_points_rect)
        
        cp_text = "Befehlspunkte: 3/5"
        text_rect = self.font.get_rect(cp_text)
        x = command_points_rect.centerx - text_rect.width // 2
        y = command_points_rect.centery - text_rect.height // 2
        self.font.render_to(screen, (x, y), cp_text, Colors.HEADER_TEXT)


class GameEngine:
    """Haupt-Spiel-Engine"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("General's Command - Prototyp")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Panel-Setup (35% links, 65% rechts)
        text_panel_width = int(WINDOW_WIDTH * 0.35)
        visual_panel_width = WINDOW_WIDTH - text_panel_width
        
        self.text_panel = TextPanel(0, 0, text_panel_width, WINDOW_HEIGHT)
        self.visual_panel = VisualPanel(text_panel_width, 0, visual_panel_width, WINDOW_HEIGHT)
    
    def handle_events(self):
        """Behandelt alle pygame Events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.text_panel.handle_input(event)
            
            elif event.type == pygame.MOUSEWHEEL:
                # Scrollen nur wenn Maus über Text-Panel
                mouse_pos = pygame.mouse.get_pos()
                if self.text_panel.reports_rect.collidepoint(mouse_pos):
                    self.text_panel.handle_scroll(-event.y)
    
    def update(self):
        """Update-Logic (aktuell noch leer)"""
        pass
    
    def draw(self):
        """Zeichnet alles auf den Bildschirm"""
        self.screen.fill(Colors.BACKGROUND)
        
        # Panels zeichnen
        self.text_panel.draw(self.screen)
        self.visual_panel.draw(self.screen)
        
        # Trennlinie zwischen Panels
        separator_x = self.text_panel.rect.right
        pygame.draw.line(
            self.screen, 
            Colors.BORDER, 
            (separator_x, 0), 
            (separator_x, WINDOW_HEIGHT), 
            3
        )
        
        pygame.display.flip()
    
    def run(self):
        """Haupt-Game-Loop"""
        print("General's Command - Prototyp gestartet!")
        print("Verwenden Sie die Maus zum Scrollen in den Berichten.")
        print("Geben Sie Befehle unten ein und drücken Sie Enter.")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Hauptfunktion - Startet das Spiel"""
    try:
        game = GameEngine()
        game.run()
    except Exception as e:
        print(f"Fehler beim Starten des Spiels: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()