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


def get_terminals(component, x, y):

    if component == "Resistor":

        return (
            (x - 40, y),    # left terminal
            (x + 40, y)     # right terminal
        )

    elif component == "Battery":

        return (
            (x - 30, y),
            (x + 30, y)
        )

    elif component == "Capacitor":

        return (
            (x - 30, y),
            (x + 30, y)
        )

    elif component == "Inductor":

        return (
            (x - 50, y),
            (x + 50, y))