#create funktion to create the GUI for the main window, with pygame.
#Based on the README.md
import pygame
import pygame.freetype
import mission_build

class TextPanel():
    #Left Panel, for reports, story, orders, etc.

    def __init__(self, x:int, y:int, width:int, height:int):
        self.rect = pygame.Rect(x, y, width, height)
        self.reports: List[mission_build.Report] = []
        self.scroll_offset = 0
        self.max_scroll = 0

        #Font settings
        self.font = pygame.freetype.Font(None, 14)
        self.header_font = pygame.freetype.Font(None, 16)

        # Define areas
        header_height = 40
        command_height = 200

        self.header_rect = pygame.Rect(x, y, width, header_height)
        self.reports_rect = pygame.Rect(x, y + header_height, width, height - header_height - command_height)
        self.command_rect = pygame.Rect(x, y + height - command_height, width, command_height)

        #Input field
        self.input_text = ""
        self.input_active = False
        self.cursor_pos = 0

        # Load sample reports
        mission_build._load_sample_reports()

        self.reports = mission_build.sample_reports
        self._calculate_scroll_bounds()

    def _calculate_scroll_bounds(self):
    




