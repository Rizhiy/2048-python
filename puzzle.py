from enum import Enum
from tkinter import *
from twenty_forty_eight_python.logic import *
from random import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


class Moves(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class TheGame:
    def __init__(self):
        self.commands = {Moves.UP: up, Moves.DOWN: down, Moves.LEFT: left, Moves.RIGHT: right}
        self.matrix = add_number(add_number(new_game(4)))
        self.score = 0
        self.sudden_death = False

    def make_move(self, move: Moves):
        self.matrix, done, score = self.commands[move](self.matrix, self.score)
        if done:
            self.score = score
            self.matrix = add_number(self.matrix)
            return 0
        elif self.sudden_death:
            return -1


class GameGrid(Frame):
    def __init__(self, game=None):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.moves = {KEY_UP: Moves.UP, KEY_DOWN: Moves.DOWN,
                      KEY_LEFT: Moves.LEFT, KEY_RIGHT: Moves.RIGHT}

        self.grid_cells = []
        self.init_grid()
        # Initialise the board
        if game:
            self.game = game
        else:
            self.game = TheGame()
        self.update_grid_cells()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN,
                             height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER,
                          font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number),
                                                    bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        if game_state(self.matrix) == 'win':
            self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
        if game_state(self.matrix) == 'lose':
            self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.moves and self.game.make_move(self.moves[key]) == 0:
            self.update_grid_cells()

    @property
    def matrix(self):
        return self.game.matrix


if __name__ == '__main__':
    gamegrid = GameGrid()
    gamegrid.mainloop()
