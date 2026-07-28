import pygame

def draw_resistor(screen, x, y):

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 40, y),
        (x - 20, y),
        2
    )

    points = [
        (x - 20, y),
        (x - 10, y - 10),
        (x, y + 10),
        (x + 10, y - 10),
        (x + 20, y + 10),
        (x + 30, y)
    ]

    pygame.draw.lines(
        screen,
        (255, 255, 255),
        False,
        points,
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 30, y),
        (x + 50, y),
        2
    )

#Drawing Battery Symbol
def draw_battery(screen, x, y):

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 40, y),
        (x - 10, y),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 10, y - 20),
        (x - 10, y + 20),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 10, y - 10),
        (x + 10, y + 10),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 10, y),
        (x + 40, y),
        2
    )

# Drawing Capacitor Symbol
def draw_capacitor(screen, x, y):

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 40, y),
        (x - 10, y),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 10, y - 20),
        (x - 10, y + 20),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 10, y - 20),
        (x + 10, y + 20),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 10, y),
        (x + 40, y),
        2
    )                                                                                                                                          

# Drawing Inductor Symbol
def draw_inductor(screen, x, y):

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x - 40, y),
        (x - 20, y),
        2
    )

    for i in range(4):
        pygame.draw.arc(
            screen,
            (255, 255, 255),
            (x - 20 + i * 10, y - 10, 10, 20),
            3.14,
            0,
            2
        )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (x + 20, y),
        (x + 40, y),
        2
    )


def get_terminals(component, x, y, angle=0):

    angle = int(angle) % 360

    if component == "Resistor":
        left_offset, right_offset = (-40, 0), (40, 0)

    elif component == "Battery":
        left_offset, right_offset = (-30, 0), (30, 0)

    elif component == "Capacitor":
        left_offset, right_offset = (-30, 0), (30, 0)

    elif component == "Inductor":
        left_offset, right_offset = (-50, 0), (50, 0)

    else:
        left_offset, right_offset = (-30, 0), (30, 0)

    lx, ly = _rotate_offset(left_offset, angle)
    rx, ry = _rotate_offset(right_offset, angle)

    return (x + lx, y + ly), (x + rx, y + ry)


def _rotate_offset(offset, angle):
    """
    v0.4.0 - rotates a (dx, dy) offset around the origin in 90-degree
    steps, matching the direction pygame.transform.rotate() spins the
    drawn symbol, so terminals stay lined up with the artwork.
    """
    dx, dy = offset
    if angle == 90:
        return dy, -dx
    if angle == 180:
        return -dx, -dy
    if angle == 270:
        return -dy, dx
    return dx, dy


# v0.4.0 - component rotation
# Each draw_obj() function only knows how to draw horizontally, so to
# rotate we draw onto a small local surface first and let pygame rotate
# the surface itself - the draw_xxx() functions above stay untouched.
COMPONENT_DRAW_FUNCS = {
    "Resistor": draw_resistor,
    "Battery": draw_battery,
    "Capacitor": draw_capacitor,
    "Inductor": draw_inductor,
}

COMPONENT_SURFACE_SIZE = (140, 80)


def draw_component_rotated(screen, component, x, y, angle=0):
    """
    Draws `component` centered at (x, y), rotated by `angle` degrees
    (0/90/180/270). Returns True if it drew something, False if
    `component` isn't a known type (caller can fall back to its own
    drawing for custom parts).
    """
    draw_fn = COMPONENT_DRAW_FUNCS.get(component)
    if draw_fn is None:
        return False

    angle = int(angle) % 360

    local_surface = pygame.Surface(COMPONENT_SURFACE_SIZE, pygame.SRCALPHA)
    cx, cy = COMPONENT_SURFACE_SIZE[0] // 2, COMPONENT_SURFACE_SIZE[1] // 2
    draw_fn(local_surface, cx, cy)

    rotated = pygame.transform.rotate(local_surface, angle) if angle else local_surface
    rect = rotated.get_rect(center=(x, y))
    screen.blit(rotated, rect)
    return True
