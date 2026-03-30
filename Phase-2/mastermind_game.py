import random
import tkinter as tk


COLORS = ["R", "G", "B", "Y", "W", "O"]
COLOR_LABELS = {
    "R": "Ruby",
    "G": "Glow",
    "B": "Blue",
    "Y": "Sun",
    "W": "Frost",
    "O": "Amber",
}
COLOR_HEX = {
    "R": "#ff5f7d",
    "G": "#72ffb8",
    "B": "#6ea8ff",
    "Y": "#ffd15c",
    "W": "#dff4ff",
    "O": "#ff9f5f",
}
TRIES = 10
CODE_LENGTH = 4


def generate_code():
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


def check_code(guess, real_code):
    correct_pos = 0
    incorrect_pos = 0
    color_counts = {}

    for color in real_code:
        color_counts[color] = color_counts.get(color, 0) + 1

    for guess_color, real_color in zip(guess, real_code):
        if guess_color == real_color:
            correct_pos += 1
            color_counts[guess_color] -= 1

    for guess_color, real_color in zip(guess, real_code):
        if guess_color != real_color and color_counts.get(guess_color, 0) > 0:
            incorrect_pos += 1
            color_counts[guess_color] -= 1

    return correct_pos, incorrect_pos


class MastermindUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Neon Frontend")
        self.root.geometry("960x700")
        self.root.minsize(860, 620)
        self.root.configure(bg="#071321")

        self.code = generate_code()
        self.attempts = 0
        self.game_over = False
        self.pulse_direction = 1

        self._build_scene()
        self._fade_in_window()
        self._animate_orbs()
        self._pulse_button()

    def _build_scene(self):
        self.canvas = tk.Canvas(self.root, bg="#071321", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.orbs = [
            {"x": 120, "y": 90, "r": 140, "dx": 0.45,
                "dy": 0.25, "color": "#153a5f"},
            {"x": 760, "y": 140, "r": 180, "dx": -
                0.35, "dy": 0.2, "color": "#3f2a57"},
            {"x": 480, "y": 580, "r": 200, "dx": 0.3,
                "dy": -0.28, "color": "#234a3d"},
        ]

        self.main = tk.Frame(self.root, bg="#0b1c2f", bd=0)
        self.main.place(relx=0.5, rely=0.5, anchor="center",
                        width=860, height=620)

        top = tk.Frame(self.main, bg="#10243a")
        top.pack(fill="x", padx=22, pady=(20, 12))

        title = tk.Label(
            top,
            text="MASTERMIND",
            font=("Segoe UI", 24, "bold"),
            fg="#eaf5ff",
            bg="#10243a",
        )
        title.pack(anchor="w", pady=(8, 0), padx=12)

        subtitle = tk.Label(
            top,
            text="Aesthetic Neon Edition - Crack the 4-color code",
            font=("Segoe UI", 11),
            fg="#9ec0dc",
            bg="#10243a",
        )
        subtitle.pack(anchor="w", pady=(0, 10), padx=12)

        legend = "   ".join(f"{k}={v}" for k, v in COLOR_LABELS.items())
        self.legend_label = tk.Label(
            self.main,
            text=f"Colors: {legend}",
            font=("Segoe UI", 10),
            fg="#b8d4ea",
            bg="#0b1c2f",
        )
        self.legend_label.pack(anchor="w", padx=28)

        self.status_label = tk.Label(
            self.main,
            text=f"Attempts Left: {TRIES}",
            font=("Segoe UI", 12, "bold"),
            fg="#79e6ff",
            bg="#0b1c2f",
        )
        self.status_label.pack(anchor="w", padx=28, pady=(10, 8))

        self.secret_frame = tk.Frame(self.main, bg="#0b1c2f")
        self.secret_frame.pack(anchor="w", padx=28, pady=(0, 14))
        self.secret_slots = []
        for _ in range(CODE_LENGTH):
            slot = tk.Label(
                self.secret_frame,
                text="?",
                font=("Segoe UI", 16, "bold"),
                width=3,
                fg="#0b1c2f",
                bg="#1b3954",
                relief="flat",
            )
            slot.pack(side="left", padx=5)
            self.secret_slots.append(slot)

        input_row = tk.Frame(self.main, bg="#0b1c2f")
        input_row.pack(anchor="w", padx=28)

        self.guess_vars = [tk.StringVar(value=COLORS[0])
                           for _ in range(CODE_LENGTH)]
        for i in range(CODE_LENGTH):
            menu = tk.OptionMenu(input_row, self.guess_vars[i], *COLORS)
            menu.config(
                width=5,
                font=("Segoe UI", 11, "bold"),
                bg="#14324a",
                fg="#ecf7ff",
                activebackground="#1c4566",
                activeforeground="#ffffff",
                highlightthickness=0,
                bd=0,
            )
            menu["menu"].config(bg="#14324a", fg="#ecf7ff",
                                font=("Segoe UI", 10))
            menu.pack(side="left", padx=6)

        self.submit_btn = tk.Button(
            input_row,
            text="Submit Guess",
            command=self.submit_guess,
            font=("Segoe UI", 11, "bold"),
            bg="#ff7b55",
            fg="#1b1010",
            activebackground="#ff8b66",
            activeforeground="#1b1010",
            bd=0,
            padx=18,
            pady=7,
            cursor="hand2",
        )
        self.submit_btn.pack(side="left", padx=12)
        self.submit_btn.bind(
            "<Enter>", lambda _: self.submit_btn.config(bg="#ff986f"))
        self.submit_btn.bind(
            "<Leave>", lambda _: self.submit_btn.config(bg="#ff7b55"))

        self.reset_btn = tk.Button(
            input_row,
            text="New Game",
            command=self.new_game,
            font=("Segoe UI", 10, "bold"),
            bg="#5dd8ff",
            fg="#122033",
            activebackground="#7fe2ff",
            activeforeground="#122033",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
        )
        self.reset_btn.pack(side="left")

        self.feedback_label = tk.Label(
            self.main,
            text="Make your first move",
            font=("Segoe UI", 11),
            fg="#c8deef",
            bg="#0b1c2f",
        )
        self.feedback_label.pack(anchor="w", padx=28, pady=(16, 8))

        history_wrap = tk.Frame(self.main, bg="#0b1c2f")
        history_wrap.pack(fill="both", expand=True, padx=26, pady=(0, 20))

        self.history_canvas = tk.Canvas(
            history_wrap, bg="#0f2134", highlightthickness=0)
        self.history_scroll = tk.Scrollbar(
            history_wrap, orient="vertical", command=self.history_canvas.yview)
        self.history_frame = tk.Frame(self.history_canvas, bg="#0f2134")

        self.history_frame.bind(
            "<Configure>",
            lambda _: self.history_canvas.configure(
                scrollregion=self.history_canvas.bbox("all")),
        )

        self.history_canvas.create_window(
            (0, 0), window=self.history_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scroll.set)

        self.history_canvas.pack(side="left", fill="both", expand=True)
        self.history_scroll.pack(side="right", fill="y")

    def _fade_in_window(self):
        self.root.attributes("-alpha", 0.2)

        def step(alpha):
            alpha += 0.08
            if alpha >= 1.0:
                self.root.attributes("-alpha", 1.0)
                return
            self.root.attributes("-alpha", alpha)
            self.root.after(22, lambda: step(alpha))

        step(0.2)

    def _animate_orbs(self):
        self.canvas.delete("orb")
        width = max(self.root.winfo_width(), 860)
        height = max(self.root.winfo_height(), 620)

        for orb in self.orbs:
            orb["x"] += orb["dx"]
            orb["y"] += orb["dy"]

            if orb["x"] < -80 or orb["x"] > width + 80:
                orb["dx"] *= -1
            if orb["y"] < -80 or orb["y"] > height + 80:
                orb["dy"] *= -1

            x, y, r = orb["x"], orb["y"], orb["r"]
            self.canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill=orb["color"],
                width=0,
                tags="orb",
            )

        self.root.after(38, self._animate_orbs)

    def _pulse_button(self):
        if self.game_over:
            return

        r, g, b = (255, 123, 85)
        shift = 14 * self.pulse_direction
        nr = max(200, min(255, r + shift))
        ng = max(80, min(180, g + shift // 2))
        nb = max(60, min(160, b + shift // 3))
        color = f"#{nr:02x}{ng:02x}{nb:02x}"
        self.submit_btn.config(bg=color)
        self.pulse_direction *= -1
        self.root.after(420, self._pulse_button)

    def _render_history_row(self, guess, exact, misplaced):
        row = tk.Frame(self.history_frame, bg="#1a334b", padx=10, pady=8)
        row.pack(fill="x", padx=10, pady=7)

        peg_text = " ".join(guess)
        guess_label = tk.Label(
            row,
            text=f"Guess {self.attempts:02d}: {peg_text}",
            font=("Consolas", 11, "bold"),
            fg="#e9f5ff",
            bg="#1a334b",
            anchor="w",
        )
        guess_label.pack(side="left", padx=(4, 14))

        chips = tk.Frame(row, bg="#1a334b")
        chips.pack(side="left")

        for _ in range(exact):
            tk.Label(chips, width=2, bg="#72ffb8", text="",
                     relief="flat").pack(side="left", padx=2)
        for _ in range(misplaced):
            tk.Label(chips, width=2, bg="#ffd15c", text="",
                     relief="flat").pack(side="left", padx=2)

        score_label = tk.Label(
            row,
            text=f"Exact {exact} | Misplaced {misplaced}",
            font=("Segoe UI", 10),
            fg="#b8d4ea",
            bg="#1a334b",
        )
        score_label.pack(side="right", padx=4)

        self.history_canvas.update_idletasks()
        self.history_canvas.yview_moveto(1.0)

        self._flash_row(row, 0)

    def _flash_row(self, row, step):
        shades = ["#254a68", "#21425d", "#1d3a54", "#1a334b"]
        if step >= len(shades):
            return
        row.config(bg=shades[step])
        for child in row.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg=shades[step])
            if isinstance(child, tk.Frame):
                child.config(bg=shades[step])
                for inner in child.winfo_children():
                    if isinstance(inner, tk.Label) and inner.cget("bg") in {"#72ffb8", "#ffd15c"}:
                        continue
                    inner.config(bg=shades[step])
        self.root.after(55, lambda: self._flash_row(row, step + 1))

    def _shake(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        offsets = [8, -8, 6, -6, 4, -4, 0]

        def move(i):
            if i >= len(offsets):
                return
            self.root.geometry(f"+{x + offsets[i]}+{y}")
            self.root.after(26, lambda: move(i + 1))

        move(0)

    def _reveal_code(self):
        for index, color in enumerate(self.code):
            self.secret_slots[index].config(
                text=color,
                bg=COLOR_HEX[color],
                fg="#10243a",
            )

    def submit_guess(self):
        if self.game_over:
            return

        guess = [var.get().strip().upper() for var in self.guess_vars]
        if any(color not in COLORS for color in guess):
            self.feedback_label.config(
                text="Choose only valid color letters.", fg="#ffc7b5")
            self._shake()
            return

        self.attempts += 1
        exact, misplaced = check_code(guess, self.code)
        self._render_history_row(guess, exact, misplaced)

        tries_left = max(0, TRIES - self.attempts)
        self.status_label.config(text=f"Attempts Left: {tries_left}")

        if exact == CODE_LENGTH:
            self.game_over = True
            self.feedback_label.config(
                text="You cracked it. Brilliant move!", fg="#72ffb8")
            self.status_label.config(
                text=f"Solved in {self.attempts} attempt(s)")
            self.submit_btn.config(
                state="disabled", bg="#57687a", fg="#d3dae3")
            self._reveal_code()
            return

        if self.attempts >= TRIES:
            self.game_over = True
            self.feedback_label.config(
                text="No tries left. New game?", fg="#ffb39e")
            self.submit_btn.config(
                state="disabled", bg="#57687a", fg="#d3dae3")
            self._reveal_code()
            self._shake()
            return

        self.feedback_label.config(
            text=f"Exact: {exact} | Misplaced: {misplaced}",
            fg="#c8deef",
        )

    def new_game(self):
        self.code = generate_code()
        self.attempts = 0
        self.game_over = False
        self.pulse_direction = 1

        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for slot in self.secret_slots:
            slot.config(text="?", bg="#1b3954", fg="#0b1c2f")

        for var in self.guess_vars:
            var.set(COLORS[0])

        self.feedback_label.config(
            text="Fresh code generated. Good luck.", fg="#79e6ff")
        self.status_label.config(text=f"Attempts Left: {TRIES}")
        self.submit_btn.config(state="normal", bg="#ff7b55", fg="#1b1010")
        self._pulse_button()


def run_game():
    root = tk.Tk()
    MastermindUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_game()
