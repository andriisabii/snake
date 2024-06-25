import random
import curses
import time

class SnakeGame:

    def __init__(self, width=20, height=10):
        self.width, self.height = width, height
        self.snake = [(height//2, width//2)]
        self.direction, self.apple, self.score = curses.KEY_RIGHT, self.place_apple(), 0

    def place_apple(self):
        return (random.randint(0, self.height-1), random.randint(0, self.width-1))

    def move_snake(self):
        head = self.snake[0]
        dirs = {curses.KEY_RIGHT: (0, 1), curses.KEY_LEFT: (0, -1), curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0)}
        new_head = (head[0] + dirs[self.direction][0], head[1] + dirs[self.direction][1])

        if new_head in self.snake[1:] or new_head[0] < 0 or new_head[0] >= self.height or new_head[1] < 0 or new_head[1] >= self.width:
            return False

        self.snake.insert(0, new_head)
        if new_head == self.apple:
            self.score += 1
            self.apple = self.place_apple()
        else:
            self.snake.pop()
        return True

    def display(self, win):
        win.clear()
        for i in range(self.height):
            for j in range(self.width):
                char = 'X' if (i, j) == self.snake[0] else 'O' if (i, j) == self.apple else 'x' if (i, j) in self.snake[1:] else '.'
                win.addch(i, j, char)
        win.addstr(self.height, 0, f"Score: {self.score}")
        win.refresh()

    def run(self, win):
        win.nodelay(1)
        while True:
            try:
                key = win.getch()
                if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                    if key == curses.KEY_RIGHT and self.last_direction != curses.KEY_LEFT:
                        self.direction = key
                    elif key == curses.KEY_LEFT and self.last_direction != curses.KEY_RIGHT:
                        self.direction = key
                    elif key == curses.KEY_UP and self.last_direction != curses.KEY_DOWN:
                        self.direction = key
                    elif key == curses.KEY_DOWN and self.last_direction != curses.KEY_UP:
                        self.direction = key
                if not self.move_snake():
                    break
                self.last_direction = self.direction
                self.display(win)
                time.sleep(0.2)
            except curses.error:
                pass

curses.wrapper(SnakeGame().run)
