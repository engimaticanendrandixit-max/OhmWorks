import pygame
from utils import Mode

TEXT = (255, 255, 255)
BUTTON = (70, 70, 90)
BUTTON_ACTIVE = (80, 160, 255)
STATUS_BG = (30, 30, 38)
STATUS_TEXT = (180, 180, 190)

# Mode toolbar - sits to the right of Solve/Clear/Export
MODE_BUTTONS = {
    Mode.MOVE:    pygame.Rect(810, 640, 110, 40),
    Mode.CONNECT: pygame.Rect(930, 640, 110, 40),
    Mode.DELETE:  pygame.Rect(1050, 640, 110, 40),
}


def draw_mode_buttons(screen, font, current_mode):
    for mode, rect in MODE_BUTTONS.items():
        color = BUTTON_ACTIVE if mode == current_mode else BUTTON
        pygame.draw.rect(screen, color, rect, border_radius=8)
        label = font.render(mode.value, True, TEXT)
        screen.blit(label, label.get_rect(center=rect.center))


def get_clicked_mode(mouse_pos):
    for mode, rect in MODE_BUTTONS.items():
        if rect.collidepoint(mouse_pos):
            return mode
    return None


def draw_status_bar(screen, font, current_mode, mouse_pos, width, height):
    bar_rect = pygame.Rect(0, height - 25, width, 25)
    pygame.draw.rect(screen, STATUS_BG, bar_rect)
    text = f"Mode: {current_mode.value}    X: {mouse_pos[0]}   Y: {mouse_pos[1]}"
    label = font.render(text, True, STATUS_TEXT)
    screen.blit(label, (10, height - 22))
