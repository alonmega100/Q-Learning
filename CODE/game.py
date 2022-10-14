import time
import pygame

SQUARES = {
    (0, 0): (50, 50),
    (1, 0): (250, 50),
    (0, 1): (50, 250),
    (0, 2): (50, 450),
    (1, 1): (250, 250),
    (2, 0): (450, 50),
    (3, 0): (650, 50),
    (2, 1): (450, 250),
    (1, 2): (250, 450),
    (2, 2): (450, 450),
    (3, 1): (650, 250),
    (4, 0): (850, 50),
    (4, 1): (850, 250),
    (3, 2): (650, 450),
    (4, 2): (850, 450),
    }


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

        self.map_squares = [[None for y in range(3)] for x in range(5)]

    def create_units(self):
        mario = Ally()
        bowser = Enemy()
        coopa_troopa = Enemy()
        goomba = Enemy()
        coin = Reward()

        mario.set_image("../DATA/mario.png")
        bowser.set_image("../DATA/Enemies/Bowser.png")
        coopa_troopa.set_image("../DATA/Enemies/Koopa_Troopa.png")
        goomba.set_image("../DATA/Enemies/Goomba.png")
        coin.set_image("../DATA/coin.png")

        mario.set_square((0, 0))
        bowser.set_square((4, 1))
        coin.set_square((4, 2))
        coopa_troopa.set_square((1, 2))
        goomba.set_square((2, 0))

        self.map_squares[0][0] = mario
        self.map_squares[4][1] = bowser
        self.map_squares[4][2] = coin
        self.map_squares[1][2] = coopa_troopa
        self.map_squares[2][0] = goomba

        self.units.append(mario)
        self.units.append(bowser)
        self.units.append(coopa_troopa)
        self.units.append(goomba)
        self.units.append(coin)

        return mario

    def run(self):
        pygame.init()
        mario = self.create_units()
        self.load_image(self.FILE)
        while self.running:
            self.screen.blit(self.image, self.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        temp = mario.get_square()
                        if temp[1] != 2:
                            new_square = (temp[0], temp[1]+1)
                            if type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Enemy":
                                self.running = False
                            elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Reward":
                                self.score += 3
                                print("Horray!!")
                            mario.set_square(new_square)
                    elif event.key == pygame.K_RIGHT:
                        temp = mario.get_square()
                        if temp[0] != 4:
                            new_square = (temp[0]+1, temp[1])
                            if type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Enemy":
                                self.running = False
                            elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Reward":
                                self.score += 3
                                print("Horray!!")
                            mario.set_square(new_square)
                    elif event.key == pygame.K_UP:
                        temp = mario.get_square()
                        if temp[1] != 0:
                            new_square = (temp[0], temp[1]-1)
                            if type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Enemy":
                                self.running = False
                            elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Reward":
                                self.score += 3
                                print("Horray!!")
                            mario.set_square(new_square)
                    elif event.key == pygame.K_LEFT:
                        temp = mario.get_square()
                        if temp[0] != 0:
                            new_square = (temp[0]-1, temp[1])
                            if type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Enemy":
                                self.running = False
                            elif type(self.map_squares[new_square[0]][new_square[1]]).__name__ == "Reward":
                                self.score += 3
                                print("Horray!!")
                            mario.set_square(new_square)

            for units in self.units:
                units.draw(self.screen)
            pygame.display.update()
        pygame.quit()

    def load_image(self, file):
        self.FILE = file
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)
        pygame.display.set_caption(f'size:{self.rect.size}')


class Unit:
    def __init__(self):
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
            self.position = SQUARES[self.square]


class Ally(Unit):
    def __init__(self):
        Unit.__init__(self)


class Enemy(Unit):
    def __init__(self):
        Unit.__init__(self)


class Reward(Unit):
    def __init__(self):
        Unit.__init__(self)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()



