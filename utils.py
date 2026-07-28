import pygame
from enum import Enum


class Mode(Enum):
    MOVE = "Move"
    CONNECT = "Connect"
    DELETE = "Delete"


def get_component_at(mouse_pos, placed_components):
    """
    Returns the index of the top-most component under mouse_pos, else None.
    Iterates in reverse so the most recently placed (visually on top)
    component is hit first.
    """
    mx, my = mouse_pos
    for i in range(len(placed_components) - 1, -1, -1):
        component, x, y = placed_components[i]
        if x - 50 <= mx <= x + 50 and y - 30 <= my <= y + 30:
            return i
    return None


def get_terminal_at(mouse_pos, placed_components, get_terminals_fn, radius=10):
    """
    Returns (component_index, "left"/"right") if mouse_pos is near a
    terminal, else None.
    """
    mx, my = mouse_pos
    for i, (component, x, y) in enumerate(placed_components):
        left, right = get_terminals_fn(component, x, y)
        if abs(mx - left[0]) < radius and abs(my - left[1]) < radius:
            return (i, "left")
        if abs(mx - right[0]) < radius and abs(my - right[1]) < radius:
            return (i, "right")
    return None


def draw_grid(screen, rect, spacing=20, color=(65, 65, 78)):
    """
    Draws a PSpice/KiCad-style line grid inside rect = (x, y, w, h).
    """
    x0, y0, w, h = rect
    for gx in range(x0, x0 + w, spacing):
        pygame.draw.line(screen, color, (gx, y0), (gx, y0 + h), 1)
    for gy in range(y0, y0 + h, spacing):
        pygame.draw.line(screen, color, (x0, gy), (x0 + w, gy), 1)
