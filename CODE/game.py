import runner

from agent import Agent
from Unit import *


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
        self.map_squares = [[None for _ in range(self.board_size[1])] for _ in range(self.board_size[0])]

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

        mario.set_square((0, 2))
        bowser.set_square((3, 2))
        coopa_troopa.set_square((1, 1))
        goomba.set_square((3, 0))
        coin1.set_square((0, 0))
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
        log_path = []
        number_of_tries = 1
        wins = 0
        while self.running:
            if len(log_path) > 10:
                log_path = log_path[1:]
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
                        or event.type == AGENT_LEFT:
                    state = mario.get_square()
                    new_square = mario.get_square()
                    if event.type == AGENT_UP:
                        action = 0
                        if state[1] != 0:
                            new_square = (state[0], state[1] - 1)

                    elif event.type == AGENT_DOWN:
                        action = 1
                        if state[1] != 2:
                            new_square = (state[0], state[1] + 1)

                    elif event.type == AGENT_RIGHT:
                        action = 2
                        if state[0] != 4:
                            new_square = (state[0] + 1, state[1])

                    else:  # event.type == AGENT_LEFT:
                        action = 3
                        if state[0] != 0:
                            new_square = (state[0] - 1, state[1])
                    needs_reset = False

                    if new_square != state:
                        mario.set_square(new_square)
                        landed_object = self.map_squares[new_square[0]][new_square[1]]
                        if type(landed_object).__name__ == "Exit":
                            reward = landed_object.get_value()
                            needs_reset = True
                            wins += 1

                        elif type(landed_object).__name__ == "Enemy":
                            reward = landed_object.get_value()
                            needs_reset = True

                        elif type(landed_object).__name__ == "Reward":
                            reward = landed_object.get_value()
                            self.map_squares[new_square[0]][new_square[1]] = None
                        else:  # New square is a black space
                            reward = -1

                    else:  # Agent bumped into the wall
                        reward = -2

                    log_path.append((state, action, reward))
                    self.agent.update(log_path)
                    if needs_reset:
                        self.units = []
                        mario = self.create_units()
                        log_path = []
                        first_run = True
                        number_of_tries += 1

            for y in range(self.board_size[1]):
                for x in range(self.board_size[0]):
                    if self.map_squares[x][y] is None:
                        pass
                    else:
                        self.map_squares[x][y].draw(self.screen)
            pygame.display.update()
            pygame.event.clear()
            clock.tick(100)

        self.agent.q_table.to_json('../DATA/trained-model.json')
        print(self.agent.q_table)
        print("Number of trys:", number_of_tries)
        print("Number of Wins:", wins)
        pygame.quit()

    def load_image(self, file):
        self.FILE = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')


def main():
    runner.main()


if __name__ == '__main__':
    main()
