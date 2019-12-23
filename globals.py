import pygame
import math


def point_in_rect(x, y, rect):
    return x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]


def rect_in_screen(rect):
    screen = (0, 0, 1280, 720)
    return point_in_rect(rect[0], rect[1], screen) or point_in_rect(rect[0] + rect[2], rect[1], screen) or point_in_rect(rect[0] + rect[2], rect[1] + rect[3], screen) or point_in_rect(rect[0], rect[1] + rect[3], screen)


def point_distance(a, b):
    return math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2))


def get_center(rect):
    return (rect[0] + (rect[2] / 2), rect[1] + (rect[3] / 2))


def scale_vector(old_vector, new_magnitude):
    old_magnitude = math.sqrt((old_vector[0] ** 2) + (old_vector[1] ** 2))
    if old_magnitude == 0:
        return (0, 0)
    scale = new_magnitude / old_magnitude
    new_x = old_vector[0] * scale
    new_y = old_vector[1] * scale
    return (new_x, new_y)


def rects_collide(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
