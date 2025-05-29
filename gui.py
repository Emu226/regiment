#Creating a GUI
#Based on the README.md
 
import pygame
import config
import message_system


# class UserInterface for using in the main-loop
class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text_panel_rect = pygame.Rect(50, 50, 800, 800)  # Left panel for text
        self.visual_panel_rect = pygame.Rect(900, 50, 900, 800)  # Right panel for images
        self.input_box = pygame.Rect(50, 900, 800, 40)  # Input box at the bottom
        self.input_text = ''
        self.input_active = False  # Track if input box is active
        self.cursor_timer = 0  # Timer for cursor blinking
        self.cursor_visible = True  # Current cursor visibility state
        self.message_panel = message_system.MessagePanel(self.text_panel_rect)
    
    def draw(self):
        # Update cursor blinking timer
        if self.input_active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:  # Blink every 30 frames (0.5 seconds at 60 FPS)
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False

        # Draw text panel
        # pygame.draw.rect(self.screen, config.Colors.PANEL_BG, self.text_panel_rect)
        # pygame.draw.rect(self.screen, config.Colors.BORDER, self.text_panel_rect, 2)
        self.message_panel.draw(self.screen)

        # Draw visual panel
        pygame.draw.rect(self.screen, config.Colors.PANEL_BG, self.visual_panel_rect)
        pygame.draw.rect(self.screen, config.Colors.BORDER, self.visual_panel_rect, 2)
        
        # Draw input box
        pygame.draw.rect(self.screen, config.Colors.INPUT_BG, self.input_box)
        pygame.draw.rect(self.screen, config.Colors.BLACK, self.input_box, 2) # Border around the input box
        input_surface = self.font.render(self.input_text, True, config.Colors.TEXT_PRIMARY)
        self.screen.blit(input_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Draw cursor if input is active and cursor should be visible
        if self.input_active and self.cursor_visible:
            # Calculate cursor position after the text
            text_width = self.font.size(self.input_text)[0]
            cursor_x = self.input_box.x + 5 + text_width
            cursor_y = self.input_box.y + 5
            cursor_height = self.font.get_height()
            pygame.draw.line(self.screen, config.Colors.TEXT_PRIMARY, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    def handle_user_input(self, event):
    # Methon to handle user input after mouse-click into input_box
        self.message_panel.handle_scroll(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
                self.cursor_timer = 0
                self.cursor_visible = True
            else:
                self.input_active = False

        elif event.type == pygame.KEYDOWN and self.input_active:
            # Reset cursor visibility and timer on any key press
            self.cursor_visible = True
            self.cursor_timer = 0

            if event.key == pygame.K_RETURN:
                # Process the input text (e.g. give a command)
                print(f"Command entered: {self.input_text}")
                self.input_text = "" #Clear input after processing
                self.input_active = False  # Deactivate input after enter
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1] # Remove last character
            else:
                # Add typed character to input text
                self.input_text += event.unicode
                    







