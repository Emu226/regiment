from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import pygame
import config

class MessageType(Enum):
    WITNESSED = "witnessed"
    URGENT = "urgent"
    NORMAL = "normal"

@dataclass
class Message:
    type: MessageType
    sender: str
    time: str
    content: str
    timestamp: float = None

class MessagePanel:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.messages = []
        self.scroll_offset = 0
        self.font = pygame.font.Font(None, 24)
        self.header_font = pygame.font.Font(None, 28)
        
    def add_message(self, message: Message):
        self.messages.insert(0, message)  # Neue Nachrichten oben anfügen
        
    def draw(self, screen):
        # Panel Background
        pygame.draw.rect(screen, config.Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, config.Colors.BORDER, self.rect, 2)
        
        # Messages
        y_offset = self.rect.y + 10 - self.scroll_offset
        for message in self.messages:
            if y_offset > self.rect.bottom:
                break  # Skip messages outside visible area
                
            # Message color based on type
            color = {
                MessageType.WITNESSED: config.Colors.WITNESSED_BORDER,
                MessageType.URGENT: config.Colors.URGENT_BORDER,
                MessageType.NORMAL: config.Colors.TEXT_PRIMARY
            }[message.type]
            
            # Draw message box
            msg_rect = pygame.Rect(self.rect.x + 10, y_offset, 
                                 self.rect.width - 20, 80)
            pygame.draw.rect(screen, config.Colors.PANEL_BG, msg_rect)
            pygame.draw.rect(screen, color, msg_rect, 2)
            
            # Header
            header = f"{message.sender} - {message.time}"
            header_surf = self.header_font.render(header, True, color)
            screen.blit(header_surf, (msg_rect.x + 5, y_offset + 5))
            
            # Content (basic version - could be improved with text wrapping)
            content_surf = self.font.render(message.content[:50] + "...", True, 
                                          config.Colors.TEXT_PRIMARY)
            screen.blit(content_surf, (msg_rect.x + 5, y_offset + 35))
            
            y_offset += 90
            
    def handle_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                self.scroll_offset = max(0, self.scroll_offset - 30)
            elif event.button == 5:  # Mouse wheel down
                self.scroll_offset += 30

