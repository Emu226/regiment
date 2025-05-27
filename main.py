import pygame
import sys
from typing import Dict, List

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
FPS = 60
TEXT_PANEL_WIDTH = WINDOW_WIDTH // 3
VISUAL_PANEL_WIDTH = WINDOW_WIDTH - TEXT_PANEL_WIDTH

# Colors
DARK_GRAY = (44, 44, 44)
BROWN = (139, 115, 85)
LIGHT_GRAY = (212, 212, 212)

class GameState:
    def __init__(self):
        self.turn = 1
        self.command_points = 5
        self.reports: List[Dict] = []
        self.time = "14:00"
        
    def add_report(self, report_type: str, time: str, content: str):
        self.reports.append({
            "type": report_type,  # "urgent", "witnessed", or "normal"
            "time": time,
            "content": content
        })

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("General's Command")
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.font = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Test: Add a report when space is pressed
                    self.game_state.add_report("witnessed", "14:05", 
                        "New regiment spotted at position Delta")
        return True

    def update(self):
        # Game logic updates here
        pass

    def draw(self):
        self.screen.fill(DARK_GRAY)
        
        # Draw text panel (left side)
        text_panel = pygame.Surface((TEXT_PANEL_WIDTH, WINDOW_HEIGHT))
        text_panel.fill((37, 37, 37))
        
        # Draw header
        header = pygame.Surface((TEXT_PANEL_WIDTH, 40))
        header.fill(BROWN)
        text = self.font.render(f"FELDKOMMANDO - RUNDE {self.game_state.turn}", True, DARK_GRAY)
        header.blit(text, (10, 10))
        text_panel.blit(header, (0, 0))
        
        # Draw reports
        y_offset = 50
        for report in self.game_state.reports:
            report_surface = self._create_report(report)
            text_panel.blit(report_surface, (10, y_offset))
            y_offset += 100
        
        # Draw visual panel (right side)
        visual_panel = pygame.Surface((VISUAL_PANEL_WIDTH, WINDOW_HEIGHT))
        visual_panel.fill((30, 30, 30))
        
        # Draw map placeholder
        pygame.draw.rect(visual_panel, BROWN, (20, 50, VISUAL_PANEL_WIDTH-40, WINDOW_HEIGHT-100), 2)
        map_text = self.font.render("TACTICAL MAP", True, BROWN)
        visual_panel.blit(map_text, (VISUAL_PANEL_WIDTH//2 - 50, WINDOW_HEIGHT//2))
        
        # Blit panels to screen
        self.screen.blit(text_panel, (0, 0))
        self.screen.blit(visual_panel, (TEXT_PANEL_WIDTH, 0))
        
        pygame.display.flip()

    def _create_report(self, report: Dict) -> pygame.Surface:
        surface = pygame.Surface((TEXT_PANEL_WIDTH - 20, 90))
        surface.fill((42, 42, 42))
        
        # Draw report header
        time_text = self.font.render(f"{report['time']} - {report['type'].upper()}", True, BROWN)
        surface.blit(time_text, (10, 5))
        
        # Draw report content (with word wrap)
        words = report['content'].split()
        line = ""
        y_offset = 30
        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] > TEXT_PANEL_WIDTH - 40:
                content_text = self.font.render(line, True, LIGHT_GRAY)
                surface.blit(content_text, (10, y_offset))
                y_offset += 20
                line = word + " "
            else:
                line = test_line
                
        if line:
            content_text = self.font.render(line, True, LIGHT_GRAY)
            surface.blit(content_text, (10, y_offset))
            
        return surface

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

