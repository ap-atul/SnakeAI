import curses
import sys

from astar import AStar
from components import *


class StdOutWrapper:
    text = ""

    def write(self, txt):
        self.text += txt
        self.text += "\n"

    def get_text(self):
        return self.text


def startGame():
    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    curses.initscr()
    curses.beep()
    curses.beep()
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    snake = Snake(SNAKE_X, SNAKE_Y, window)
    food = Food(window)
    astar = AStar()

    while True:
        window.clear()
        window.border(0)

        # rendering the objects
        snake.render()
        food.render()

        window.addstr(0, 5, snake.getScore)
        event = window.getch()

        if event == 27:
            break

        if snake.head.x == food.x and snake.head.y == food.y:
            snake.eatFood(food)

        event = astar.getKey(food, snake)
        # print(event)

        if event in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            snake.makeMove(event)

        snake.update()
        if snake.collided():
            break

    curses.endwin()
    print(f"High score :: {snake.score}")

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdout.write(mystdout.get_text())


if __name__ == "__main__":
    startGame()
