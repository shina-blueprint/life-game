import random
import sys
import time
from math import floor

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT


class Cell:
    def __init__(self) -> None:
        self.current: bool = False
        self.previous: bool = False


WIDTH: int = 60
HEIGHT: int = 60
SIZE: int = 10

pygame.init()
SURFACE: pygame.Surface = pygame.display.set_mode((800, 600))
FPSCLOCK: pygame.time.Clock = pygame.time.Clock()

SYSFONT: pygame.font.Font = pygame.font.SysFont("None", 28)

RANDOM_RECT: pygame.Rect = pygame.Rect(615, 25, 170, 30)
CLEAR_RECT: pygame.Rect = pygame.Rect(615, 65, 170, 30)
PAUSE_RECT: pygame.Rect = pygame.Rect(615, 145, 170, 30)
X1_RECT: pygame.Rect = pygame.Rect(615, 185, 35, 30)
X2_RECT: pygame.Rect = pygame.Rect(660, 185, 35, 30)
X4_RECT: pygame.Rect = pygame.Rect(705, 185, 35, 30)
X8_RECT: pygame.Rect = pygame.Rect(750, 185, 35, 30)
STEP_RECT: pygame.Rect = pygame.Rect(615, 225, 170, 30)
SHOW_GRID_RECT: pygame.Rect = pygame.Rect(615, 305, 170, 30)


def random_fill(grid: list[list[Cell]]) -> None:
    for y in range(1, HEIGHT + 1):
        for x in range(1, WIDTH + 1):
            grid[y][x].current = bool(random.getrandbits(1))


def update(grid: list[list[Cell]]) -> None:
    for y in range(1, HEIGHT + 1):
        for x in range(1, WIDTH + 1):
            grid[y][x].previous = grid[y][x].current

    for y in range(1, HEIGHT + 1):
        for x in range(1, WIDTH + 1):
            c: bool = grid[y][x].previous

            n: int = 0
            n += grid[y - 1][x - 1].previous
            n += grid[y - 1][x].previous
            n += grid[y - 1][x + 1].previous
            n += grid[y][x - 1].previous
            n += grid[y][x + 1].previous
            n += grid[y + 1][x - 1].previous
            n += grid[y + 1][x].previous
            n += grid[y + 1][x + 1].previous

            grid[y][x].current = (c == False and n == 3) or (
                c == True and (n == 2 or n == 3)
            )


def blit_button(text: str, rect: pygame.Rect) -> None:
    pygame.draw.rect(SURFACE, (255, 255, 255), rect)
    render: pygame.Surface = SYSFONT.render(text, True, (0, 0, 0))
    SURFACE.blit(
        render, render.get_rect(center=(rect[0] + rect[2] / 2, rect[1] + rect[3] / 2))
    )


def main() -> None:
    grid: list[list[Cell]] = [
        [Cell() for _ in range(HEIGHT + 2)] for _ in range(WIDTH + 2)
    ]

    auto_step: bool = False

    speed: int = 1

    stepped: bool = False

    show_grid: bool = True

    start_time: float = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if 0 < event.pos[0] < 599 and 0 < event.pos[1] < 599:
                    xpos: int = floor(event.pos[0] / SIZE)
                    ypos: int = floor(event.pos[1] / SIZE)
                    grid[ypos + 1][xpos + 1].current = (
                        True if event.button == 1 else False
                    )

                if event.button == 1:
                    if RANDOM_RECT.collidepoint(event.pos):
                        random_fill(grid)

                    if CLEAR_RECT.collidepoint(event.pos):
                        grid = [
                            [Cell() for _ in range(HEIGHT + 2)]
                            for _ in range(WIDTH + 2)
                        ]

                    if PAUSE_RECT.collidepoint(event.pos):
                        auto_step = not auto_step

                    if STEP_RECT.collidepoint(event.pos):
                        stepped = True

                    if SHOW_GRID_RECT.collidepoint(event.pos):
                        show_grid = not show_grid

                    if X1_RECT.collidepoint(event.pos):
                        speed = 1

                    if X2_RECT.collidepoint(event.pos):
                        speed = 2

                    if X4_RECT.collidepoint(event.pos):
                        speed = 4

                    if X8_RECT.collidepoint(event.pos):
                        speed = 8

        SURFACE.fill((0, 0, 0))

        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                pygame.draw.rect(
                    SURFACE,
                    (255, 255, 255) if grid[ypos + 1][xpos + 1].current else (0, 0, 0),
                    (xpos * SIZE, ypos * SIZE, SIZE, SIZE),
                )

        if 0 < pygame.mouse.get_pos()[0] < 599 and 0 < pygame.mouse.get_pos()[1] < 599:
            xpos: int = floor(pygame.mouse.get_pos()[0] / SIZE)
            ypos: int = floor(pygame.mouse.get_pos()[1] / SIZE)
            pygame.draw.rect(
                SURFACE, (0, 255, 255), (xpos * SIZE, ypos * SIZE, SIZE, SIZE)
            )

        if show_grid:
            for index in range(0, (WIDTH + 1) * SIZE, SIZE):
                pygame.draw.line(
                    SURFACE, (0, 0, 255), (index, 0), (index, HEIGHT * SIZE)
                )
            for index in range(0, (HEIGHT + 1) * SIZE, SIZE):
                pygame.draw.line(
                    SURFACE, (0, 0, 255), (0, index), (WIDTH * SIZE, index)
                )

        blit_button("Random", RANDOM_RECT)

        blit_button("Clear", CLEAR_RECT)

        blit_button("Pause" if auto_step else "Run", PAUSE_RECT)

        blit_button("x 1", X1_RECT)

        blit_button("x 2", X2_RECT)

        blit_button("x 4", X4_RECT)

        blit_button("x 8", X8_RECT)

        blit_button("Step", STEP_RECT)

        blit_button("Grid OFF" if show_grid else "Grid ON", SHOW_GRID_RECT)

        if stepped or (auto_step and time.time() - start_time >= 1.0 / speed):
            update(grid)
            stepped = False
            start_time = time.time()

        pygame.display.update()
        FPSCLOCK.tick(30)


if __name__ == "__main__":
    main()
