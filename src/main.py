import sys
import pyray as rl

from src.maze import Maze
from src.error import ErrorCode
from src.display import Display
from src.parsing.parsing import Parser


def main() -> int:
    parser = Parser("config.json")
    config = parser.run()
    maze: Maze = Maze(15, 15, 42)
    Display(maze)
    return ErrorCode.NO_ERROR


if (__name__ == "__main__"):
    sys.exit(main())
