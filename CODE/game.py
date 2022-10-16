import random
import time
import pygame
import numpy as np
import pandas as pd

SQUARES = {
    (0, 0): ((50, 50), 0),
    (1, 0): ((250, 50), 1),
    (0, 1): ((50, 250), 2),
    (0, 2): ((50, 450), 3),
    (1, 1): ((250, 250), 4),
    (2, 0): ((450, 50), 5),
    (3, 0): ((650, 50), 6),
    (2, 1): ((450, 250), 7),
    (1, 2): ((250, 450), 8),
    (2, 2): ((450, 450), 9),
    (3, 1): ((650, 250), 10),
    (4, 0): ((850, 50), 11),
    (4, 1): ((850, 250), 12),
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


class Game:

    W = 1000
    H = 600
    FILE = "../DATA/Background/Tiling-Grass-Texture-Main.jpg"

    SIZE = (W, H)

    def __init__(self):
        self.image = None
        self.rect = None
        self.units = []
        self.screen = pygame.display.set_mode(Game.SIZE)
        pygame.display.set_caption("Mario 2d World")
        self.running = True
        self.score = 0
        self.board_size = (5, 3)
        self.map_squares = [[None for y in range(self.board_size[1])] for x in range(self.board_size[0])]

        self.agent = Agent()

    def create_units(self):
        mario = Ally()
        bowser = Enemy()
        coopa_troopa = Enemy()
        goomba = Enemy()
        coin1 = Reward()
        coin2 = Reward()
        coin3 = Reward()
        coin4 = Reward()
        pipe = Exit()

        mario.set_image("../DATA/mario.png")
        bowser.set_image("../DATA/Enemies/Bowser.png")
        coopa_troopa.set_image("../DATA/Enemies/Koopa_Troopa.png")
        goomba.set_image("../DATA/Enemies/Goomba.png")
        coin1.set_image("../DATA/coin.png")
        coin2.set_image("../DATA/coin.png")
        coin3.set_image("../DATA/coin.png")
        coin4.set_image("../DATA/coin.png")
        pipe.set_image("../DATA/pipe.png")

        mario.set_square((0, 0))
        bowser.set_square((3, 1))
        coopa_troopa.set_square((1, 1))
        goomba.set_square((3, 0))
        coin1.set_square((0, 2))
        coin2.set_square((2, 0))
        coin3.set_square((2, 2))
        coin4.set_square((4, 2))
        pipe.set_square((4, 0))

        self.map_squares[mario.get_square()[0]][mario.get_square()[1]] = mario
        self.map_squares[bowser.get_square()[0]][bowser.get_square()[1]] = bowser
        self.map_squares[coopa_troopa.get_square()[0]][coopa_troopa.get_square()[1]] = coopa_troopa
        self.map_squares[goomba.get_square()[0]][goomba.get_square()[1]] = goomba
        self.map_squares[coin1.get_square()[0]][coin1.get_square()[1]] = coin1
        self.map_squares[coin2.get_square()[0]][coin2.get_square()[1]] = coin2
        self.map_squares[coin3.get_square()[0]][coin3.get_square()[1]] = coin3
        self.map_squares[coin4.get_square()[0]][coin4.get_square()[1]] = coin4
        self.map_squares[pipe.get_square()[0]][pipe.get_square()[1]] = pipe

        self.units.append(mario)
        self.units.append(bowser)
        self.units.append(coopa_troopa)
        self.units.append(goomba)
        self.units.append(coin1)
        self.units.append(coin2)
        self.units.append(coin3)
        self.units.append(coin4)
        self.units.append(pipe)

        return mario

    def run(self):
        pygame.init()
        mario = self.create_units()
        self.load_image(self.FILE)
        clock = pygame.time.Clock()
        first_run = True
        while self.running:
            log_path = []
            self.screen.blit(self.image, self.rect)
            self.agent.set_square(mario.get_square())
            if first_run:
                first_run = False
            else:
                pygame.event.post(pygame.event.Event(self.agent.take_action()))
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == AGENT_UP or event.type == AGENT_DOWN or event.type == AGENT_RIGHT \
                        or event.type == AGENT_LEFT or event.type == pygame.KEYDOWN:
                    current_square = mario.get_square()
                    new_square = mario.get_square()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            temp = mario.get_square()
                            if temp[1] != 2:
                                new_square = (temp[0], temp[1]+1)
                                mario.set_square(new_square)
                        elif event.key == pygame.K_RIGHT:
                            temp = mario.get_square()
                            if temp[0] != 4:
                                new_square = (temp[0]+1, temp[1])
                                mario.set_square(new_square)
                        elif event.key == pygame.K_UP:
                            temp = mario.get_square()
                            if temp[1] != 0:
                                new_square = (temp[0], temp[1]-1)
                                mario.set_square(new_square)
                        elif event.key == pygame.K_LEFT:
                            temp = mario.get_square()
                            if temp[0] != 0:
                                new_square = (temp[0]-1, temp[1])
                                mario.set_square(new_square)

                    elif event.type == AGENT_RIGHT:
                        log_path.append(current_square)
                        log_path.append(2)
                        if current_square[0] != 4:
                            new_square = (current_square[0] + 1, current_square[1])

                    elif event.type == AGENT_LEFT:
                        log_path.append(mario.get_square())
                        log_path.append(3)
                        if current_square[0] != 0:
                            new_square = (current_square[0] - 1, current_square[1])

                    elif event.type == AGENT_UP:
                        log_path.append(mario.get_square())
                        log_path.append(0)
                        if current_square[1] != 0:
                            new_square = (current_square[0], current_square[1] - 1)

                    elif event.type == AGENT_DOWN:
                        log_path.append(mario.get_square())
                        log_path.append(1)
                        if current_square[1] != 2:
                            new_square = (current_square[0], current_square[1] + 1)

                    if new_square == (4, 1):
                        print("Alon is ge")
                    if new_square != current_square:
                        mario.set_square(new_square)
                        if type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Exit":
                            log_path.append(self.map_squares[new_square[0]][new_square[1]].get_value())
                            self.units = list()
                            mario = self.create_units()
                            self.agent.update(log_path)
                            first_run = True
                            print("Its a W")

                        elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Enemy":
                            log_path.append(self.map_squares[new_square[0]][new_square[1]].get_value())

                            self.units = list()
                            mario = self.create_units()
                            self.agent.update(log_path)
                            first_run = True

                        elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Reward":
                            log_path.append(self.map_squares[new_square[0]][new_square[1]].get_value())
                            self.map_squares[new_square[0]][new_square[1]] = None
                            self.agent.update(log_path)
                        else:  # New square is a black space
                            log_path.append(-1)
                            self.agent.update(log_path)

                    else:  # Agent bumped into the wall
                        mario.set_square(new_square)
                        log_path.append(-2)
                        self.agent.update(log_path)

            for y in range(self.board_size[1]):
                for x in range(self.board_size[0]):
                    if self.map_squares[x][y] is None:
                        pass
                    else:
                        self.map_squares[x][y].draw(self.screen)
            pygame.display.update()
            pygame.event.clear()
            clock.tick(100)

        # df = pd.DataFrame(self.agent.q_table, columns=["Up", "Down", "Right", "Left"])
        # df.index = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]
        self.agent.q_table.to_json('../DATA/trained-model.json')
        print(self.agent.q_table)
        pygame.quit()

    def load_image(self, file):
        self.FILE = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')


class Agent:
    def __init__(self):
        self.q_table = np.zeros((15, 4), dtype=float)
        df = pd.DataFrame(self.q_table, columns=["Up", "Down", "Right", "Left"], dtype=float)
        df.index = ["(0, 0)", "(1, 0)", "(2, 0)", "(3, 0)", "(4, 0)", "(0, 1)", "(1, 1)", "(2, 1)", "(3, 1)", "(4, 1)", "(0, 2)", "(1, 2)", "(2, 2)", "(3, 2)", "(4, 2)"]

        self.q_table = df
        try:
            self.q_table = pd.read_json('../DATA/trained-model.json', dtype=float)
        except FileNotFoundError as error:
            print(error)
        # self.q_table = pd.DataFrame(np.zeros((15, 4)))
        # self.q_table.columns = ["Up", "Down", "Right", "Left"]
        # self.q_table.index = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2),
        #             (2, 2), (3, 2), (4, 2)]
        self.square = None
        self.last_reward = 0
        self.score = 0
        self.last_action = 0
        self.last_state = None

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
        while len(log_path) != 0:

            square = log_path[0]
            action = log_path[1]
            reward = log_path[2]
            action = DIRECTIONS[action]

            for i in range(3, len(log_path), 3):
                # temp_q_value = self.q_table.loc[SQUARES[square][1]][action].copy()
                current_q_value = float(self.q_table.loc[str(square)][str(action)])
                self.q_table.loc[str(square)][str(action)] = float(current_q_value + 1*(reward + (0.5**i)*(np.max(self.q_table.loc[str(log_path[i])])) - current_q_value))
            log_path = log_path[3:]

    # AGENT_RIGHT = pygame.USEREVENT + 1
    # AGENT_UP = pygame.USEREVENT + 2
    # AGENT_DOWN = pygame.USEREVENT + 3
    # AGENT_LEFT = pygame.USEREVENT + 4


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
        self.value = 10000


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()



