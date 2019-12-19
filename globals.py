import pygame


def point_in_rect(x, y, rect):
    return x >= rect[0] and x <= rect[0] + rect[2] and y >= rect[1] and y <= rect[1] + rect[3]


def rects_collide(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))
