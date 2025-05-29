# Kernidee: Der Spieler übernimmt die Rolle eines Generals während einer Schlacht. Er hat keine direkte Sicht auf das gesamte 
# Schlachtfeld und muss Entscheidungen basierend auf unvollständigen, zeitverzögerten Informationen treffen.
# Besonderheit: Manche Ereignisse erlebt der General selbst (blaue Berichte), andere erfährt er nur durch Boten und Offiziere 
# (graue/rote Berichte). Dies schafft unterschiedliche Verlässlichkeitsgrade der Information.

# Technische Überlegungen:
# Pygame Implementation: Das linke Panel kann als scrollbarer Textbereich umgesetzt werden, während das rechte Panel verschiedene 
# Bilder basierend auf der aktuellen Situation anzeigt.
# Datenstruktur: Jeder Bericht hat Eigenschaften wie Zeitstempel, Zuverlässigkeit (hoch bei direkter Beobachtung, niedriger bei Boten), 
# und Aktualität. Dies beeinflusst, wie der Spieler die Information interpretiert.

# Immersion: Die unterschiedlichen Berichtsstile (direkte Beobachtung vs. Botenmeldungen) verstärken das Gefühl, wirklich ein General 
# zu sein, der auf fragmentierte Informationen angewiesen ist.


# 🎯 Kern-Anforderungen des Spiels
# Was das Spiel können muss:
#     • Rundenbasierter Ablauf mit Befehlspunkten 
#     • Unsichtbare Schlacht im Hintergrund simulieren 
#     • Informationsfilterung - Spieler bekommt nur Fragmente der Realität 
#     • Zeitverzögerung bei Berichten und Befehlsausführung 
#     • Verschiedene Informationsquellen mit unterschiedlicher Zuverlässigkeit 
#     • Visuelle Unterstützung durch statische Bilder 
#     • Befehlseingabe und -verarbeitung 

# 🏗️ Hauptkomponenten (Die "Bausteine" des Spiels)
# 1. Game Engine (Das Herzstück)
# GameEngine
# ├── Spiel-Loop (Hauptschleife)
# ├── Rundenmanagement
# ├── Eingabeverarbeitung
# └── Grafik-Updates
# 2. Battle Simulator (Die unsichtbare Schlacht)
# BattleSimulator
# ├── Echte Truppenpositionen
# ├── Kampfberechnungen
# ├── Bewegungslogik
# └── Ereignis-Generator
# 3. Information System (Der "Nebel des Krieges")
# InformationSystem
# ├── Nachrichtenfilter
# ├── Zeitverzögerung
# ├── Zuverlässigkeits-System
# └── Bericht-Generator
# 4. User Interface (Was der Spieler sieht)
# UserInterface
# ├── Text-Panel (Links)
# ├── Visual-Panel (Rechts)
# ├── Eingabefeld
# └── Status-Anzeigen

import pygame
import config
import gui
from message_system import Message, MessageType, MessagePanel
import mission_build

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("General's Command")
    clock = pygame.time.Clock()
    ui = gui.UserInterface(screen)
    return screen, clock, ui

def main():
    screen, clock, ui = initialize_game()

    # Test messages
    test_messages = mission_build.sample_messages()
    for test_messages in test_messages:
        ui.message_panel.add_message(test_messages)



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    # Handle keyboard input for the UI
                    ui.handle_user_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks for the UI
                ui.handle_user_input(event)
                print("input...")            

        #screen fill with background color
        screen.fill(config.Colors.BACKGROUND)
        # Draw user interface on top of background
        ui.draw()
        # Update the display
        pygame.display.flip()
        # Control the frame rate
        clock.tick(config.FPS)
        # Quite pygame
    pygame.quit()

if __name__ == "__main__":
    main()
    




        





            