import random
import re
import tkinter as tk
from tkinter import messagebox


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)]
                 for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):

        num_neighboring_bombs = 0

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):

        visible_board = [[None for _ in range(
            self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                max(len(str(x)) for x in columns)
            )

        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# GUI Implementation
class MinesweeperGUI:
    def __init__(self, root, dim_size=10, num_bombs=10):
        self.root = root
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = Board(dim_size, num_bombs)
        self.buttons = {}
        self.game_over = False

        self.root.title("Minesweeper")

        # Create menu bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)

        # Create game frame
        self.game_frame = tk.Frame(root)
        self.game_frame.pack(padx=10, pady=10)

        self.create_board()

    def create_board(self):
        # Clear existing buttons
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        # Create buttons for each cell
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                btn = tk.Button(
                    self.game_frame,
                    text='',
                    width=4,
                    height=2,
                    font=('Arial', 10, 'bold'),
                    command=lambda row=r, col=c: self.on_click(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

                # Right-click to flag
                btn.bind('<Button-3>', lambda e, row=r,
                         col=c: self.toggle_flag(row, col))

    def on_click(self, row, col):
        if self.game_over or (row, col) in self.board.dug:
            return

        safe = self.board.dig(row, col)

        if not safe:
            # Hit a bomb
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo("Game Over", "SORRY, GAME OVER!")
        else:
            self.update_board()
            # Check for win
            if len(self.board.dug) >= self.dim_size ** 2 - self.num_bombs:
                self.game_over = True
                messagebox.showinfo("Congratulations",
                                    "CONGRATULATIONS! YOU WON!")

    def toggle_flag(self, row, col):
        if self.game_over or (row, col) in self.board.dug:
            return

        btn = self.buttons[(row, col)]
        if btn['text'] == '🚩':
            btn['text'] = ''
            btn['bg'] = 'SystemButtonFace'
        else:
            btn['text'] = '🚩'
            btn['bg'] = 'yellow'

    def update_board(self):
        colors = {
            0: 'lightgray',
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'darkblue',
            5: 'darkred',
            6: 'cyan',
            7: 'black',
            8: 'gray'
        }

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r, c) in self.board.dug:
                    btn = self.buttons[(r, c)]
                    value = self.board.board[r][c]

                    if value == 0:
                        btn['text'] = ''
                        btn['bg'] = 'lightgray'
                    else:
                        btn['text'] = str(value)
                        btn['fg'] = colors.get(value, 'black')
                        btn['bg'] = 'lightgray'

                    btn['relief'] = tk.SUNKEN

    def reveal_all(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                btn = self.buttons[(r, c)]
                value = self.board.board[r][c]

                if value == '*':
                    btn['text'] = '💣'
                    btn['bg'] = 'red'
                elif (r, c) in self.board.dug:
                    if value == 0:
                        btn['text'] = ''
                    else:
                        btn['text'] = str(value)
                    btn['bg'] = 'lightgray'
                    btn['relief'] = tk.SUNKEN

    def new_game(self):
        self.board = Board(self.dim_size, self.num_bombs)
        self.game_over = False
        self.create_board()


def play(dim_size=10, num_bombs=10):

    board = Board(dim_size, num_bombs)
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(
            ',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid Location. Try again.")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("CONGRATULATIONS! YOU WON!")
    else:
        print("SORRY, GAME OVER!")
        board.dug = set((r, c) for r in range(board.dim_size)
                        for c in range(board.dim_size))
        print(board)


def play_gui(dim_size=10, num_bombs=10):
    root = tk.Tk()
    game = MinesweeperGUI(root, dim_size, num_bombs)
    root.mainloop()


if __name__ == '__main__':
    # Uncomment the version you want to play:
    play_gui()  # GUI version
    # play()  # Console version
