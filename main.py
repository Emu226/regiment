import pygame
import pygame.freetype
import sys
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum
import gui
import mission_build
import config

# Initialisierung von pygame
pygame.init()

screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
# Im Game Loop:
text_panel = gui.TextPanel(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

# Events weiterleiten:
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        text_panel.handle_input(event)
    elif event.type == pygame.MOUSEWHEEL:
        if text_panel.reports_rect.collidepoint(pygame.mouse.get_pos()):
            text_panel.handle_scroll(-event.y)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        text_panel.handle_mouse_click(event.pos)

# Zeichnen:
text_panel.draw(screen)