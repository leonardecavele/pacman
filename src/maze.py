from enum import IntEnum

from mazegenerator import MazeGenerator

from src.type import brd


class Maze():
    def __init__(self, maze_generator: MazeGenerator, size: int) -> None:
        maze_generator.generate(size)
        self.maze: brd = maze_generator.maze
        self.size: int = size

    class Tile(IntEnum):
        UP = 1 << 0
        RIGHT = 1 << 1
        DOWN = 1 << 2
        LEFT = 1 << 3
