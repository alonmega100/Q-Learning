import random
import time
import pygame
import numpy as np
import pandas as pd


SQUARES = {
    (0, 0): ((50, 50), 0),
    (1, 0): ((250, 50), 1),
    (2, 0): ((450, 50), 2),
    (3, 0): ((650, 50), 3),
    (4, 0): ((850, 50), 4),
    (0, 1): ((50, 250), 5),
    (1, 1): ((250, 250), 6),
    (2, 1): ((450, 250), 7),
    (3, 1): ((650, 250), 8),
    (4, 1): ((850, 250), 9),
    (0, 2): ((50, 450), 10),
    (1, 2): ((250, 450), 11),
    (2, 2): ((450, 450), 12),
    (3, 2): ((650, 450), 13),
    (4, 2): ((850, 450), 14),
    }

DIRECTIONS = {
    0: "Up",
    1: "Down",
    2: "Right",
    3: "Left"
}
AGENT_RIGHT = pygame.USEREVENT + 1
AGENT_UP = pygame.USEREVENT + 2
AGENT_DOWN = pygame.USEREVENT + 3
AGENT_LEFT = pygame.USEREVENT + 4


class Unit:
    def __init__(self):
        self.value = 0
        self.square = (0, 0)
        self.position = (0, 0)
        self.type = None
        self.image_path = None
        self.image = None

    def set_image(self, path):
        self.image_path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (100, 100))

    def move(self, new_position):
        self.position = new_position

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def set_square(self, square):
        self.square = square
        self.set_position()

    def get_square(self):
        return self.square

    def set_position(self, position=None):
        if position is not None:
            self.position = position

        else:
            self.position = SQUARES[self.square][0]

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class Ally(Unit):
    def __init__(self):
        Unit.__init__(self)


class Enemy(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.value = -1000


class Reward(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.value = 5


class Exit(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.value = 99999999