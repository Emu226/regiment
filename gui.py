#create funktion to create the GUI for the main window, with pygame.
#Based on the README.md
import pygame
import pygame.freetype
import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum
import gui
import mission_build
import config


class ScrollManager:
    """Verwaltet Scrolling-Verhalten"""
    
    def __init__(self, content_height: int, visible_height: int):
        self.scroll_offset = 0
        self.content_height = content_height
        self.visible_height = visible_height
        self.max_scroll = max(0, content_height - visible_height)
    
    def update_content_height(self, new_height: int):
        """Aktualisiert die Content-Höhe"""
        self.content_height = new_height
        self.max_scroll = max(0, new_height - self.visible_height)
    
    def scroll(self, direction: int, speed: int = 20):
        """Scrollt in die angegebene Richtung"""
        self.scroll_offset += direction * speed
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
    
    def scroll_to_bottom(self):
        """Scrollt zum Ende"""
        self.scroll_offset = self.max_scroll


class InputHandler:
    """Verwaltet Texteingabe und Cursor"""
    
    def __init__(self):
        self.text = ""
        self.cursor_pos = 0
        self.is_active = False
    
    def handle_keydown(self, event) -> str:
        """Verarbeitet Tastatureingaben, gibt Command zurück wenn Enter gedrückt"""
        if not self.is_active:
            return ""
            
        if event.key == pygame.K_RETURN:
            command = self.text
            self.clear()
            return command
        elif event.key == pygame.K_BACKSPACE:
            if self.text:
                self.text = self.text[:-1]
                self.cursor_pos = max(0, self.cursor_pos - 1)
        elif event.key == pygame.K_LEFT:
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif event.key == pygame.K_RIGHT:
            self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
        elif event.unicode and event.unicode.isprintable():
            self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        
        return ""
    
    def clear(self):
        """Leert die Eingabe"""
        self.text = ""
        self.cursor_pos = 0
    
    def activate(self):
        """Aktiviert die Eingabe"""
        self.is_active = True
    
    def deactivate(self):
        """Deaktiviert die Eingabe"""
        self.is_active = False



class TextRenderer:
    """Verwaltet Text-Rendering und Formatierung"""
    
    def __init__(self):
        self.font = pygame.freetype.Font(None, 14)
        self.header_font = pygame.freetype.Font(None, 16)
    
    def wrap_text(self, text: str, max_width: int) -> List[str]:
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
    
    def render_text(self, screen, pos, text, color):
        """Rendert Text an Position"""
        self.font.render_to(screen, pos, text, color)
    
    def render_header(self, screen, pos, text, color):
        """Rendert Header-Text"""
        self.header_font.render_to(screen, pos, text, color)


# === 6. Neue modulare TextPanel ===
class TextPanel:
    """Hauptklasse die alle Module koordiniert"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        
        # Layout definieren
        header_height = 40
        command_height = 200
        
        self.header_rect = pygame.Rect(x, y, width, header_height)
        self.reports_rect = pygame.Rect(x, y + header_height, width, height - header_height - command_height)
        self.command_rect = pygame.Rect(x, y + height - command_height, width, command_height)
        
        # Module initialisieren
        self.report_manager = mission_build.ReportManager()
        self.scroll_manager = ScrollManager(
            content_height=len(self.report_manager.get_reports()) * 80,
            visible_height=self.reports_rect.height
        )
        self.command_processor = mission_build.CommandProcessor(self.report_manager)
        self.input_handler = InputHandler()
        self.text_renderer = TextRenderer()
        
        # Input standardmäßig aktivieren
        self.input_handler.activate()
    
    def handle_scroll(self, direction: int):
        """Delegiert Scrolling an ScrollManager"""
        self.scroll_manager.scroll(direction)
    
    def handle_input(self, event):
        """Delegiert Input-Handling"""
        command = self.input_handler.handle_keydown(event)
        if command:
            self.command_processor.process_command(command)
            # Content-Höhe aktualisieren und zum Ende scrollen
            new_height = len(self.report_manager.get_reports()) * 80
            self.scroll_manager.update_content_height(new_height)
            self.scroll_manager.scroll_to_bottom()
    
    def draw(self, screen):
        """Koordiniert das Zeichnen aller Bereiche"""
        # Panel-Hintergrund
        pygame.draw.rect(screen, config.Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, config.Colors.BORDER, self.rect, 2)
        
        self._draw_header(screen)
        self._draw_reports(screen)
        self._draw_command_section(screen)
    
    def _draw_header(self, screen):
        """Zeichnet Header"""
        pygame.draw.rect(screen, config.Colors.HEADER_BG, self.header_rect)
        header_text = "FELDKOMMANDO - RUNDE 7"
        text_rect = self.text_renderer.header_font.get_rect(header_text)
        x = self.header_rect.centerx - text_rect.width // 2
        y = self.header_rect.centery - text_rect.height // 2
        self.text_renderer.render_header(screen, (x, y), header_text, config.Colors.HEADER_TEXT)
    
    def _draw_reports(self, screen):
        """Zeichnet Reports mit Scrolling"""
        screen.set_clip(self.reports_rect)
        
        y_offset = self.reports_rect.y - self.scroll_manager.scroll_offset
        reports = self.report_manager.get_reports()
        
        for report in reports:
            report_rect = pygame.Rect(
                self.reports_rect.x + 10,
                y_offset,
                self.reports_rect.width - 20,
                75
            )
            
            if report_rect.bottom > self.reports_rect.top and report_rect.top < self.reports_rect.bottom:
                self._draw_single_report(screen, report, report_rect)
            
            y_offset += 80
        
        screen.set_clip(None)
        pygame.draw.rect(screen, config.Colors.BORDER, self.reports_rect, 1)
    
    def _draw_single_report(self, screen, report: mission_build.Report, rect: pygame.Rect):
        """Zeichnet einen einzelnen Report"""
        # Hintergrund und Border
        pygame.draw.rect(screen, config.Colors.BACKGROUND, rect)
        
        border_color = config.Colors.BORDER
        if report.report_type == "urgent":
            border_color = config.Colors.URGENT_BORDER
        elif report.report_type == "witnessed":
            border_color = config.Colors.WITNESSED_BORDER
        
        pygame.draw.rect(screen, border_color, rect, 2)
        
        # Header
        header_text = f"{report.source} - {report.timestamp}"
        self.text_renderer.render_text(screen, (rect.x + 5, rect.y + 5), header_text, config.Colors.TEXT_SECONDARY)
        
        # Content mit Zeilenumbruch
        content_lines = self.text_renderer.wrap_text(report.content, rect.width - 10)
        y_pos = rect.y + 25
        for line in content_lines[:3]:
            self.text_renderer.render_text(screen, (rect.x + 5, y_pos), line, config.Colors.TEXT_PRIMARY)
            y_pos += 16
    
    def _draw_command_section(self, screen):
        """Zeichnet Command-Sektion"""
        pygame.draw.rect(screen, config.Colors.BACKGROUND, self.command_rect)
        pygame.draw.rect(screen, config.Colors.BORDER, self.command_rect, 1)
        
        # Header
        header_rect = pygame.Rect(self.command_rect.x, self.command_rect.y, self.command_rect.width, 30)
        pygame.draw.rect(screen, config.Colors.HEADER_BG, header_rect)
        self.text_renderer.render_header(screen, (header_rect.x + 10, header_rect.y + 8), "BEFEHLSAUSGABE", config.Colors.HEADER_TEXT)
        
        # Hilfetext
        help_lines = self.command_processor.get_help_text()
        y_pos = self.command_rect.y + 40
        for line in help_lines:
            self.text_renderer.render_text(screen, (self.command_rect.x + 10, y_pos), line, config.Colors.TEXT_PRIMARY)
            y_pos += 18
        
        # Eingabefeld
        input_rect = pygame.Rect(
            self.command_rect.x + 10,
            self.command_rect.bottom - 40,
            self.command_rect.width - 20,
            30
        )
        pygame.draw.rect(screen, config.Colors.INPUT_BG, input_rect)
        pygame.draw.rect(screen, config.Colors.BORDER, input_rect, 1)
        
        # Eingabe-Text
        display_text = self.input_handler.text if self.input_handler.text else "Befehl eingeben..."
        text_color = config.Colors.TEXT_PRIMARY if self.input_handler.text else config.Colors.TEXT_SECONDARY
        self.text_renderer.render_text(screen, (input_rect.x + 5, input_rect.y + 8), display_text, text_color)


