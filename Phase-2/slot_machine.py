import random
import tkinter as tk
from tkinter import messagebox

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

SYMBOL_COUNT = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

SYMBOL_VALUE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

SYMBOL_COLORS = {
    "A": "#FFE082",
    "B": "#80CBC4",
    "C": "#FFAB91",
    "D": "#B39DDB",
}


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        if all(column[line] == symbol for column in columns):
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines


class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Slot Lounge")
        self.root.geometry("980x640")
        self.root.minsize(860, 560)
        self.root.configure(bg="#121829")

        self.balance = 200
        self.spinning = False
        self.reel_labels = []
        self.bg_orbs = []

        self.balance_var = tk.StringVar(value=f"$ {self.balance}")
        self.status_var = tk.StringVar(value="Set your bet and press SPIN.")
        self.bet_var = tk.StringVar(value="10")
        self.lines_var = tk.StringVar(value="3")

        self._build_ui()
        self._animate_background()

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#121829")
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_frame = tk.Frame(self.root, bg="#121829")
        self.main_frame.pack(fill="both", expand=True, padx=24, pady=20)

        self._header_section()
        self._slot_section()
        self._control_section()

    def _header_section(self):
        header = tk.Frame(self.main_frame, bg="#121829")
        header.pack(fill="x", pady=(0, 14))

        tk.Label(
            header,
            text="NEON SLOT LOUNGE",
            fg="#E8F1FF",
            bg="#121829",
            font=("Segoe UI Black", 28),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Aesthetic animated frontend with live slot interaction",
            fg="#9FB3D9",
            bg="#121829",
            font=("Consolas", 11),
        ).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(header, bg="#121829")
        right.pack(anchor="e", pady=(8, 0))

        tk.Label(
            right,
            text="Balance",
            fg="#94A9D1",
            bg="#121829",
            font=("Consolas", 10),
        ).pack(anchor="e")

        tk.Label(
            right,
            textvariable=self.balance_var,
            fg="#61F3D8",
            bg="#121829",
            font=("Segoe UI Semibold", 18),
        ).pack(anchor="e")

    def _slot_section(self):
        slot_box = tk.Frame(self.main_frame, bg="#18213A", bd=0)
        slot_box.pack(fill="x", pady=8)

        tk.Label(
            slot_box,
            text="REELS",
            fg="#C7D8F6",
            bg="#18213A",
            font=("Consolas", 11, "bold"),
        ).pack(anchor="w", padx=16, pady=(10, 6))

        reels_frame = tk.Frame(slot_box, bg="#18213A")
        reels_frame.pack(fill="x", padx=14, pady=(0, 12))

        for _ in range(COLS):
            reel_wrap = tk.Frame(reels_frame, bg="#1F2B47", padx=2, pady=2)
            reel_wrap.pack(side="left", fill="both", expand=True, padx=7)

            reel_label = tk.Label(
                reel_wrap,
                text="A",
                fg=SYMBOL_COLORS["A"],
                bg="#0E1526",
                font=("Segoe UI Black", 44),
                height=2,
            )
            reel_label.pack(fill="both", expand=True)
            self.reel_labels.append(reel_label)

    def _control_section(self):
        controls = tk.Frame(self.main_frame, bg="#121829")
        controls.pack(fill="x", pady=(10, 0))

        form = tk.Frame(controls, bg="#121829")
        form.pack(side="left")

        self._make_input(form, "Bet / line ($)",
                         self.bet_var).grid(row=0, column=0, padx=(0, 10))
        self._make_input(form, "Lines (1-3)",
                         self.lines_var).grid(row=0, column=1)

        self.spin_btn = tk.Button(
            controls,
            text="SPIN",
            command=self.start_spin,
            bg="#2EC4B6",
            activebackground="#53DCCF",
            fg="#0A1323",
            activeforeground="#0A1323",
            font=("Segoe UI Black", 15),
            padx=26,
            pady=10,
            bd=0,
            cursor="hand2",
        )
        self.spin_btn.pack(side="right")

        self.spin_btn.bind(
            "<Enter>", lambda _e: self.spin_btn.configure(bg="#53DCCF"))
        self.spin_btn.bind(
            "<Leave>", lambda _e: self.spin_btn.configure(bg="#2EC4B6"))

        tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            fg="#F3F6FF",
            bg="#121829",
            font=("Consolas", 11),
            anchor="w",
            justify="left",
            wraplength=840,
        ).pack(fill="x", pady=(18, 0))

    def _make_input(self, parent, label_text, variable):
        box = tk.Frame(parent, bg="#121829")
        tk.Label(
            box,
            text=label_text,
            fg="#A4B7DA",
            bg="#121829",
            font=("Consolas", 10),
        ).pack(anchor="w")
        tk.Entry(
            box,
            textvariable=variable,
            bg="#1B2742",
            fg="#EAF2FF",
            insertbackground="#EAF2FF",
            relief="flat",
            width=14,
            font=("Consolas", 12),
        ).pack(ipady=7, pady=(5, 0))
        return box

    def _animate_background(self):
        self.canvas.delete("orb")

        width = max(self.root.winfo_width(), 960)
        height = max(self.root.winfo_height(), 580)

        if not self.bg_orbs:
            for _ in range(7):
                radius = random.randint(90, 180)
                orb = {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "r": radius,
                    "dx": random.uniform(-0.8, 0.8),
                    "dy": random.uniform(-0.6, 0.6),
                    "color": random.choice(["#263E76", "#2D4A93", "#2A7F8A", "#5B3F8F"]),
                }
                self.bg_orbs.append(orb)

        for orb in self.bg_orbs:
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
                stipple="gray50",
                tags="orb",
            )

        self.canvas.tag_lower("orb")
        self.root.after(45, self._animate_background)

    def _read_inputs(self):
        try:
            bet = int(self.bet_var.get().strip())
            lines = int(self.lines_var.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Enter whole numbers for bet and lines.")
            return None

        if not (MIN_BET <= bet <= MAX_BET):
            messagebox.showerror(
                "Invalid Bet", f"Bet per line must be between ${MIN_BET} and ${MAX_BET}.")
            return None

        if not (1 <= lines <= MAX_LINES):
            messagebox.showerror(
                "Invalid Lines", f"Lines must be between 1 and {MAX_LINES}.")
            return None

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showwarning(
                "Low Balance", "Not enough balance for that total bet.")
            return None

        return bet, lines, total_bet

    def start_spin(self):
        if self.spinning:
            return

        parsed = self._read_inputs()
        if not parsed:
            return

        self.current_bet, self.current_lines, self.current_total_bet = parsed
        self.spinning = True
        self.spin_btn.configure(state="disabled")
        self.status_var.set("Spinning reels...")

        self._run_spin_animation(0)

    def _run_spin_animation(self, step):
        if step < 18:
            for idx, reel in enumerate(self.reel_labels):
                if step >= idx * 2:
                    symbol = random.choice(list(SYMBOL_COUNT.keys()))
                    reel.configure(text=symbol, fg=SYMBOL_COLORS[symbol])

            speed = 52 if step < 10 else 72
            self.root.after(speed, lambda: self._run_spin_animation(step + 1))
            return

        self._finish_spin()

    def _finish_spin(self):
        result = get_slot_machine_spin(ROWS, COLS, SYMBOL_COUNT)

        for idx, reel in enumerate(self.reel_labels):
            symbol = result[idx][0]
            reel.configure(text=symbol, fg=SYMBOL_COLORS[symbol])

        winnings, winning_lines = check_winnings(
            result,
            self.current_lines,
            self.current_bet,
            SYMBOL_VALUE,
        )

        self.balance += winnings - self.current_total_bet
        self.balance_var.set(f"$ {self.balance}")

        if winnings > 0:
            line_text = ", ".join(str(line) for line in winning_lines)
            self.status_var.set(
                f"You won $ {winnings} on line(s): {line_text}. Net: +$ {winnings - self.current_total_bet}"
            )
        else:
            self.status_var.set(
                f"No match this spin. Net: -$ {self.current_total_bet}")

        if self.balance <= 0:
            messagebox.showinfo(
                "Game Over", "Your balance is zero. Resetting to $200.")
            self.balance = 200
            self.balance_var.set(f"$ {self.balance}")

        self.spinning = False
        self.spin_btn.configure(state="normal")


def main():
    root = tk.Tk()
    SlotMachineApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
