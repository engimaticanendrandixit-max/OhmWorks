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
    component is hit first. Hit-box stays axis-aligned regardless of
    rotation - close enough for a symbol-sized bounding box.
    """
    mx, my = mouse_pos
    for i in range(len(placed_components) - 1, -1, -1):
        component, x, y, angle = placed_components[i]
        if x - 50 <= mx <= x + 50 and y - 30 <= my <= y + 30:
            return i
    return None


def get_terminal_at(mouse_pos, placed_components, get_terminals_fn, radius=10):
    """
    Returns (component_index, "left"/"right") if mouse_pos is near a
    terminal, else None.
    """
    mx, my = mouse_pos
    for i, (component, x, y, angle) in enumerate(placed_components):
        left, right = get_terminals_fn(component, x, y, angle)
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


def point_in_rect(pos, rect):
    """rect = (x, y, w, h)"""
    x0, y0, w, h = rect
    return x0 <= pos[0] <= x0 + w and y0 <= pos[1] <= y0 + h


def orthogonal_route(start, end):
    """
    v0.3.0 - Auto Manhattan (right-angle) routing between two points,
    used when a connection has no manually placed waypoints.
    Routes horizontal-first then vertical.
    """
    x1, y1 = start
    x2, y2 = end
    if x1 == x2 or y1 == y2:
        return [start, end]
    bend = (x2, y1)
    return [start, bend, end]


def build_wire_path(start_pos, end_pos, waypoints):
    """
    v0.3.0 - Full path for a connection: manual waypoints if the user
    placed any while wiring, otherwise an auto orthogonal route.
    """
    if waypoints:
        return [start_pos] + list(waypoints) + [end_pos]
    return orthogonal_route(start_pos, end_pos)


def compute_junctions(connections):
    """
    v0.3.0 - Returns a set of (component_index, terminal) pairs where two
    or more wires meet at the same terminal, so the UI can draw a
    junction node there.
    """
    counts = {}
    for start, start_t, end, end_t, _ in connections:
        counts[(start, start_t)] = counts.get((start, start_t), 0) + 1
        counts[(end, end_t)] = counts.get((end, end_t), 0) + 1
    return {key for key, count in counts.items() if count >= 2}
