import pygame
import sys 
from components import *


#Initializing pygame 
pygame.init()

# Window Setting
WIDTH = 1400
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('OHM_Works')
clock = pygame.time.Clock()

# Colors
BACKGROUND = (20, 20, 25)
PANEL = (35, 35, 45)
CANVAS = (50, 50, 60)
BUTTON = (70, 70, 90)
TEXT = (255, 255, 255)

font = pygame.font.SysFont("arial", 20)

running = True

selected_component = None
placed_components = []
connections = []
wire_start = None
wire_terminal = None

dragging = False
drag_index = None


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dragging = False

            for i, (component, x, y) in enumerate(placed_components):
                left_terminal, right_terminal = get_terminals(component, x, y)
                lx, ly = left_terminal
                rx, ry = right_terminal

    # Left terminal click

                if abs(mouse_x - lx) < 10 and abs(mouse_y - ly) < 10:

                    if wire_start is None:

                        wire_start = i
                        wire_terminal = "left"

                    else:
                        connections.append(
                        (wire_start, wire_terminal, i, "left")
                        )

                        wire_start = None
                        wire_terminal = None

                    break

            # Right terminal click

                elif abs(mouse_x - rx) < 10 and abs(mouse_y - ry) < 10:

                    if wire_start is None:
                        wire_start = i
                        wire_terminal = "right"

                    else:
                        connections.append((wire_start, wire_terminal, i, "right"))
                        wire_start = None
                        wire_terminal = None
                    break

# Component body click (drag)

            for i, (component, x, y) in enumerate(placed_components):

                if x - 50 <= mouse_x <= x + 50 and y - 30 <= mouse_y <= y + 30:
                    dragging = True
                    drag_index = i
                    break


            if not dragging:
                if 25 <= mouse_x <= 225:
                    if 80 <= mouse_y <= 130:
                        selected_component = "Resistor"
                    elif 150 <= mouse_y <= 200:
                        selected_component = "Battery"
                    elif 220 <= mouse_y <= 270:
                        selected_component = "Capacitor"
                    elif 290 <= mouse_y <= 340:
                        selected_component = "Inductor"
                    print("Selected:", selected_component)
                elif 260 <= mouse_x <= 1180 and 20 <= mouse_y <= 620:
                    if selected_component is not None:
                        placed_components.append((selected_component, mouse_x, mouse_y))

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            drag_index = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging and drag_index is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                component, _, _ = placed_components[drag_index]
                placed_components[drag_index] = (component, mouse_x, mouse_y)
   
    screen.fill(BACKGROUND)

    # Left panel
    pygame.draw.rect(screen, PANEL, (0, 0, 250, HEIGHT))

    # Components buttons
    components = [
        "Resistor",
        "Battery",
        "Capacitor",
        "Inductor"
    ]

    for i, component in enumerate(components):

        y = 80 + i * 70

        pygame.draw.rect(
            screen,
            BUTTON,
            (25, y, 200, 50),
            border_radius=8
        )

        text = font.render(component, True, TEXT)
        screen.blit(text, (80, y + 15))

    # Canvas

    pygame.draw.rect(screen, CANVAS, (260, 20, 920, 600))

    for start, start_terminal, end, end_terminal in connections:
        component1, x1, y1 = placed_components[start]
        component2, x2, y2 = placed_components[end]
        left1, right1 = get_terminals(component1, x1, y1)
        left2, right2 = get_terminals(component2, x2, y2)
        # Start position
        if start_terminal == "left":
            start_pos = left1
        else:
            start_pos = right1
    # End position
        if end_terminal == "left":
            end_pos = left2
        else:
            end_pos = right2
        pygame.draw.line(screen,(255, 255, 0),start_pos,end_pos,3)


    for component, x, y in placed_components:
        if component == "Resistor":
            draw_resistor(screen, x, y)
            left_terminal, right_terminal = get_terminals(component, x, y)
            pygame.draw.circle(screen,(255, 0, 0),left_terminal,6)
            pygame.draw.circle(screen,(0, 255, 0),right_terminal,6)

        elif component == "Battery":
            draw_battery(screen, x, y)
            left_terminal, right_terminal = get_terminals(component, x, y)
            pygame.draw.circle(screen,(255, 0, 0),left_terminal,6)
            pygame.draw.circle(screen,(0, 255, 0),right_terminal,6)


        elif component == "Capacitor":
            draw_capacitor(screen, x, y)
            left_terminal, right_terminal = get_terminals(component, x, y)
            pygame.draw.circle(screen,(255, 0, 0),left_terminal,6)
            pygame.draw.circle(screen,(0, 255, 0),right_terminal,6)
        
        elif component == "Inductor":
            draw_inductor(screen, x, y)
            left_terminal, right_terminal = get_terminals(component, x, y)
            pygame.draw.circle(screen,(255, 0, 0),left_terminal,6)
            pygame.draw.circle(screen,(0, 255, 0),right_terminal,6)

        else:
            pygame.draw.rect(screen,(220, 220, 220),(x - 30, y - 10, 60, 20),border_radius=5)
            left_terminal, right_terminal = get_terminals(component, x, y)
            pygame.draw.circle(screen,(255, 0, 0),left_terminal,6)
            pygame.draw.circle(screen,(0, 255, 0),right_terminal,6)

        label = font.render(
        component[0],
        True,
        (0, 0, 0)
        )

        screen.blit(
        label,
        (x - 5, y - 8)
        )
    pygame.display.update()

    # Bottom buttons
    pygame.draw.rect(screen, BUTTON, (300, 640, 120, 40))
    pygame.draw.rect(screen, BUTTON, (470, 640, 120, 40))
    pygame.draw.rect(screen, BUTTON, (640, 640, 120, 40))

    # Labels
    screen.blit(font.render("Components", True, TEXT), (60, 20))

    screen.blit(font.render("Solve", True, TEXT), (335, 650))
    screen.blit(font.render("Clear", True, TEXT), (505, 650))
    screen.blit(font.render("Export", True, TEXT), (670, 650))

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()

