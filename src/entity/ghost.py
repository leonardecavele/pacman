from math import sqrt
import heapq

from .pac_man import Pac_man
from .entity import Entity

from src.type import vec2
from src.maze import Maze


class Ghost(Entity):
    def __init__(
        self, screen_pos: vec2, maze_pos: vec2,
        sprite: str, m: Maze, pac_man: Pac_man
    ) -> None:
        super().__init__(screen_pos, maze_pos, sprite, m)
        self.scatter: bool = False
        self.directions: list[vec2]
        self.pac_man: Pac_man = pac_man

    def a_star(self, target: vec2) -> list[vec2]:
        counter: int = 0

        def push(
            queue: list[tuple[int, int, Maze.Cell]],
            new_cell: Maze.Cell, score: int
        ) -> None:
            nonlocal counter
            heapq.heappush(queue, (score, counter, new_cell))
            counter += 1

        back = Maze.Direction((-self.direction[0], -self.direction[1]))

        visited: set[vec2] = set()
        parent: dict[vec2, vec2] = {}

        queue: list[tuple[int, int, Maze.Cell]] = []
        g: dict[vec2, int] = {}
        h: dict[vec2, int] = {}

        goal_x, goal_y = target
        goal: Maze.Cell = self.maze.maze[goal_y][goal_x]

        start_x, start_y = self.maze_pos
        g[(start_x, start_y)] = 0
        h[(start_x, start_y)] = self.manhattan(self.maze_pos, target)
        push(
            queue,
            self.maze.maze[start_y][start_x],
            g[(start_x, start_y)] + h[(start_x, start_y)]
        )

        path: list[vec2] = []

        while queue:
            _, _, current = heapq.heappop(queue)
            x, y = current.pos
            if current == goal:
                while current.pos != (start_x, start_y):
                    parent_x, parent_y = parent[current.pos]
                    dx = current.pos[0] - parent_x
                    dy = current.pos[1] - parent_y
                    path.append((dx, dy))
                    current = self.maze.maze[parent_y][parent_x]

                path.reverse()
                break

            if (x, y) in visited:
                continue

            visited.add((x, y))

            for direction in Maze.Direction:
                # cannot go back
                if (x, y) == (start_x, start_y) and direction == back:
                    continue

                # blocked by wall
                if self.maze.maze[y][x] & Maze.convert(direction):
                    continue

                # visited
                new_x, new_y = (x + direction.value[0], y + direction.value[1])
                if (new_x, new_y) in visited:
                    continue

                new_g: int = g[(x, y)] + 1
                if (new_x, new_y) not in g or new_g < g[(new_x, new_y)]:
                    parent[(new_x, new_y)] = (x, y)
                    g[(new_x, new_y)] = new_g
                    h[(new_x, new_y)] = self.manhattan((new_x, new_y), target)
                    push(
                        queue,
                        self.maze.maze[new_y][new_x],
                        new_g + h[(new_x, new_y)]
                    )
        return path

    def on_intersection(self) -> bool:
        x, y = self.maze_pos
        cell = self.maze.maze[y][x]
        back = Maze.Direction((-self.direction[0], -self.direction[1]))

        count = 0
        for wall in Maze.Cell.Walls:
            if not (cell.value & wall.value) and Maze.convert(wall) != back:
                count += 1

        return count >= 2

    @staticmethod
    def euclidean(pos1: vec2, pos2: vec2) -> int:
        dx: int = pos2[0] - pos1[0]
        dy: int = pos2[1] - pos1[1]
        return int(sqrt(dx * dx + dy * dy))

    @staticmethod
    def manhattan(pos1: vec2, pos2: vec2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Blinky(Ghost):
    def __init__(
        self, screen_pos: vec2, maze_pos: vec2,
        sprite: str, m: Maze, pac_man: Pac_man
    ) -> None:
        super().__init__(screen_pos, maze_pos, sprite, m, pac_man)
        self.angry: bool = False

    def update(self) -> None:
        if not self.on_intersection():
            return


class Inky(Ghost):
    def update(self) -> None:
        if not self.on_intersection():
            return


class Pinky(Ghost):
    def update(self) -> None:
        if not self.on_intersection():
            return


class Clyde(Ghost):
    def update(self) -> None:
        if not self.on_intersection():
            return
        direction: vec2
        # DIRECTION CANNOT BE BACK
        # choisir a partir de intersec + 1

        # on update flush direction list with pops and every intersection clear
        # it and recompute new path, if empty recompute one
        # list is directions
        if self.euclidean(self.maze_pos, self.pac_man.maze_pos) <= 8:
            direction = self.a_star((self.maze.height, 0))
        else:
            direction = self.a_star(self.pac_man.maze_pos)
        self.direction = direction
