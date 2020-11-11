from queue import PriorityQueue

from components import *


class AStar:
    """
     A star algorithm implementation
     f(n) = g(n) + h(n)
     """

    def __init__(self):
        self.paths = [
            KEY_RIGHT,
            KEY_LEFT,
            KEY_UP,
            KEY_DOWN
        ]
        self.invalid = {
            KEY_UP: KEY_DOWN,
            KEY_DOWN: KEY_UP,
            KEY_LEFT: KEY_RIGHT,
            KEY_RIGHT: KEY_LEFT
        }

        self.moves = 0

    def collides(self, headPosition, snake):
        """ Check for body collision on the next step """
        return any([body.position == headPosition for body in snake.body[: -1]])

    def getDistances(self, goal, current, snake):
        """ Finding distance for each path """
        distances = PriorityQueue()
        self.moves += 1

        for path in self.paths:
            x = None
            y = None
            goal_x = goal.x
            goal_y = goal.y

            if path is KEY_UP:
                x = current.x
                y = current.y - 1

            elif path is KEY_DOWN:
                x = current.x
                y = current.y + 1

            elif path is KEY_RIGHT:
                x = current.x + 1
                y = current.y

            elif path is KEY_LEFT:
                x = current.x - 1
                y = current.y

            if self.collides((x, y), snake):
                continue

            gn = self.moves
            hn = abs(x - goal_x) + abs(y - goal_y)
            fn = gn + hn

            # add to queue
            distances.put((fn, path))

        return distances

    def getKey(self, food, snake):
        """ Returns the next step """
        if snake.head.x == food.x and snake.head.y:
            self.moves = 0
            return snake.direction

        distances = self.getDistances(food, snake.head, snake)

        if distances.qsize() == 0:
            return snake.direction

        return distances.get()[1]
