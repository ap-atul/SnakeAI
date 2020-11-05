from components import *


class AStar:
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

    def getMoves(self, direction):
        paths = self.paths.copy()
        paths.remove(direction)
        return paths

    def getDistances(self, paths, goal, current):
        distances = dict()

        for path in paths:
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

            distances[path] = abs(x - goal_x) + abs(y - goal_y)

        return distances

    def sortDictionary(self, x):
        return {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}

    def getKey(self, food, snake):
        if snake.head.x == food.x and snake.head.y:
            return snake.direction

        currentDirection = snake.direction
        availablePaths = self.getMoves(currentDirection)

        distances = self.getDistances(availablePaths, food, snake.head)
        distances = self.sortDictionary(distances)

        return list(distances.keys())[0]
