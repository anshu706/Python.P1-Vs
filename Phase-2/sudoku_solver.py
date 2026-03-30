import copy
import random
import tkinter as tk
from tkinter import messagebox

EMPTY = -1
GRID_SIZE = 9

PUZZLES = [
    [
        [3, 9, EMPTY, EMPTY, 5, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, 2, EMPTY, EMPTY, EMPTY, EMPTY, 5],
        [EMPTY, EMPTY, EMPTY, 7, 1, 9, EMPTY, 8, EMPTY],
        [EMPTY, 5, EMPTY, EMPTY, 6, 8, EMPTY, EMPTY, EMPTY],
        [2, EMPTY, 6, EMPTY, EMPTY, 3, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, 4],
        [5, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [6, 7, EMPTY, 1, EMPTY, 5, EMPTY, 4, EMPTY],
        [1, EMPTY, 9, EMPTY, EMPTY, EMPTY, 2, EMPTY, EMPTY],
    ],
    [
        [EMPTY, 2, EMPTY, 6, EMPTY, 8, EMPTY, EMPTY, EMPTY],
        [5, 8, EMPTY, EMPTY, EMPTY, 9, 7, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, 4, EMPTY, EMPTY, EMPTY, EMPTY],
        [3, 7, EMPTY, EMPTY, EMPTY, EMPTY, 5, EMPTY, EMPTY],
        [6, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, 4],
        [EMPTY, EMPTY, 8, EMPTY, EMPTY, EMPTY, EMPTY, 1, 3],
        [EMPTY, EMPTY, EMPTY, EMPTY, 2, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, 9, 8, EMPTY, EMPTY, EMPTY, 3, 6],
        [EMPTY, EMPTY, EMPTY, 3, EMPTY, 6, EMPTY, 9, EMPTY],
    ],
]


def find_next_empty(puzzle):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if puzzle[r][c] == EMPTY:
                return r, c
    return None, None


def is_valid(puzzle, guess, row, col):
    if guess in puzzle[row]:
        return False

    col_values = [puzzle[r][col] for r in range(GRID_SIZE)]
    if guess in col_values:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True


def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
            puzzle[row][col] = EMPTY

    return False


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("980x730")
        self.root.minsize(900, 680)
        self.root.configure(bg="#0E1220")

        self.cells = []
        self.orbs = []
        self.solving = False
        self.current_puzzle = []
        self.original_puzzle = []
        self.solution_puzzle = []

        self.status_var = tk.StringVar(
            value="Choose a puzzle and tap Solve with Animation.")

        self.canvas = tk.Canvas(self.root, bg="#0E1220", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.content = tk.Frame(self.root, bg="#0E1220")
        self.content.pack(fill="both", expand=True, padx=24, pady=20)

        self._build_header()
        self._build_grid()
        self._build_controls()
        self._load_puzzle(random.choice(PUZZLES))
        self._animate_background()

    def _build_header(self):
        header = tk.Frame(self.content, bg="#0E1220")
        header.pack(fill="x", pady=(0, 12))

        tk.Label(
            header,
            text="SUDOKU AURORA",
            font=("Segoe UI Black", 30),
            fg="#F1F7FF",
            bg="#0E1220",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="A cool, aesthetic frontend with cinematic motion and solve animation",
            font=("Consolas", 11),
            fg="#9CB4E0",
            bg="#0E1220",
        ).pack(anchor="w", pady=(2, 0))

    def _build_grid(self):
        shell = tk.Frame(self.content, bg="#1B2440", padx=4, pady=4)
        shell.pack(pady=10)

        board = tk.Frame(shell, bg="#1B2440")
        board.pack()

        for r in range(GRID_SIZE):
            row_widgets = []
            for c in range(GRID_SIZE):
                cell_bg = "#111A2E" if ((r // 3 + c // 3) %
                                        2 == 0) else "#141F36"
                label = tk.Label(
                    board,
                    text="",
                    width=3,
                    height=1,
                    font=("Segoe UI Semibold", 20),
                    bg=cell_bg,
                    fg="#EAF2FF",
                    relief="flat",
                )

                padx = (3, 1) if c % 3 == 0 else (1, 1)
                pady = (3, 1) if r % 3 == 0 else (1, 1)
                if c == 8:
                    padx = (1, 3)
                if r == 8:
                    pady = (1, 3)

                label.grid(row=r, column=c, padx=padx,
                           pady=pady, sticky="nsew")
                row_widgets.append(label)

            self.cells.append(row_widgets)

    def _build_controls(self):
        controls = tk.Frame(self.content, bg="#0E1220")
        controls.pack(fill="x", pady=(10, 0))

        self.solve_btn = tk.Button(
            controls,
            text="Solve with Animation",
            command=self.start_solve_animation,
            bg="#39D0C5",
            fg="#081321",
            activebackground="#64E3DA",
            activeforeground="#081321",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            font=("Segoe UI Semibold", 12),
        )
        self.solve_btn.pack(side="left")

        self.new_btn = tk.Button(
            controls,
            text="New Puzzle",
            command=self.new_puzzle,
            bg="#FF9D66",
            fg="#211108",
            activebackground="#FFB789",
            activeforeground="#211108",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            font=("Segoe UI Semibold", 12),
        )
        self.new_btn.pack(side="left", padx=(10, 0))

        self.reset_btn = tk.Button(
            controls,
            text="Reset",
            command=self.reset_board,
            bg="#7A8CFF",
            fg="#FFFFFF",
            activebackground="#9FAEFF",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            font=("Segoe UI Semibold", 12),
        )
        self.reset_btn.pack(side="left", padx=(10, 0))

        for button, base, hover in [
            (self.solve_btn, "#39D0C5", "#64E3DA"),
            (self.new_btn, "#FF9D66", "#FFB789"),
            (self.reset_btn, "#7A8CFF", "#9FAEFF"),
        ]:
            button.bind("<Enter>", lambda _e, btn=button,
                        color=hover: btn.configure(bg=color))
            button.bind("<Leave>", lambda _e, btn=button,
                        color=base: btn.configure(bg=color))

        tk.Label(
            self.content,
            textvariable=self.status_var,
            bg="#0E1220",
            fg="#EAF2FF",
            font=("Consolas", 11),
            justify="left",
            anchor="w",
            wraplength=900,
        ).pack(fill="x", pady=(16, 0))

    def _set_buttons_state(self, state):
        self.solve_btn.configure(state=state)
        self.new_btn.configure(state=state)
        self.reset_btn.configure(state=state)

    def _load_puzzle(self, puzzle):
        self.original_puzzle = copy.deepcopy(puzzle)
        self.current_puzzle = copy.deepcopy(puzzle)
        self.solution_puzzle = []
        self._render_grid()
        self.status_var.set(
            "Puzzle loaded. Hit Solve with Animation to watch the logic in motion.")

    def _render_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.current_puzzle[r][c]
                text = "" if value == EMPTY else str(value)
                is_original = self.original_puzzle[r][c] != EMPTY
                fg = "#EAF2FF" if is_original else "#6BE8D7"
                self.cells[r][c].configure(text=text, fg=fg)

    def _animate_background(self):
        self.canvas.delete("orb")
        width = max(self.root.winfo_width(), 920)
        height = max(self.root.winfo_height(), 680)

        if not self.orbs:
            for _ in range(8):
                self.orbs.append(
                    {
                        "x": random.randint(0, width),
                        "y": random.randint(0, height),
                        "r": random.randint(110, 210),
                        "dx": random.uniform(-1.0, 1.0),
                        "dy": random.uniform(-0.8, 0.8),
                        "color": random.choice(["#223769", "#2F1F66", "#205D64", "#2D3B8A"]),
                    }
                )

        for orb in self.orbs:
            orb["x"] += orb["dx"]
            orb["y"] += orb["dy"]

            if orb["x"] < -orb["r"] or orb["x"] > width + orb["r"]:
                orb["dx"] *= -1
            if orb["y"] < -orb["r"] or orb["y"] > height + orb["r"]:
                orb["dy"] *= -1

            self.canvas.create_oval(
                orb["x"] - orb["r"],
                orb["y"] - orb["r"],
                orb["x"] + orb["r"],
                orb["y"] + orb["r"],
                fill=orb["color"],
                outline="",
                tags="orb",
                stipple="gray50",
            )

        self.canvas.tag_lower("orb")
        self.root.after(45, self._animate_background)

    def new_puzzle(self):
        if self.solving:
            return
        self._load_puzzle(random.choice(PUZZLES))

    def reset_board(self):
        if self.solving:
            return
        self.current_puzzle = copy.deepcopy(self.original_puzzle)
        self._render_grid()
        self.status_var.set("Board reset to original puzzle.")

    def start_solve_animation(self):
        if self.solving:
            return

        candidate = copy.deepcopy(self.current_puzzle)
        solved = solve_sudoku(candidate)
        if not solved:
            messagebox.showerror(
                "No Solution", "This puzzle does not have a valid solution.")
            return

        self.solution_puzzle = candidate
        self.solving = True
        self._set_buttons_state("disabled")

        self.status_var.set("Solving with animated reveal...")
        steps = [
            (r, c)
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if self.original_puzzle[r][c] == EMPTY
        ]
        self._animate_steps(steps, 0)

    def _animate_steps(self, steps, index):
        if index >= len(steps):
            self.solving = False
            self._set_buttons_state("normal")
            self.status_var.set("Solved. Smooth, clean, and complete.")
            return

        r, c = steps[index]
        value = self.solution_puzzle[r][c]
        self.current_puzzle[r][c] = value
        cell = self.cells[r][c]
        cell.configure(text=str(value), fg="#7AF4E1", bg="#203054")

        self.root.after(55, lambda: cell.configure(
            bg="#141F36" if ((r // 3 + c // 3) % 2) else "#111A2E"))
        self.root.after(68, lambda: self._animate_steps(steps, index + 1))


def main():
    root = tk.Tk()
    SudokuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
