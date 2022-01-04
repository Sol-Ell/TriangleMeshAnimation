import pygame, math
from pygame import *
from math import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
PLANET_WIDTH = 20
PLANET_HEIGHT = 20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
SPACE_COLOR = "#000022"
SUN_COLOR = "yellow"
PLANET_COLOR = "blue"

# Sun position
X0 = WIN_WIDTH // 2
Y0 = WIN_HEIGHT // 2
# Sun mass
M0 = 0.001
# Stop conditions
CRASH_DIST = 10
OUT_DIST = 1000


def main():
    global X0, Y0
    # PyGame init
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Solar Mechanics v0.1")

    # Space init
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(SPACE_COLOR))

    # Timer init
    timer = pygame.time.Clock()

    # Planet init
    planet = Surface((PLANET_WIDTH, PLANET_HEIGHT))
    planet.fill(Color(SPACE_COLOR))
    draw.circle(planet,
                Color(PLANET_COLOR),
                (PLANET_WIDTH // 2, PLANET_HEIGHT // 2),
                5)

    # Planet to Sun distance
    r = 0.0
    # Initial planet pos, speed and accel
    x = 100.0
    y = 290.0
    vx = 0.1
    vy = 1.5

    done = False
    while not done:
        timer.tick(50)
        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
                break
        m = mouse.get_pos()
        if m[0] != 0:
            X0 = m[0]
            Y0 = m[1]

        r = sqrt((x - X0) ** 2 + (y - Y0) ** 2)

        # New speed based on accel
        vx += M0 * (X0 - x) / r ** 2
        vy += M0 * (Y0 - y) / r ** 2

        # New pos based on speed
        x += vx
        y += vy

        screen.blit(bg, (0, 0))
        screen.blit(planet, (int(x), int(y)))
        draw.circle(screen, Color(SUN_COLOR), [X0, Y0], 10)
        pygame.display.update()

        if r < CRASH_DIST:
            done = True
            print("Crashed")
            break
        if r > OUT_DIST:
            done = True
            print("Out of system")
            break

    # Farewell
    print(":-)")


if __name__ == "__main__":
    main()