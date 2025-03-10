import tkinter as tk
from tkinter import messagebox
import random
import time

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
ARROW_COUNT = 2

# Wumpus World elements
PIT = "P"
WUMPUS = "W"
GOLD = "G"
STENCH = "S"
BREEZE = "B"
PLAYER = "P"


class WumpusWorld:
    def __init__(self, root):
        self.root = root
        self.root.title("Wumpus World")
        self.start_time = time.time()
        self.timer_label = tk.Label(
            self.root, text="Time: 0s", font=("Arial", 16))
        self.timer_label.pack()
        self.grid = self.create_grid()
        self.player_pos = (0, 0)
        self.revealed_tiles = [
            [False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # Player's starting position is revealed
        self.revealed_tiles[0][0] = True
        self.arrows = ARROW_COUNT
        self.create_gui()
        self.update_gui()
        self.update_timer()

        # Set a minimum window size
        self.root.minsize(GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE + 50)

    def create_grid(self):
        grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        # Place Wumpus
        wumpus_pos = (random.randint(0, GRID_SIZE-1),
                      random.randint(0, GRID_SIZE-1))
        grid[wumpus_pos[0]][wumpus_pos[1]] = WUMPUS
        # Place pits
        for _ in range(3):
            pit_pos = (random.randint(0, GRID_SIZE-1),
                       random.randint(0, GRID_SIZE-1))
            while grid[pit_pos[0]][pit_pos[1]] is not None:
                pit_pos = (random.randint(0, GRID_SIZE-1),
                           random.randint(0, GRID_SIZE-1))
            grid[pit_pos[0]][pit_pos[1]] = PIT
        # Place gold
        gold_pos = (random.randint(0, GRID_SIZE-1),
                    random.randint(0, GRID_SIZE-1))
        while grid[gold_pos[0]][gold_pos[1]] is not None:
            gold_pos = (random.randint(0, GRID_SIZE-1),
                        random.randint(0, GRID_SIZE-1))
        grid[gold_pos[0]][gold_pos[1]] = GOLD
        # Add stench and breeze
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == WUMPUS:
                    self.add_percept(grid, i, j, STENCH)
                elif grid[i][j] == PIT:
                    self.add_percept(grid, i, j, BREEZE)
        return grid

    def add_percept(self, grid, x, y, percept):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] is None:
                    grid[nx][ny] = percept
                elif grid[nx][ny] in [STENCH, BREEZE]:
                    grid[nx][ny] += percept

    def create_gui(self):
        self.canvas = tk.Canvas(
            self.root, width=GRID_SIZE*TILE_SIZE, height=GRID_SIZE*TILE_SIZE)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Configure>", self.on_resize)

    def update_gui(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x0, y0 = i*TILE_SIZE, j*TILE_SIZE
                x1, y1 = x0 + TILE_SIZE, y0 + TILE_SIZE
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill="lightgrey", outline="black")
                if self.revealed_tiles[i][j]:
                    if (i, j) == self.player_pos:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="P", font=("Arial", 24))
                    elif self.grid[i][j] == WUMPUS:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="W", font=("Arial", 24))
                    elif self.grid[i][j] == PIT:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="O", font=("Arial", 24))
                    elif self.grid[i][j] == GOLD:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="G", font=("Arial", 24))
                    elif self.grid[i][j] == STENCH:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="S", font=("Arial", 24))
                    elif self.grid[i][j] == BREEZE:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="B", font=("Arial", 24))
                    elif self.grid[i][j] == STENCH + BREEZE:
                        self.canvas.create_text(
                            (x0+x1)//2, (y0+y1)//2, text="SB", font=("Arial", 24))
                else:
                    self.canvas.create_text(
                        (x0+x1)//2, (y0+y1)//2, text="?", font=("Arial", 24))

    def on_click(self, event):
        x, y = event.x // TILE_SIZE, event.y // TILE_SIZE
        if self.is_adjacent(self.player_pos, (x, y)):
            self.move_player((x, y))
        elif not self.revealed_tiles[x][y]:
            self.reveal_tile(x, y)
        self.update_gui()

    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def move_player(self, new_pos):
        self.player_pos = new_pos
        self.revealed_tiles[new_pos[0]][new_pos[1]] = True
        if self.grid[new_pos[0]][new_pos[1]] == PIT:
            messagebox.showinfo("Game Over", "You fell into a pit!")
            self.root.quit()
        elif self.grid[new_pos[0]][new_pos[1]] == WUMPUS:
            messagebox.showinfo("Game Over", "You were eaten by the Wumpus!")
            self.root.quit()
        elif self.grid[new_pos[0]][new_pos[1]] == GOLD:
            messagebox.showinfo(
                "Victory", "You found the gold and won the game! Hurray")
            self.root.quit()

    def reveal_tile(self, x, y):
        self.revealed_tiles[x][y] = True

    def update_timer(self):
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.root.after(1000, self.update_timer)

    def on_resize(self, event):
        global TILE_SIZE
        # Ensure the window does not collapse
        new_tile_size = min(event.width // GRID_SIZE, event.height // GRID_SIZE)
        if new_tile_size < 50:  # Set a minimum tile size
            new_tile_size = 50
        TILE_SIZE = new_tile_size
        self.update_gui()


if __name__ == "__main__":
    root = tk.Tk()
    game = WumpusWorld(root)
    root.mainloop()
