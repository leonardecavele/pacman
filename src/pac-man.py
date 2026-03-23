import sys

from .error import ErrorCode

from display.display import Display


def main() -> int:
    display = Display()
    return ErrorCode.NO_ERROR


if (__name__ == "__main__"):
    sys.exit(main())
