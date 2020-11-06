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

        self.moves = 0

    def sortDictionary(self, x):
        return {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}

    def collides(self, headPosition, snake):
        return any([body.position == headPosition for body in snake.body[: -1]])

    def getDistances(self, goal, current, snake):
        distances = dict()
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

            distances[path] = self.moves + abs(x - goal_x) + abs(y - goal_y)

        return distances

    def getKey(self, food, snake):
        if snake.head.x == food.x and snake.head.y:
            self.moves = 0
            return snake.direction

        distances = self.getDistances(food, snake.head, snake)
        distances = self.sortDictionary(distances)
        distances = list(distances.keys())

        return distances[0]
