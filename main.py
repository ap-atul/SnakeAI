import curses

from components import *


def startGame():
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

        if event in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            snake.makeMove(event)

        if snake.head.x == food.x and snake.head.y == food.y:
            snake.eatFood(food)

        snake.update()
        if snake.collided():
            break

    curses.endwin()


if __name__ == "__main__":
    startGame()
