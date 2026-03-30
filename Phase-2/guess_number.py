import random
import tkinter as tk


class GuessNumberApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Guess The Number")
        self.root.geometry("860x580")
        self.root.minsize(820, 560)
        self.root.configure(bg="#0b132b")

        self.player_target = None
        self.player_attempts = 0
        self.player_max_value = 100

        self.computer_low = 1
        self.computer_high = 100
        self.computer_guess_value = None
        self.computer_attempts = 0

        self._build_ui()
        self._start_player_game()

    def _build_ui(self):
        title = tk.Label(
            self.root,
            text="Guess Number Studio",
            font=("Poppins", 28, "bold"),
            fg="#f7f7ff",
            bg="#0b132b",
        )
        title.pack(pady=(24, 8))

        subtitle = tk.Label(
            self.root,
            text="A modern number duel: you vs the machine",
            font=("Poppins", 12),
            fg="#9fb3c8",
            bg="#0b132b",
        )
        subtitle.pack(pady=(0, 18))

        switcher = tk.Frame(self.root, bg="#0b132b")
        switcher.pack(pady=(0, 18))

        self.mode_var = tk.StringVar(value="player")
        player_btn = tk.Radiobutton(
            switcher,
            text="I Guess",
            variable=self.mode_var,
            value="player",
            command=self._show_mode,
            font=("Poppins", 11, "bold"),
            indicatoron=False,
            width=14,
            bg="#1c2541",
            fg="#e6edf3",
            selectcolor="#3a506b",
            activebackground="#3a506b",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        )
        player_btn.grid(row=0, column=0, padx=6)

        computer_btn = tk.Radiobutton(
            switcher,
            text="Computer Guesses",
            variable=self.mode_var,
            value="computer",
            command=self._show_mode,
            font=("Poppins", 11, "bold"),
            indicatoron=False,
            width=14,
            bg="#1c2541",
            fg="#e6edf3",
            selectcolor="#3a506b",
            activebackground="#3a506b",
            activeforeground="#ffffff",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        )
        computer_btn.grid(row=0, column=1, padx=6)

        self.card = tk.Frame(
            self.root,
            bg="#1c2541",
            highlightthickness=2,
            highlightbackground="#5bc0be",
            padx=28,
            pady=24,
        )
        self.card.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        self.player_panel = tk.Frame(self.card, bg="#1c2541")
        self.computer_panel = tk.Frame(self.card, bg="#1c2541")

        self._build_player_panel()
        self._build_computer_panel()
        self._show_mode()

    def _build_player_panel(self):
        heading = tk.Label(
            self.player_panel,
            text="You Guess the Secret Number",
            font=("Poppins", 20, "bold"),
            bg="#1c2541",
            fg="#f4f7fb",
        )
        heading.pack(anchor="w")

        controls = tk.Frame(self.player_panel, bg="#1c2541")
        controls.pack(anchor="w", pady=(16, 10))

        tk.Label(
            controls,
            text="Max Number",
            font=("Poppins", 11),
            bg="#1c2541",
            fg="#b8c6d4",
        ).grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.player_max_entry = tk.Entry(
            controls,
            width=10,
            font=("Poppins", 11),
            bg="#0b132b",
            fg="#f4f7fb",
            insertbackground="#f4f7fb",
            relief="flat",
            justify="center",
        )
        self.player_max_entry.grid(row=0, column=1, padx=(0, 10))
        self.player_max_entry.insert(0, "100")

        new_game_btn = tk.Button(
            controls,
            text="New Game",
            command=self._start_player_game,
            font=("Poppins", 10, "bold"),
            bg="#5bc0be",
            fg="#0b132b",
            bd=0,
            padx=14,
            pady=7,
            cursor="hand2",
            activebackground="#74d6d4",
        )
        new_game_btn.grid(row=0, column=2)

        guess_row = tk.Frame(self.player_panel, bg="#1c2541")
        guess_row.pack(anchor="w", pady=(6, 16))

        self.player_guess_entry = tk.Entry(
            guess_row,
            width=20,
            font=("Poppins", 13),
            bg="#0b132b",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            justify="center",
        )
        self.player_guess_entry.grid(row=0, column=0, padx=(0, 10))
        self.player_guess_entry.bind(
            "<Return>", lambda _event: self._submit_player_guess())

        submit_btn = tk.Button(
            guess_row,
            text="Submit Guess",
            command=self._submit_player_guess,
            font=("Poppins", 10, "bold"),
            bg="#3a506b",
            fg="#f5f9ff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            activebackground="#526b8a",
        )
        submit_btn.grid(row=0, column=1)

        self.player_feedback = tk.Label(
            self.player_panel,
            text="",
            font=("Poppins", 12),
            bg="#1c2541",
            fg="#d8e2ec",
        )
        self.player_feedback.pack(anchor="w", pady=(4, 10))

        self.player_attempts_label = tk.Label(
            self.player_panel,
            text="Attempts: 0",
            font=("Poppins", 11, "bold"),
            bg="#1c2541",
            fg="#9dd9d8",
        )
        self.player_attempts_label.pack(anchor="w")

    def _build_computer_panel(self):
        heading = tk.Label(
            self.computer_panel,
            text="Computer Guesses Your Number",
            font=("Poppins", 20, "bold"),
            bg="#1c2541",
            fg="#f4f7fb",
        )
        heading.pack(anchor="w")

        instructions = tk.Label(
            self.computer_panel,
            text="Think of a number, then guide the computer with the buttons.",
            font=("Poppins", 11),
            bg="#1c2541",
            fg="#b8c6d4",
        )
        instructions.pack(anchor="w", pady=(6, 16))

        top_controls = tk.Frame(self.computer_panel, bg="#1c2541")
        top_controls.pack(anchor="w", pady=(0, 14))

        tk.Label(
            top_controls,
            text="Max Number",
            font=("Poppins", 11),
            bg="#1c2541",
            fg="#b8c6d4",
        ).grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.computer_max_entry = tk.Entry(
            top_controls,
            width=10,
            font=("Poppins", 11),
            bg="#0b132b",
            fg="#f4f7fb",
            insertbackground="#f4f7fb",
            relief="flat",
            justify="center",
        )
        self.computer_max_entry.grid(row=0, column=1, padx=(0, 10))
        self.computer_max_entry.insert(0, "100")

        start_btn = tk.Button(
            top_controls,
            text="Start",
            command=self._start_computer_game,
            font=("Poppins", 10, "bold"),
            bg="#5bc0be",
            fg="#0b132b",
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            activebackground="#74d6d4",
        )
        start_btn.grid(row=0, column=2)

        self.computer_guess_label = tk.Label(
            self.computer_panel,
            text="Press Start to make the first guess.",
            font=("Poppins", 15, "bold"),
            bg="#1c2541",
            fg="#f7f9fd",
        )
        self.computer_guess_label.pack(anchor="w", pady=(2, 16))

        feedback_buttons = tk.Frame(self.computer_panel, bg="#1c2541")
        feedback_buttons.pack(anchor="w")

        self.low_btn = tk.Button(
            feedback_buttons,
            text="Too Low",
            command=lambda: self._computer_feedback("l"),
            font=("Poppins", 10, "bold"),
            bg="#3a506b",
            fg="#f5f9ff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            activebackground="#526b8a",
            state="disabled",
        )
        self.low_btn.grid(row=0, column=0, padx=(0, 8))

        self.high_btn = tk.Button(
            feedback_buttons,
            text="Too High",
            command=lambda: self._computer_feedback("h"),
            font=("Poppins", 10, "bold"),
            bg="#3a506b",
            fg="#f5f9ff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            activebackground="#526b8a",
            state="disabled",
        )
        self.high_btn.grid(row=0, column=1, padx=8)

        self.correct_btn = tk.Button(
            feedback_buttons,
            text="Correct",
            command=lambda: self._computer_feedback("c"),
            font=("Poppins", 10, "bold"),
            bg="#5bc0be",
            fg="#0b132b",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground="#74d6d4",
            state="disabled",
        )
        self.correct_btn.grid(row=0, column=2, padx=(8, 0))

        self.computer_attempts_label = tk.Label(
            self.computer_panel,
            text="Attempts: 0",
            font=("Poppins", 11, "bold"),
            bg="#1c2541",
            fg="#9dd9d8",
        )
        self.computer_attempts_label.pack(anchor="w", pady=(16, 8))

        self.computer_status = tk.Label(
            self.computer_panel,
            text="",
            font=("Poppins", 11),
            bg="#1c2541",
            fg="#d8e2ec",
        )
        self.computer_status.pack(anchor="w")

    def _show_mode(self):
        self.player_panel.pack_forget()
        self.computer_panel.pack_forget()

        if self.mode_var.get() == "player":
            self.player_panel.pack(fill="both", expand=True)
            self.player_guess_entry.focus_set()
        else:
            self.computer_panel.pack(fill="both", expand=True)

    def _start_player_game(self):
        max_value_text = self.player_max_entry.get().strip()
        try:
            max_value = int(max_value_text)
            if max_value < 2:
                raise ValueError
        except ValueError:
            self.player_feedback.config(
                text="Use a valid max number (2 or higher).", fg="#f7b267")
            return

        self.player_max_value = max_value
        self.player_target = random.randint(1, self.player_max_value)
        self.player_attempts = 0
        self.player_attempts_label.config(text="Attempts: 0")
        self.player_feedback.config(
            text=f"New game ready. Guess a number from 1 to {self.player_max_value}.",
            fg="#d8e2ec",
        )
        self.player_guess_entry.delete(0, tk.END)
        self.player_guess_entry.focus_set()

    def _submit_player_guess(self):
        if self.player_target is None:
            self._start_player_game()
            return

        guess_text = self.player_guess_entry.get().strip()
        try:
            value = int(guess_text)
        except ValueError:
            self.player_feedback.config(
                text="Enter a whole number.", fg="#f7b267")
            return

        if value < 1 or value > self.player_max_value:
            self.player_feedback.config(
                text=f"Guess must be in range 1 to {self.player_max_value}.",
                fg="#f7b267",
            )
            return

        self.player_attempts += 1
        self.player_attempts_label.config(
            text=f"Attempts: {self.player_attempts}")

        if value < self.player_target:
            self.player_feedback.config(
                text="Too low. Push it higher.", fg="#9dd9d8")
        elif value > self.player_target:
            self.player_feedback.config(
                text="Too high. Bring it down.", fg="#9dd9d8")
        else:
            self.player_feedback.config(
                text=(
                    f"Perfect guess. {value} is correct in "
                    f"{self.player_attempts} attempts."
                ),
                fg="#86efac",
            )

        self.player_guess_entry.delete(0, tk.END)

    def _start_computer_game(self):
        max_value_text = self.computer_max_entry.get().strip()
        try:
            max_value = int(max_value_text)
            if max_value < 2:
                raise ValueError
        except ValueError:
            self.computer_status.config(
                text="Use a valid max number (2 or higher).", fg="#f7b267")
            return

        self.computer_low = 1
        self.computer_high = max_value
        self.computer_attempts = 0
        self.computer_status.config(
            text=f"Think of a number from 1 to {max_value}. I am guessing now...",
            fg="#d8e2ec",
        )
        self._enable_computer_buttons(True)
        self._make_computer_guess()

    def _make_computer_guess(self):
        if self.computer_low > self.computer_high:
            self.computer_status.config(
                text="The hints conflict. Restart and try consistent feedback.",
                fg="#f7b267",
            )
            self._enable_computer_buttons(False)
            return

        self.computer_guess_value = random.randint(
            self.computer_low, self.computer_high)
        self.computer_attempts += 1
        self.computer_guess_label.config(
            text=f"Is your number {self.computer_guess_value}?")
        self.computer_attempts_label.config(
            text=f"Attempts: {self.computer_attempts}")

    def _computer_feedback(self, feedback: str):
        if self.computer_guess_value is None:
            return

        if feedback == "l":
            self.computer_low = self.computer_guess_value + 1
            self.computer_status.config(
                text="Raising the lower bound.", fg="#9dd9d8")
            self._make_computer_guess()
        elif feedback == "h":
            self.computer_high = self.computer_guess_value - 1
            self.computer_status.config(
                text="Dropping the upper bound.", fg="#9dd9d8")
            self._make_computer_guess()
        elif feedback == "c":
            self.computer_guess_label.config(
                text=f"Locked in: {self.computer_guess_value}")
            self.computer_status.config(
                text=(
                    f"Victory. I found your number in "
                    f"{self.computer_attempts} attempts."
                ),
                fg="#86efac",
            )
            self._enable_computer_buttons(False)

    def _enable_computer_buttons(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.low_btn.config(state=state)
        self.high_btn.config(state=state)
        self.correct_btn.config(state=state)


def main():
    root = tk.Tk()
    GuessNumberApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
