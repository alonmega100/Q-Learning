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


class Agent:
    def __init__(self):
        self.q_table = np.zeros((15, 4), dtype=float)
        self.q_table = pd.DataFrame(self.q_table, columns=["Up", "Down", "Right", "Left"], dtype=float)
        print(self.q_table)
        self.square = None

    def set_square(self, square):
        self.square = square

    def reset(self):
        self.score = 0
        self.square = (0, 0)

    def take_action(self):
        eps = 0.1
        p = np.random.random()
        actions = [AGENT_UP, AGENT_DOWN, AGENT_RIGHT, AGENT_LEFT]

        if p < eps:
            j = np.random.choice(4)
        else:
            row_number = SQUARES[self.square][1]
            j = self.q_table.iloc[row_number].argmax()
        return actions[j]

    def update(self, log_path):
        print(log_path)
        for i in range(len(log_path)):
            o_state, o_action, o_reward = log_path[i]
            o_state_index = SQUARES[o_state][1]
            counter = 1
            for j in range(i, len(log_path)):
                t_state, t_action, t_reward = log_path[j]
                t_state_index = SQUARES[t_state][1]
                o_value = self.q_table.iloc[o_state_index][o_action]
                self.q_table.iloc[o_state_index][o_action] = o_value + 0.1*(o_reward + (0.1 ** counter) * np.max(self.q_table.iloc[t_state_index]) - o_value)
                counter += 1
