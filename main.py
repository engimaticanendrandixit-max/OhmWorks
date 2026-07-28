import pygame
import sys
from components import *
from utils import Mode, get_component_at, get_terminal_at, draw_grid
from ui import draw_mode_buttons, get_clicked_mode, draw_status_bar


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
BUTTON_ACTIVE = (80, 160, 255)
TEXT = (255, 255, 255)

CANVAS_RECT = (260, 20, 920, 600)

font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 14)

running = True

selected_component = None
placed_components = []
connections = []
wire_start = None
wire_terminal = None

dragging = False
drag_index = None

# v0.2.0: interaction mode - Move / Connect / Delete
current_mode = Mode.MOVE


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            dragging = False

            # 1) Mode toolbar click - switch mode, nothing else this click
            clicked_mode = get_clicked_mode((mouse_x, mouse_y))
            if clicked_mode is not None:
                current_mode = clicked_mode
                wire_start = None
                wire_terminal = None
                continue

            # 2) Connect Mode - terminal-to-terminal wiring
            if current_mode == Mode.CONNECT:
                hit = get_terminal_at((mouse_x, mouse_y), placed_components, get_terminals)
                if hit is not None:
                    i, terminal = hit
                    if wire_start is None:
                        wire_start = i
                        wire_terminal = terminal
                    else:
                        connections.append((wire_start, wire_terminal, i, terminal))
                        wire_start = None
                        wire_terminal = None
                    continue

            # 3) Move Mode - pick up a component to drag
            if current_mode == Mode.MOVE:
                idx = get_component_at((mouse_x, mouse_y), placed_components)
                if idx is not None:
                    dragging = True
                    drag_index = idx
                    continue

            # 4) Delete Mode - remove component + its connections
            if current_mode == Mode.DELETE:
                idx = get_component_at((mouse_x, mouse_y), placed_components)
                if idx is not None:
                    placed_components.pop(idx)

                    # connections store indices into placed_components, so
                    # drop any wire touching the deleted part and shift the
                    # indices of everything that came after it
                    new_connections = []
                    for start, start_t, end, end_t in connections:
                        if start == idx or end == idx:
                            continue
                        if start > idx:
                            start -= 1
                        if end > idx:
                            end -= 1
                        new_connections.append((start, start_t, end, end_t))
                    connections[:] = new_connections

                    if wire_start == idx:
                        wire_start = None
                        wire_terminal = None
                    continue

            # 5) Component palette selection / placement (any mode)
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
            if current_mode == Mode.MOVE and dragging and drag_index is not None:
                mouse_x, mouse_y = event.pos
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
        is_selected = component == selected_component

        pygame.draw.rect(
            screen,
            BUTTON_ACTIVE if is_selected else BUTTON,
            (25, y, 200, 50),
            border_radius=8
        )

        text = font.render(component, True, TEXT)
        screen.blit(text, (80, y + 15))

    # Canvas
    pygame.draw.rect(screen, CANVAS, CANVAS_RECT)
    draw_grid(screen, CANVAS_RECT)

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
        pygame.draw.line(screen, (255, 255, 0), start_pos, end_pos, 3)

    # Live preview of a wire being drawn in Connect Mode
    if current_mode == Mode.CONNECT and wire_start is not None:
        comp, cx, cy = placed_components[wire_start]
        left, right = get_terminals(comp, cx, cy)
        origin = left if wire_terminal == "left" else right
        pygame.draw.line(screen, (255, 255, 0), origin, pygame.mouse.get_pos(), 1)

    for i, (component, x, y) in enumerate(placed_components):
        if component == "Resistor":
            draw_resistor(screen, x, y)
        elif component == "Battery":
            draw_battery(screen, x, y)
        elif component == "Capacitor":
            draw_capacitor(screen, x, y)
        elif component == "Inductor":
            draw_inductor(screen, x, y)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (x - 30, y - 10, 60, 20), border_radius=5)

        left_terminal, right_terminal = get_terminals(component, x, y)
        pygame.draw.circle(screen, (255, 0, 0), left_terminal, 6)
        pygame.draw.circle(screen, (0, 255, 0), right_terminal, 6)

        # Highlight the component currently being dragged (Move Mode)
        if current_mode == Mode.MOVE and i == drag_index:
            pygame.draw.rect(screen, (80, 160, 255), (x - 55, y - 35, 110, 70), 2, border_radius=6)

        label = font.render(component[0], True, (0, 0, 0))
        screen.blit(label, (x - 5, y - 8))

    # Bottom action buttons
    pygame.draw.rect(screen, BUTTON, (300, 640, 120, 40))
    pygame.draw.rect(screen, BUTTON, (470, 640, 120, 40))
    pygame.draw.rect(screen, BUTTON, (640, 640, 120, 40))

    # Mode toolbar (Move / Connect / Delete)
    draw_mode_buttons(screen, font, current_mode)

    # Labels
    screen.blit(font.render("Components", True, TEXT), (60, 20))
    screen.blit(font.render("Solve", True, TEXT), (335, 650))
    screen.blit(font.render("Clear", True, TEXT), (505, 650))
    screen.blit(font.render("Export", True, TEXT), (670, 650))

    # Status bar
    draw_status_bar(screen, small_font, current_mode, pygame.mouse.get_pos(), WIDTH, HEIGHT)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
