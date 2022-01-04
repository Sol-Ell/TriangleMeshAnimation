import pygame as pg
from random import choice
from math import sqrt

LINE_COLOR_R = 75
LINE_COLOR_G = 39
LINE_COLOR_B = 186


class MeshAnimation:
    def __init__(self):
        self.screen = pg.display.set_mode((600, 600))  # , pg.FULLSCREEN)
        self.SCREEN_WIDTH = self.screen.get_width()
        self.SCREEN_HEIGHT = self.screen.get_height()
        self.net_width = 10
        self.net_height = 10
        self.mouse_radius = 20
        self.net = Net(self.net_width, self.net_height,
                       (self.SCREEN_WIDTH - 50, self.SCREEN_HEIGHT - 50), 50, 50)
        self.clock = pg.time.Clock()

    def loop(self):
        while True:
            self.screen.fill((17, 32, 46))  # (36, 53, 107)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.mouse_radius = min(self.mouse_radius + 1, 50)
                    if event.button == 5:
                        self.mouse_radius = max(self.mouse_radius - 1, 10)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        pg.quit()
                        quit()

            self.net.draw(self.screen)
            m_pos = pg.mouse.get_pos()
            if pg.mouse.get_pressed(3)[0]:
                pg.draw.circle(self.screen, (255, 0, 0), m_pos, self.mouse_radius, 1)
                self.net.update(m_pos, self.mouse_radius)
            else:
                pg.draw.circle(self.screen, (0, 255, 0), m_pos, self.mouse_radius, 1)
                self.net.update()

            pg.display.flip()
            self.clock.tick(50)


class Net:
    def __init__(self, column_size, row_size, size, margin_left=0, margin_top=0):
        self.size = size
        self.points = []
        self.column_size = column_size
        self.row_size = row_size
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.point_padding_left = size[0] / self.column_size
        self.point_padding_top = size[1] / self.row_size
        for row in range(self.row_size):
            self.points.append([])
            for column in range(self.column_size):
                self.points[row].append(Point(
                    margin_left + column * self.point_padding_left + (row % 2 * self.point_padding_left / 2),
                    margin_top + row * self.point_padding_top
                ))

        for row in range(self.row_size):
            for column in range(self.column_size):
                point = self.points[row][column]
                if row == 0:
                    continue
                point.p.append(self.points[row][column - 1])
                if column > 0:
                    if row % 2:
                        point.p.append(self.points[row - 1][column])
                    else:
                        point.p.append(self.points[row - 1][column - 1])
                        point.p1.append(self.points[row - 1][column - 1])
                point.p1.append(self.points[row - 1][column])
                if row % 2:
                    if column < self.column_size - 1:
                        point.p1.append(self.points[row - 1][column + 1])

    def draw(self, screen):
        for row in self.points:
            for point in row:
                point.draw_polygon(screen)

        for row in self.points:
            for point in row:
                point.draw_circle(screen)

    def update(self, m_pos=(), mouse_radius=0):
        if m_pos:
            for row in self.points:
                for p in row:
                    p.update()
        else:
            for row in self.points:
                for p in row:
                    p.update(m_pos, mouse_radius)


class Point:
    def __init__(self, x0, y0):
        o = choice([10, 8, 6])
        self.x = x0 + o
        self.y = y0 + o
        self.r = 1
        self.x0 = x0
        self.y0 = y0
        self.vx = 0
        self.vy = 1
        self.m = 1
        self.p = []
        self.p1 = []

    def draw_polygon(self, screen):
        if len(self.p) > 1:
            cords = [[self.x, self.y]]
            mr = self.r
            for point in self.p:
                cords.append([point.x, point.y])
                mr += point.r

            pg.draw.polygon(screen,
                            (norm(LINE_COLOR_R / mr * 10),
                             norm(LINE_COLOR_G / mr * 10),
                             norm(LINE_COLOR_B / mr * 10)),
                            cords)

        if len(self.p1) > 1:
            cords = [[self.x, self.y]]
            mr = self.r
            for point in self.p1:
                cords.append([point.x, point.y])
                mr += point.r

            pg.draw.polygon(screen,
                            (norm(LINE_COLOR_R / mr * 10),
                             norm(LINE_COLOR_G / mr * 10),
                             norm(LINE_COLOR_B / mr * 10)),
                            cords)

    def draw_circle(self, screen):
        pg.draw.circle(screen, (123, 50, 179), [self.x, self.y], 2)

    def update(self, mouse_pos=(), mouse_radius=0):
        if mouse_pos:
            self.gravity_to_center(mouse_pos[0], mouse_pos[1], mouse_radius)
        else:
            self.gravity_to_center()

    def gravity_to_center(self, mouse_x=0, mouse_y=0, mouse_radius=0):
        k = 1
        if mouse_x == mouse_y == 0:
            m_x = mouse_x - self.x
            m_y = mouse_y - self.y

            m_r = sqrt(m_x * m_x + m_y * m_y)
            if m_r < mouse_radius:
                k = 1.5

        x = (self.x0 - self.x) * k
        y = (self.y0 - self.y) * k
        self.r = sqrt(x * x + y * y)

        if self.r < 1:
            o = choice([10, 8, 6])
            self.x = self.x0 + o
            self.y = self.y0 + o
            return

        self.vx += self.m * x / self.r ** 2
        self.vy += self.m * y / self.r ** 2
        self.x += self.vx
        self.y += self.vy


def norm(color):
    return min(max(0, color), 255)


if __name__ == '__main__':
    MeshAnimation().loop()
