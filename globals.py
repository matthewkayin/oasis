import pygame
import math


def point_in_rect(x, y, rect):
    return x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]


def point_distance(a, b):
    return math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2))


def rects_collide(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
