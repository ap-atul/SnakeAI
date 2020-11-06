from curses import KEY_UP, KEY_DOWN, KEY_RIGHT, KEY_LEFT
from random import randint

from constant import *


class Body(object):
    def __init__(self, x, y, char=BODY_CHAR):
        self.x = x
        self.y = y
        self.char = char

    @property
    def position(self):
        return self.x, self.y


class Food(object):
    def __init__(self, window, snake, char=FOOD_CHAR):
        self.x = randint(10, MAX_X - 10)
        self.y = randint(10, MAX_Y - 10)
        self.char = char
        self.window = window
        self.snake = snake

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

    def reset(self):
        self.x = randint(10, MAX_X - 10)
        self.y = randint(10, MAX_Y - 10)

        if self.collides():
            self.reset()

    def collides(self):
        return any([body.position == (self.x, self.y) for body in self.snake.body[: -1]])


class Snake(object):
    def __init__(self, x, y, window):
        self.window = window
        self.body = list()
        self.score = 0
        self.headCharacter = HEAD_CHAR
        self.timeout = TIMEOUT

        for i in range(SNAKE_LEN, 0, -1):
            self.body.append(Body(x, y))

        self.body.append(Body(x, y, self.headCharacter))
        self.direction = KEY_RIGHT
        self.last = (x, y)

        self.move = {
            KEY_UP: self.moveUp,
            KEY_DOWN: self.moveDown,
            KEY_LEFT: self.moveLeft,
            KEY_RIGHT: self.moveRight
        }

        self.invalid = {
            KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP,
            KEY_LEFT: KEY_RIGHT,
            KEY_RIGHT: KEY_LEFT
        }

    @property
    def getScore(self):
        return "Score : " + str(self.score)

    def eatFood(self, food: Food):
        food.reset()
        body = Body(self.last[0], self.last[1])
        self.body.insert(-1, body)
        self.score += 1

        if self.score % 3 == 0:
            if self.timeout > 20:
                self.timeout -= 5
            self.window.timeout(self.timeout)

    @property
    def head(self):
        return self.body[-1]

    def collided(self):
        return any([body.position == self.head.position for body in self.body[: -1]])

    def update(self):
        last = self.body.pop(0)
        last.x = self.body[-1].x
        last.y = self.body[-1].y

        self.body.insert(-1, last)
        self.last = (self.head.x, self.head.y)
        self.move[self.direction]()

    def makeMove(self, direction):
        # if key and current directions opposite, don't react
        if direction != self.invalid[self.direction]:
            self.direction = direction

    def render(self):
        for body in self.body:
            self.window.addstr(body.y, body.x, body.char)

    def moveUp(self):
        self.head.y -= 1

        if self.head.y < 1:
            self.head.y = MAX_Y

    def moveDown(self):
        self.head.y += 1

        if self.head.y > MAX_Y:
            self.head.y = 1

    def moveLeft(self):
        self.head.x -= 1

        if self.head.x < 1:
            self.head.x = MAX_X

    def moveRight(self):
        self.head.x += 1

        if self.head.x > MAX_X:
            self.head.x = 1
