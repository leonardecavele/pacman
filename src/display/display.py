import pyray as rl
from mazegenerator import MazeGenerator


class Display:
    def __init__(self, maze: list[list[int]]):
        self.generator = MazeGenerator()
        self.generator.generate(42)
        self.maze = maze
        print(self.maze)
        rl.init_window(1080, 720, "Pac-Man")
        rl.set_target_fps(60)
        self.gap = 10
        cols = len(self.maze[0])
        rows = len(self.maze)
        self.cell_size = min(
            (1080 - (cols - 1) * self.gap) // cols,
            (720 - (rows - 1) * self.gap) // rows,
        ) - 1
        self._generate_tiles()
        self.maze_image = rl.gen_image_color(1080, 720, rl.BLACK)
        self.draw_maze()
        self.maze_texture = rl.load_texture_from_image(self.maze_image)

        while not rl.window_should_close():
            rl.begin_drawing()
            rl.clear_background(rl.WHITE)
            rl.draw_texture(self.maze_texture, 0, 0, rl.WHITE)
            rl.end_drawing()

        rl.close_window()

    def draw_maze(self):
        x, y = 0, 0
        for line in range(len(self.maze)):
            for c in self.maze[line]:
                tile = self.tiles[c]
                src = rl.Rectangle(0, 0, self.cell_size, self.cell_size)
                dst = rl.Rectangle(
                    x * (self.cell_size + self.gap),
                    y * (self.cell_size + self.gap),
                    self.cell_size, self.cell_size)
                rl.image_draw(self.maze_image, tile, src, dst, rl.WHITE)
                # self.put_cell(c, x * (self.cell_size + self.gap),
                #               y * (self.cell_size + self.gap))
                x += 1
            x = 0
            y += 1

    def put_cell(self, c: int, cell_x: int, cell_y: int) -> None:
        """Draw cell wall on image

        Args:
        cell_x, cell_y: Cell coordinates
        """
        if (c & 1):
            rl.image_draw_line(self.maze_image, cell_x, cell_y, cell_x +
                               self.cell_size, cell_y, rl.WHITE)
        if ((c >> 1) & 1):
            rl.image_draw_line(self.maze_image, cell_x + self.cell_size, cell_y,
                               cell_x + self.cell_size, cell_y + self.cell_size, rl.WHITE)
        if ((c >> 2) & 1):
            rl.image_draw_line(self.maze_image, cell_x, cell_y + self.cell_size,
                               cell_x + self.cell_size, cell_y + self.cell_size, rl.WHITE)
        if ((c >> 3) & 1):
            rl.image_draw_line(self.maze_image, cell_x, cell_y,
                               cell_x, cell_y + self.cell_size, rl.WHITE)
        if (c == 0xF):
            rl.image_draw_rectangle(self.maze_image, cell_x, cell_y,
                                    self.cell_size, self.cell_size, rl.WHITE)

    def _generate_tiles(self):
        self.tiles = []
        color = rl.Color(0, 0, 200, 255)
        s = self.cell_size - 1

        for i in range(16):
            top = bool(i & 1)
            right = bool((i >> 1) & 1)
            bot = bool((i >> 2) & 1)
            left = bool((i >> 3) & 1)

            tile = rl.gen_image_color(s, s, rl.BLACK)

            if (top):
                rl.image_draw_line(tile, 0, 0, s - 1, 0, color)
            if (bot):
                rl.image_draw_line(tile, 0, s - 1, s - 1, s - 1, color)
            if (right):
                rl.image_draw_line(tile, s - 1, 0, s - 1, s - 1, color)
            if (left):
                rl.image_draw_line(tile, 0, 0, 0, s - 1, color)

            self.tiles.append(tile)
